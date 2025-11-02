import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
        - Lihat distribusi jawaban tiap pertanyaan  
        - Cocok untuk uji coba cepat
        """)

    with col2:
        st.subheader("Analisis Lengkap (Berbayar)")
        st.write("""
        - Upload file & beri keterangan analisis  
        - Hasil lengkap dikirim ke email (visualisasi + laporan profesional)  
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

        st.write("### 📊 Statistik Deskriptif")
        try:
            st.dataframe(df.describe(include='all'))
        except Exception:
            st.warning("Tidak dapat menampilkan statistik karena format data tidak sesuai.")

        # --- Pilih kolom untuk visualisasi ---
        st.write("### 🎨 Visualisasi Frekuensi")
        skip_keywords = ["cap waktu", "timestamp", "nama", "nim", "npm", "email", "usia"]
        kolom_list = [c for c in df.columns if not any(k.lower() in c.lower() for k in skip_keywords)]

        if not kolom_list:
            kolom_list = df.columns.tolist()

        kolom_pilih = st.selectbox("Pilih satu variabel untuk divisualisasikan:", kolom_list)

        if kolom_pilih:
            fig, ax = plt.subplots(figsize=(8, 4))
            if df[kolom_pilih].dtype == 'object' or df[kolom_pilih].nunique() < 20:
                sns.countplot(y=kolom_pilih, data=df, order=df[kolom_pilih].value_counts().index, palette="viridis", ax=ax)
                ax.set_title(f"Frekuensi Jawaban: {kolom_pilih}")
            else:
                df[kolom_pilih].hist(ax=ax, bins=15, color='#b30086')
                ax.set_title(f"Distribusi Nilai: {kolom_pilih}")
            st.pyplot(fig)

        st.info("💡 Untuk analisis mendalam (crosstab, insight lanjutan, laporan PDF), gunakan menu **Analisis Lengkap (Berbayar)**.")

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
