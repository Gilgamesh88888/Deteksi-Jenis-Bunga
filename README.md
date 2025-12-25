# FlowerAI - Sistem Klasifikasi Bunga Cerdas

Website native Flask untuk klasifikasi bunga menggunakan Deep Learning.

## Fitur Utama
- Upload gambar untuk prediksi
- Kamera real-time untuk capture langsung
- Analisis kepercayaan prediksi
- Pencarian bunga dari database 102 jenis bunga
- UI yang responsif dan modern

## Setup & Installation

1. **Clone repository**
```bash
git clone <your-repo>
cd Deteksi-Jenis-Bunga
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Struktur folder**
Pastikan struktur folder seperti ini:
```
flowerai/
├── app.py
├── requirements.txt
├── model/
│   ├── flower_classification_model_MobileNetV2.keras
│   └── cat_to_name.json
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── uploads/
```

4. **Jalankan aplikasi**
```bash
python app.py
```

Buka browser dan akses: `http://localhost:5000`

## Model

Model menggunakan arsitektur **MobileNetV2** yang telah dilatih dengan dataset 102 jenis bunga.

### Cara training (jika perlu):
```python
from model.model_utils import create_flower_model
model = create_flower_model(num_classes=102)
# Training code...
model.save('model/flower_classification_model_MobileNetV2.keras')
```

## API Endpoints

- `GET /` - Home page
- `POST /predict` - Prediksi dari upload gambar
  - Parameter: `file` (image)
  - Response: `{success, filename, prediction, confidence}`
- `POST /camera_predict` - Prediksi dari kamera
  - Parameter: `image` (blob)
  - Response: `{success, filename, prediction, confidence}`

## Deployment

### Ke Vercel (dengan serverless function):
1. Ubah app.py menjadi serverless handler
2. Gunakan environment variables untuk path model

### Ke PythonAnywhere:
1. Upload files ke server
2. Configure WSGI
3. Set environment variables untuk model path

### Ke Heroku:
```bash
heroku create flowerai
git push heroku main
```

## Teknologi
- Frontend: HTML, CSS, JavaScript
- Backend: Flask
- ML: TensorFlow, MobileNetV2
- Image Processing: PIL, OpenCV

## License
MIT License
