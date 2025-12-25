# ============================================================
# Isi khusus testing & prediksi interaktif
# ============================================================

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
import tkinter as tk
from tkinter import filedialog

# Pastikan predict_flower mengambil model sebagai argumen
from model_utils import predict_flower, cat_to_name 

# Nama file model
MODEL_FILE = 'flower_classification_model_MobileNetV2.keras'
BASE_DIR = "../dataset"
TRAIN_DIR = os.path.join(BASE_DIR, "train")

# ====== LOAD KELAS & MODEL (Dilakukan sekali) ======
try:
    # 1. Load Kelas
    class_names = {i: folder for i, folder in enumerate(sorted(os.listdir(TRAIN_DIR)))
                   if os.path.isdir(os.path.join(TRAIN_DIR, folder))}

    # 2. Load Model Keras (PENTING: Pemuatan model hanya dilakukan sekali di awal)
    model = tf.keras.models.load_model(MODEL_FILE)
    print(f"✅ Model '{MODEL_FILE}' berhasil dimuat.")

except FileNotFoundError:
    print(f"❌ Error: Direktori atau file model tidak ditemukan: {TRAIN_DIR} atau {MODEL_FILE}")
    model = None # Set model ke None jika gagal

# ====== TEST FUNCTIONS ======

def test_with_image_file(model_obj):
    """Memprediksi bunga dari file gambar yang dipilih melalui dialog."""
    if model_obj is None: return

    root = tk.Tk(); root.withdraw()
    file_path = filedialog.askopenfilename(title="Pilih gambar bunga",
                                           filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        # Panggil predict_flower dengan objek model yang sudah dimuat
        flower_name, confidence, _, class_num = predict_flower(model_obj, 
                                                               cat_to_name, class_names,
                                                               img_path=file_path)
        img = Image.open(file_path)
        plt.imshow(img)
        plt.title(f' {flower_name}\nConf: {confidence:.4f}')
        plt.axis('off')
        plt.show()
        print(f"📸 {flower_name} ({class_num}) - {confidence:.4f}")

def test_with_camera(model_obj):
    """Memprediksi bunga menggunakan input dari kamera (real-time/capture)."""
    if model_obj is None: return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Gagal membuka kamera.")
        return
        
    print("📷 Tekan 'c' untuk capture, 'q' untuk keluar")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal mengambil frame.")
            break
            
        cv2.imshow('Camera', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('c'):
            # Panggil predict_flower dengan objek model yang sudah dimuat
            flower_name, confidence, _, class_num = predict_flower(model_obj, 
                                                                   cat_to_name, class_names,
                                                                   img_array=frame)
            print(f"🔍 {flower_name} ({class_num}) - {confidence:.4f}")
            
    cap.release(); cv2.destroyAllWindows()

def test_with_test_folder(model_obj):
    """Memprediksi bunga dari semua gambar dalam folder test."""
    if model_obj is None: return
    
    test_dir = os.path.join(BASE_DIR, "../folder_test")
    if not os.path.exists(test_dir):
        print("❌ Folder test tidak ditemukan!")
        return
        
    for img_name in os.listdir(test_dir):
        if img_name.lower().endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(test_dir, img_name)
            # Panggil predict_flower dengan objek model yang sudah dimuat
            flower_name, confidence, _, class_num = predict_flower(model_obj, 
                                                                   cat_to_name, class_names,
                                                                   img_path=img_path)
            print(f"📊 {img_name}: {flower_name} ({class_num}) - {confidence:.4f}")

def search_flower_by_name():
    """Mencari nama bunga yang cocok dalam dictionary cat_to_name."""
    try:
        term = input("Masukkan nama bunga: ").lower()
        # Menggunakan .items() untuk efisiensi
        found = [(c, n) for c, n in cat_to_name.items() if term in n.lower()]
        if found:
            for c, n in found:
                print(f"✅ {c}: {n}")
        else:
            print("❌ Tidak ditemukan.")
    except NameError:
        print("❌ Variabel 'cat_to_name' tidak terdefinisi. Pastikan 'model_utils' sudah benar.")

# ====== MENU UTAMA ======
def main_menu():
    global model
    if model is None:
        print("\n🚫 Sistem Klasifikasi tidak bisa berjalan karena model gagal dimuat.")
        return

    while True:
        print("\n🌺 FLOWER CLASSIFICATION SYSTEM")
        print("1. Test dengan gambar file")
        print("2. Test dengan kamera")
        print("3. Test dengan folder test")
        print("4. Cari bunga berdasarkan nama")
        print("5. Keluar")

        choice = input("Pilih opsi (1–5): ").strip()
        
        # Panggil fungsi dengan meneruskan objek model
        if choice == '1': test_with_image_file(model)
        elif choice == '2': test_with_camera(model)
        elif choice == '3': test_with_test_folder(model)
        elif choice == '4': search_flower_by_name()
        elif choice == '5': break
        else: print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    main_menu()