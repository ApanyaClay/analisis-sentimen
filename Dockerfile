# Gunakan Python 3.12 versi slim (lebih ringan)
FROM python:3.12-slim-bookworm

# Set working directory di dalam container
WORKDIR /app

# Install dependency sistem yang mungkin dibutuhkan oleh matplotlib/opencv
# (Opsional, tapi sering dibutuhkan untuk library visualisasi di versi slim)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Salin requirements terlebih dahulu (agar cache docker optimal)
COPY requirements.txt .

# Install library Python
# --no-cache-dir digunakan untuk menjaga ukuran image tetap kecil
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode dan model ke dalam container
COPY . .

# Expose port default Streamlit
EXPOSE 8501

# Healthcheck untuk memastikan container berjalan lancar
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Perintah untuk menjalankan aplikasi
# server.address=0.0.0.0 PENTING agar bisa diakses dari luar container
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]