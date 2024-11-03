from django.shortcuts import render

# Create your views here.


# classifier/views.py

from .model import predict_image
import os

def classify_image(request):
    if request.method == 'POST' and request.FILES['image']:
        # Sauvegarder l'image téléchargée
        uploaded_image = request.FILES['image']
        image_path = os.path.join('media', uploaded_image.name)
        
        with open(image_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)
        
        # Effectuer la prédiction
        prediction = predict_image(image_path)
        return render(request, 'classifier/result.html', {
            'prediction': prediction,
            'image_path': image_path
        })
    return render(request, 'classifier/upload.html')
