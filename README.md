# 🎬 Movie Sentiment Dashboard (Bi-LSTM + Gemini AI)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Bi--LSTM-orange)

Dashboard interaktif untuk menganalisis sentimen ulasan film secara *real-time*. Aplikasi ini mengambil ulasan terbaru dari **TMDB**, memprediksi sentimen (Positif/Negatif) menggunakan model Deep Learning **Bi-LSTM**, dan memberikan ringkasan kritik cerdas menggunakan **Google Gemini AI**.

## ✨ Fitur Utama
* **Pencarian Film Real-time**: Terintegrasi dengan TMDB API.
* **Deep Learning Sentiment Analysis**: Menggunakan model Bi-LSTM custom untuk mengklasifikasikan review.
* **AI Summary**: Menggunakan **Gemini 1.5 Flash** untuk merangkum poin kritik dan pujian dari ratusan review.
* **Visualisasi Data**: Menampilkan grafik Pie Chart perbandingan sentimen.
* **Containerized**: Siap dijalankan di mana saja menggunakan Docker.

## 🛠️ Teknologi
* **Frontend**: Streamlit
* **AI/ML**: TensorFlow (Keras), Google Generative AI (Gemini)
* **Data Source**: The Movie Database (TMDB) API
* **Deployment**: Docker & Docker Compose

## 📂 Struktur Proyek
Pastikan struktur folder Anda terlihat seperti ini sebelum menjalankan aplikasi:

```text
.
├── app.py                # Kode utama aplikasi Streamlit
├── Dockerfile            # Konfigurasi Docker Image
├── docker-compose.yml    # Konfigurasi Container Orchestration
├── requirements.txt      # Daftar library Python
├── .env                  # File konfigurasi API Key (JANGAN DI-COMMIT)
├── model_bilstm.h5       # Model hasil training (Wajib ada)
└── tokenizer.pickle      # Tokenizer hasil training (Wajib ada)

```

## 🚀 Cara Menjalankan dengan Docker (Recommended)

Pastikan Anda sudah menginstall **Docker** dan **Docker Compose** di komputer Anda.

### 1. Clone Repository

```bash
git clone [https://github.com/username-anda/nama-repo.git](https://github.com/username-anda/nama-repo.git)
cd nama-repo

```

### 2. Siapkan File Model

Karena ukuran file model biasanya besar, pastikan Anda telah meletakkan file hasil training Anda di root folder proyek:

* `model_bilstm.h5`
* `tokenizer.pickle`

> **Catatan:** Jika Anda belum memiliki file ini, jalankan script training model terlebih dahulu.

### 3. Konfigurasi API Key

Buat file bernama `.env` di dalam folder proyek, lalu isi dengan API Key Anda:

```ini
TMDB_API_KEY=masukkan_key_tmdb_anda_disini
GEMINI_API_KEY=masukkan_key_google_gemini_anda_disini

```

### 4. Jalankan Aplikasi

Jalankan perintah berikut di terminal:

```bash
docker-compose up --build

```

Tunggu hingga proses build selesai. Setelah muncul pesan sukses, buka browser dan akses:

👉 **http://localhost:8501**

### 5. Menghentikan Aplikasi

Untuk mematikan server, tekan `Ctrl+C` di terminal atau jalankan:

```bash
docker-compose down

```

## ⚠️ Troubleshooting

**Q: Error `models/gemini-pro is not found**`
A: Pastikan di `app.py` Anda menggunakan model `gemini-1.5-flash` atau model terbaru yang didukung oleh Google AI Studio.

**Q: Error `FileNotFoundError: tokenizer.pickle**`
A: Docker container tidak dapat menemukan file model. Pastikan file `.h5` dan `.pickle` ada di folder yang sama dengan `Dockerfile` sebelum Anda melakukan build.

**Q: Bagaimana cara mendapatkan API Key?**

* **TMDB**: Daftar di [TheMovieDB.org](https://www.themoviedb.org/documentation/api).
* **Gemini**: Dapatkan di [Google AI Studio](https://aistudio.google.com/).

## 🤝 Kontribusi

Pull request dipersilakan. Untuk perubahan besar, harap buka issue terlebih dahulu untuk mendiskusikan apa yang ingin Anda ubah.

## 📝 Lisensi

[MIT](https://choosealicense.com/licenses/mit/)

```

***

### Tips Tambahan untuk GitHub:

Jangan lupa membuat file **`.gitignore`** agar file sensitif (API Key) dan file sampah tidak ikut ter-upload ke GitHub.

Buat file `.gitignore` dan isi dengan:
```text
# Environment Variables (PENTING: Jangan upload API Key!)
.env

# Python Cache
__pycache__/
*.pyc

# Virtual Environment
venv/
.venv/

# IDE settings
.vscode/
.idea/

# (Opsional) Jika file model terlalu besar (>100MB), GitHub akan menolaknya.
# Jika ingin upload model, gunakan Git LFS atau jangan masukkan ke gitignore.
# model_bilstm.h5

```