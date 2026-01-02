import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os
import re

# --- KONFIGURASI API (GANTI DENGAN KEY KAMU) ---
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not TMDB_API_KEY or not GEMINI_API_KEY:
    st.error("API Key belum diset! Harap masukkan API Key di docker-compose.yml")
    st.stop()

# Konfigurasi Gemini
genai.configure(api_key=GEMINI_API_KEY)
model_gemini = genai.GenerativeModel('gemini-2.5-flash')

# --- 1. FUNGSI LOAD MODEL BI-LSTM (CUSTOM) ---
@st.cache_resource
def load_sentiment_model():
    """
    Memuat model Bi-LSTM dan Tokenizer yang sudah dilatih.
    Sesuaikan path file dengan file lokal kamu.
    """
    try:
        # Ganti 'model_bilstm.h5' dengan path model kamu
        model = tf.keras.models.load_model('model_bilstm.h5') 
        
        # Ganti 'tokenizer.pickle' dengan path tokenizer kamu
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
            
        return model, tokenizer
    except Exception as e:
        st.error(f"Gagal memuat model: {e}. Menggunakan Mode Demo (Random).")
        return None, None

# Fungsi Clean Text
def clean_text_dashboard(text):
    # Lowercase
    text = text.lower()
    # Hapus HTML
    text = re.sub(r'<br\s*/?>', ' ', text)
    # Hapus URL
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Hapus karakter non-alfabet
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # (Opsional) Stopwords removal sederhana bisa ditiadakan di inferensi 
    # jika sulit load library besar di docker, tapi idealnya ada.
    return text

# Fungsi Preprocessing & Prediksi (Sesuaikan dengan cara kamu melatih model)
def predict_sentiment(texts, model, tokenizer):
    if model is None or tokenizer is None:
        return [0] * len(texts)

    # Lakukan Preprocessing Dulu!
    cleaned_texts = [clean_text_dashboard(t) for t in texts]

    # Tokenizing
    sequences = tokenizer.texts_to_sequences(cleaned_texts)
    
    # PENTING: Ubah maxlen jadi 250 (Sesuai Training Kamu)
    padded = pad_sequences(sequences, maxlen=250, padding='post', truncating='post')
    
    # Prediksi
    predictions = model.predict(padded)
    
    results = [1 if p > 0.5 else 0 for p in predictions]
    return results

# --- 2. FUNGSI TMDB ---
def get_movie_id(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(url).json()
    if response['results']:
        return response['results'][0]['id'], response['results'][0]['title'], response['results'][0]['poster_path']
    return None, None, None

def get_tmdb_reviews(movie_id, limit=100):
    reviews = []
    page = 1
    while len(reviews) < limit:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={TMDB_API_KEY}&language=en-US&page={page}"
        data = requests.get(url).json()
        
        if 'results' not in data or not data['results']:
            break
            
        for review in data['results']:
            reviews.append(review['content'])
            if len(reviews) >= limit:
                break
        page += 1
        
        if page > data['total_pages']:
            break
            
    return reviews

# --- 3. FUNGSI GEMINI AI (KESIMPULAN) ---
def generate_summary(movie_title, reviews):
    # Menggabungkan review (dipotong agar tidak melebihi token limit)
    combined_text = " ".join(reviews)[:15000] 
    
    prompt = f"""
    Bertindaklah sebagai kritikus film. Berikut adalah kumpulan review mentah untuk film "{movie_title}".
    Tolong berikan kesimpulan singkat dan padat dalam Bahasa Indonesia.
    
    Format output:
    1. **Pujian Utama**: Apa yang disukai penonton?
    2. **Kritik Utama**: Apa yang tidak disukai?
    3. **Kesimpulan Akhir**: Satu kalimat rangkuman (misal: "Visual memukau tapi plot membosankan").
    
    Data Review:
    {combined_text}
    """
    
    response = model_gemini.generate_content(prompt)
    return response.text

# --- 4. MAIN DASHBOARD UI ---
def main():
    st.set_page_config(page_title="Dashboard Sentimen Film", layout="wide")
    
    st.title("🎬 Dashboard Analisis Sentimen Film (Bi-LSTM & Gemini)")
    st.markdown("Analisis review film menggunakan **Deep Learning** dan **Generative AI**.")

    # Sidebar Input
    with st.sidebar:
        st.header("Input Data")
        movie_title = st.text_input("Masukkan Judul Film", "Dune: Part Two")
        btn_process = st.button("Analisis Film")

    if btn_process:
        # Load Model
        model, tokenizer = load_sentiment_model()
        
        with st.spinner(f"Mencari film '{movie_title}' di TMDB..."):
            movie_id, real_title, poster = get_movie_id(movie_title)
            
        if movie_id:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if poster:
                    st.image(f"https://image.tmdb.org/t/p/w500{poster}", caption=real_title)
                st.success(f"ID Film: {movie_id}")
            
            with col2:
                # Ambil Review
                with st.spinner("Mengambil 100 review terbaru..."):
                    reviews = get_tmdb_reviews(movie_id, limit=100)
                
                if reviews:
                    st.write(f"Berhasil mengambil **{len(reviews)}** review.")
                    
                    # Prediksi Sentimen (Bi-LSTM)
                    with st.spinner("Menganalisis sentimen dengan Bi-LSTM..."):
                        sentiments = predict_sentiment(reviews, model, tokenizer)
                        df = pd.DataFrame({'review': reviews, 'sentiment': sentiments})
                        
                        # Mapping: 1 = Positif, 0 = Negatif
                        pos_count = df[df['sentiment'] == 1].shape[0]
                        neg_count = df[df['sentiment'] == 0].shape[0]
                    
                    # --- OUTPUT VISUAL: PIE CHART ---
                    st.subheader("📊 Distribusi Sentimen (Bi-LSTM)")
                    fig, ax = plt.subplots(figsize=(6, 3))
                    ax.pie([pos_count, neg_count], labels=['Positif', 'Negatif'], 
                           autopct='%1.1f%%', colors=['#66b3ff', '#ff9999'], startangle=90)
                    ax.axis('equal') 
                    st.pyplot(fig)
                    
                    st.divider()
                    
                    # --- OUTPUT TEKS: GEMINI AI ---
                    st.subheader("🤖 Kesimpulan AI (Gemini)")
                    with st.spinner("Gemini sedang membaca review..."):
                        try:
                            summary = generate_summary(real_title, reviews)
                            st.markdown(summary)
                        except Exception as e:
                            st.error(f"Gemini Error: {e}")
                    
                    # Tampilkan Sampel Data
                    with st.expander("Lihat Sampel Review Raw"):
                        st.dataframe(df.head(10))
                        
                else:
                    st.warning("Tidak ada review ditemukan untuk film ini.")
        else:
            st.error("Film tidak ditemukan di TMDB.")

if __name__ == "__main__":
    main()