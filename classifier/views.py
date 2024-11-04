from django.shortcuts import render, redirect
from .models import ClassificationHistory


from .model import predict_image
import os

# def classify_image(request):
#     if request.method == 'POST' and request.FILES['image']:
#         # Sauvegarder l'image téléchargée
#         uploaded_image = request.FILES['image']
#         image_path = os.path.join('media', uploaded_image.name)
        
#         with open(image_path, 'wb+') as destination:
#             for chunk in uploaded_image.chunks():
#                 destination.write(chunk)
        
#         # Effectuer la prédiction
#         prediction = predict_image(image_path)
#         return render(request, 'classifier/result.html', {
#             'prediction': prediction,
#             'image_path': image_path
#         })
#     return render(request, 'classifier/upload.html')


def classify_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        image_path = os.path.join('media', uploaded_image.name)

        with open(image_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        prediction = predict_image(image_path)

        # Save classification history
        if request.user.is_authenticated:
            ClassificationHistory.objects.create(
                user=request.user,
                image=uploaded_image,
                prediction=prediction
            )

        return render(request, 'classifier/result.html', {
            'prediction': prediction,
            'image_path': image_path
        })
    return render(request, 'classifier/upload.html')




from .models import ClassificationHistory

def classification_history(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    history = ClassificationHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'classifier/history.html', {'history': history})
