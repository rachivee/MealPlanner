# file: backend/tester.py
import requests
import json

# URL API yang sudah kamu buat di app.py
url = 'http://127.0.0.1:5000/generate-menu'

# Data pura-pura (Ceritanya ini input dari user)
data_dummy = {
    "days": 1,
    "calories": 2000,
    "pantry": ["telur", "nasi"] # User punya telur dan nasi
}

print("--- MENGIRIM REQUEST KE AI ---")
try:
    # Kita kirim data ke backend (POST Request)
    response = requests.post(url, json=data_dummy)
    
    # Cek jawaban server
    if response.status_code == 200:
        print("SUKSES! AI Menjawab:")
        print(json.dumps(response.json(), indent=2))
    else:
        print("ERROR:", response.status_code)
        print(response.text)
        
except Exception as e:
    print("Gagal konek ke server. Pastikan app.py sedang jalan!")
    print(e)