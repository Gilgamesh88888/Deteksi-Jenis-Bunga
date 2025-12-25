from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import json
import tensorflow as tf
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load model
try:
    model = tf.keras.models.load_model('model/flower_classification_model_MobileNetV2.keras')
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Load flower names mapping
try:
    with open('model/cat_to_name.json', 'r') as f:
        cat_to_name = json.load(f)
    print(f"✅ Loaded {len(cat_to_name)} flower names")
except FileNotFoundError:
    print("❌ cat_to_name.json not found")
    cat_to_name = {str(i): f"Unknown Flower {i}" for i in range(1, 103)}

class_names = {i: str(i+1) for i in range(102)}

def preprocess_image(img_path=None, img_array=None):
    """Preprocess image untuk prediksi"""
    if img_path:
        img = Image.open(img_path).convert('RGB')
        img = img.resize((224, 224))
        img_array_processed = np.array(img)
    elif img_array is not None:
        img_array_processed = cv2.resize(img_array, (224, 224))
    else:
        raise ValueError("Harus ada img_path atau img_array")
    
    img_array_processed = img_array_processed.astype('float32') / 255.0
    img_array_processed = np.expand_dims(img_array_processed, axis=0)
    return img_array_processed

def predict_flower(img_path=None, img_array=None):
    """Prediksi jenis bunga"""
    if model is None:
        return None, 0, "Model belum dimuat"
    
    try:
        img_processed = preprocess_image(img_path, img_array)
        preds = model.predict(img_processed, verbose=0)
        top_idx = np.argmax(preds[0])
        confidence = float(preds[0][top_idx])
        
        class_num_str = class_names.get(top_idx, str(top_idx))
        flower_name = cat_to_name.get(class_num_str, f"Kelas tidak dikenal: {class_num_str}")
        
        return flower_name, confidence, None
    except Exception as e:
        return None, 0, str(e)

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload prediction"""
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file gambar'}), 400
    
    file = request.files['file']
    if file.filename == "":
        return jsonify({'error': 'Nama file kosong'}), 400
    
    if not file or not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return jsonify({'error': 'Format gambar tidak didukung'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        flower_name, confidence, error = predict_flower(img_path=filepath)
        
        if error:
            return jsonify({'error': error}), 500
        
        return jsonify({
            "success": True,
            "filename": f"/uploads/{filename}",
            "prediction": flower_name,
            "confidence": float(confidence * 100)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/camera_predict', methods=['POST'])
def camera_predict():
    """Handle camera prediction"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Tidak ada data kamera'}), 400
        
        file = request.files['image']
        img_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({"error": "Gagal decode gambar"}), 400
        
        flower_name, confidence, error = predict_flower(img_array=frame)
        
        if error:
            return jsonify({'error': error}), 500
        
        # Save camera capture
        filename = f"camera_{int(os.times()[4] * 1000)}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cv2.imwrite(filepath, frame)
        
        return jsonify({
            "success": True,
            "filename": f"/uploads/{filename}",
            "prediction": flower_name,
            "confidence": float(confidence * 100)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
