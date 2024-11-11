# classifier/model.py

import torch
from torchvision import models, transforms
from PIL import Image
import json

# Charger le modèle ResNet
model = models.resnet18(pretrained=True)
model.eval()


import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
imagenet_classes_path = os.path.join(BASE_DIR, "classifier", "imagenet_classes.txt")

with open(imagenet_classes_path) as f:
    class_names = json.load(f)


# Transformation pour le prétraitement des images
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def predict_image(image_path):
    # Charger et transformer l'image
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image)
    _, predicted = outputs.max(1)
    return class_names[predicted.item()]  # Retourne le nom de la classe prédite
    
