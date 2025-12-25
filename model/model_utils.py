import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0
import json
import numpy as np
import cv2
from PIL import Image
import os

try:
    with open('model/cat_to_name.json', 'r') as f:
        cat_to_name = json.load(f)
    print(f"✅ Loaded {len(cat_to_name)} flower names from cat_to_name.json")
except FileNotFoundError:
    print("❌ Error: File 'cat_to_name.json' tidak ditemukan.")
    cat_to_name = {str(i): f"Unknown Flower {i}" for i in range(102)}

def create_flower_model(num_classes=102):
    """Membuat arsitektur model berdasarkan EfficientNetB0."""
    base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False 
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

def predict_flower(model_obj, cat_to_name, class_names, img_path=None, img_array=None):
    """
    Fungsi untuk memprediksi gambar bunga. 
    Menerima objek model yang sudah dimuat (model_obj).
    """

    if img_path:
        img = Image.open(img_path).convert('RGB')
        img = img.resize((224, 224)) 
        img_array_processed = np.array(img)
    elif img_array is not None:
        img_array_processed = cv2.resize(img_array, (224, 224))
    else:
        raise ValueError("Harus ada img_path atau img_array untuk prediksi.")

    img_array_processed = img_array_processed.astype('float32') / 255.0
    img_array_processed = np.expand_dims(img_array_processed, axis=0)

    preds = model_obj.predict(img_array_processed, verbose=0) 
    top_idx = np.argmax(preds[0])
    confidence = float(preds[0][top_idx])

    class_num_str = class_names.get(top_idx, str(top_idx))
    flower_name = cat_to_name.get(class_num_str, f"Kelas tidak dikenal: {class_num_str}")

    return flower_name, confidence, preds[0], top_idx
