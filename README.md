# AI Meal Planner 🍽️

Sebuah aplikasi berbasis web untuk merencanakan jadwal makan (Meal Plan). Aplikasi ini memanfaatkan pendekatan algoritma Constraint Satisfaction Problems (CSP) dan A* Search, yang dikombinasikan dengan Google Generative AI untuk menyusun resep serta jadwal makan yang optimal dan terstruktur.

Konsep Algoritma
Project ini dirancang untuk menyelesaikan masalah perencanaan makan yang kompleks dengan mengimplementasikan dua konsep utama dari Kecerdasan Buatan (AI):

1. Constraint Satisfaction Problem (CSP) : Dalam menyusun jadwal makan, ada banyak variabel dan batasan (constraints) yang harus dipenuhi agar meal plan menjadi valid dan sesuai kebutuhan pengguna. CSP diimplementasikan untuk menangani batasan-batasan tersebut. Algoritma memastikan bahwa setiap menu yang dimasukkan ke dalam jadwal (state) memenuhi seluruh kondisi (constraints).
2. A* (A-Star) Search Algorithm : A* Search digunakan sebagai mesin pencari utama untuk menemukan kombinasi menu harian yang paling optimal. Dengan kombinasi `f(n) = g(n) + h(n)`, algoritma A* dapat dengan cerdas memprioritaskan pencarian kombinasi makanan (path) yang paling mendekati target nutrisi harian dengan biaya terendah, tanpa harus mengecek semua kemungkinan kombinasi makanan (exhaustive search) yang akan memakan waktu komputasi besar.

# Cara Menjalankan Project

### 1. Konfigurasi Database
1. Nyalakan service MySQL.
2. Buat database baru bernama `meal_planner`.
3. Impor file `meal_planner (7).sql` ke dalam database tersebut.
4. Buka file `back-end/database.py` dan sesuaikan konfigurasi koneksinya (host, user, password, database).

### 2. Menjalankan Backend (Python/Flask)
Buka terminal dan arahkan ke folder `back-end`, lalu jalankan perintah berikut:
```bash
# Instalasi library yang dibutuhkan
pip install flask flask-cors mysql-connector-python google-generativeai

# Jalankan server
python app.py
```
*Catatan: Pastikan API Key Google AI sudah dimasukkan dengan benar di dalam `genai_service.py`. Server backend akan berjalan di `http://127.0.0.1:5000` sebagai penyedia API.*

### 3. Menjalankan Frontend (Vue.js)
Buka tab terminal **baru** (biarkan terminal backend tetap menyala), arahkan ke folder `frontend`, lalu jalankan:
```bash
# Instalasi dependencies Vue
npm install

# Jalankan development server
npm run dev
```

# Dokumentasi

Tampilan ini berfungsi sebagai formulir utama di mana pengguna mengisi preferensi dan batasan diet mereka agar sistem AI dapat memproses parameter tersebut dan menghasilkan rencana jadwal menu makanan beserta daftar belanjanya secara otomatis.
<img width="1897" height="868" alt="image" src="https://github.com/user-attachments/assets/9bb74422-c69e-4425-96e8-ec4a4f55f8a7" />

Hasilnya sangat dipengaruhi oleh isi dari database yang dimiliki.
<img width="1886" height="861" alt="image" src="https://github.com/user-attachments/assets/d282264a-b34e-44dc-a4fa-db03721ccd75" />
<img width="1892" height="858" alt="image" src="https://github.com/user-attachments/assets/6f0b7038-34eb-4721-8374-d5273a8ba478" />




