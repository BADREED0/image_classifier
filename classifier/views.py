
from django.shortcuts import render, redirect
from .models import ClassificationHistory
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import tensorflow as tf
import io
import os

# Charger le modèle de classification
model = load_model(os.path.join('model', 'Image_classify.keras'))

# Catégories pour la classification
data_cat = [
    'apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot', 
    'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic', 'ginger', 
    'grapes', 'jalapeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion', 'orange', 
    'paprika', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato', 'radish', 
    'soy beans', 'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelon'
]

def classify_image(request):
    result, confidence, image_path = None, None, None
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image_path = os.path.join('media', image_file.name)

        # Sauvegarder l'image dans le dossier 'media'
        with open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Charger et prétraiter l'image
        img = load_img(image_path, target_size=(180, 180))
        img_array = img_to_array(img)
        img_batch = tf.expand_dims(img_array, 0)

        # Faire une prédiction
        predictions = model.predict(img_batch)
        score = tf.nn.softmax(predictions[0])

        # Résultat de la prédiction
        predicted_category = data_cat[np.argmax(score)]
        result =  predicted_category
        confidence = f"{np.max(score) * 100:.2f}%"

        # Enregistrer l'historique de classification pour les utilisateurs authentifiés
        if request.user.is_authenticated:
            ClassificationHistory.objects.create(
                user=request.user,
                image=image_file,
                prediction=predicted_category
            )

        return render(request, 'classifier/result.html', {
            'result': result,
            'confidence': confidence,
            'image_path': image_path  # Passer le chemin de l'image
        })

    return render(request, 'classifier/upload.html')




from .models import ClassificationHistory

def classification_history(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    history = ClassificationHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'classifier/history.html', {'history': history})
