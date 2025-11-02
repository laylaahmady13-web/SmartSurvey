import streamlit as st
import pandas as pd
import numpy as np

# ====== Tampilan Dasar ======
st.set_page_config(page_title="SmartSurvey", page_icon="📊", layout="centered")

# ====== Gaya CSS ======
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #ffe6f2; /* pink lembut */
    }
    [data-testid="stSidebar"] * {
        color: #6a006a; /* teks ungu tua */
    }
    .main-title {
        text-align: center;
        color: #6a006a;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #b30086;
        font-size: 18px;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ====== Sidebar ======
menu = st.sidebar.radio("Menu Utama", ["Home", "Analisis Cepat (Gratis)", "Analisis Lengkap (Berbayar)"])

# ====== Halaman HOME ======
if menu == "Home":
    st.markdown("<div class='main-title'>SmartSurvey</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Analisis survei otomatis — cepat, mudah, dan profesional</div>", unsafe_allow_html=True)

    st.write("""
    Selamat datang di **SmartSurvey**, platform analisis data survei berbasis web.  
    Kami membantu mahasiswa, peneliti, dan pelaku bisnis mendapatkan insight data tanpa harus jago statistik!

    ### Pilih layanan sesuai kebutuhanmu:
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Analisis Cepat (Gratis)")
        st.write("""
        - Upload file CSV kamu  
        - Dapatkan analisis deskriptif & korelasi sederhana langsung di halaman  
        - Cocok untuk uji coba cepat
        """)

    with col2:
        st.subheader("Analisis Lengkap (Berbayar)")
        st.write("""
        - Upload file dan beri keterangan analisis  
        - Hasil lengkap dikirim ke email (dengan visualisasi & laporan profesional)  
        - Termasuk konsultasi hasil
        """)

    st.markdown("---")
    st.write("📊 **SmartSurvey – Data Anda, Insight Kami.**")

# ====== Halaman GRATIS ======
elif menu == "Analisis Cepat (Gratis)":
    st.header("Analisis Cepat (Gratis)")
    st.write("Unggah file CSV Anda untuk melihat hasil analisis otomatis secara langsung.")

    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File berhasil diunggah!")
        st.write("### 🧾 5 Baris Pertama Data")
        st.dataframe(df.head())

        # Analisis sederhana
        st.write("### 📊 Statistik Deskriptif")
        st.dataframe(df.describe(include='all'))

        # Korelasi numerik
        num_df = df.select_dtypes(include=[np.number])
        if not num_df.empty:
            st.write("### 🔗 Korelasi antar variabel numerik")
            st.dataframe(num_df.corr())
        else:
            st.info("Tidak ada kolom numerik untuk dihitung korelasinya.")

# ====== Halaman BERBAYAR ======
elif menu == "Analisis Lengkap (Berbayar)":
    st.header("Analisis Lengkap (Berbayar)")
    st.write("Isi form berikut untuk pengajuan analisis lengkap.")

    uploaded_file = st.file_uploader("Upload file CSV Anda", type=["csv"])
    deskripsi = st.text_area("Deskripsikan analisis yang diinginkan", placeholder="Misal: analisis hubungan antara pola makan dan tingkat stres mahasiswa.")
    email = st.text_input("Masukkan email Anda untuk pengiriman hasil")
    bukti_bayar = st.file_uploader("Upload bukti pembayaran (jpg/png/pdf)", type=["jpg", "png", "pdf"])

    if st.button("Kirim Pengajuan"):
        if uploaded_file and deskripsi and email and bukti_bayar:
            st.success("✅ Pengajuan berhasil dikirim! Hasil akan dikirim ke email dalam 1x24 jam.")
        else:
            st.warning("⚠️ Mohon lengkapi semua kolom sebelum mengirim.")

