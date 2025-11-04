import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_extras import confetti  # install dulu: pip install streamlit-extras

# ====== Konfigurasi Halaman ======
st.set_page_config(page_title="SmartSurvey", page_icon="📊", layout="wide")

# ====== Fungsi Visualisasi ======
@st.cache_data
def plot_frequency(df, column):
    fig, ax = plt.subplots(figsize=(8, 4))
    if df[column].dtype == 'object' or df[column].nunique() < 20:
        sns.countplot(y=column, data=df,
                      order=df[column].value_counts().index,
                      palette="crest", ax=ax)
        ax.set_title(f"Frekuensi Jawaban: {column}", fontsize=14)
        ax.set_xlabel("Jumlah Responden")
        ax.set_ylabel("")
    else:
        df[column].hist(ax=ax, bins=15, color='#007BBD')
        ax.set_title(f"Distribusi Nilai: {column}", fontsize=14)
        ax.set_xlabel(column)
        ax.set_ylabel("Frekuensi")
    plt.tight_layout()
    return fig

# ====== CSS Tema Soft Blue ======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

body {
    font-family: 'Poppins', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e6f0ff 0%, #f3f8ff 100%);
    box-shadow: 2px 0 10px rgba(0,0,0,0.05);
}
[data-testid="stSidebar"] * {
    color: #004c7f;
}
.header {
    background: linear-gradient(90deg, #c9e6ff 0%, #dbeaff 100%);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 25px;
}
.header h1 {
    color: #004c7f;
    font-size: 40px;
    font-weight: 700;
    margin-bottom: 5px;
}
.header p {
    color: #007BBD;
    font-size: 18px;
    margin-top: 0;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    margin: 10px;
    text-align: center;
}
.price-box {
    background: linear-gradient(135deg, #e8f3ff 0%, #dbeaff 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #007BBD;
    margin-bottom: 20px;
}
.footer {
    text-align: center;
    color: #004c7f;
    font-size: 14px;
    margin-top: 40px;
    padding: 10px;
    background: #e6f0ff;
    border-radius: 10px;
}
a {
    color: #007BBD;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ====== Sidebar ======
menu = st.sidebar.radio("Menu Utama", ["Home", "Analisis Cepat (Gratis)", "Analisis Lengkap (Berbayar)"])

# ====== Halaman HOME ======
if menu == "Home":
    st.markdown("""
    <div class='header'>
        <h1>📊 SmartSurvey</h1>
        <p>Analisis Survei Otomatis — Cepat, Mudah, dan Profesional</p>
    </div>
    """, unsafe_allow_html=True)

    st.image("https://raw.githubusercontent.com/laylaahmady13-web/SmartSurvey/main/Logo%20SmartSurvey.png", width=220)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card'>
            <h3>Analisis Cepat (Gratis)</h3>
            <p>Upload CSV kamu, lihat hasil analisis deskriptif dan grafik otomatis.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card'>
            <h3>Analisis Lengkap (Berbayar)</h3>
            <p>Jasa analisis kustom Rp25.000 — laporan lengkap dikirim via email.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("Gunakan menu di Sidebar untuk memulai analisis data survei kamu.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("📩 Hubungi kami di [Instagram @smart.survey1](https://www.instagram.com/smart.survey1) untuk informasi lebih lanjut.")

# ====== Halaman GRATIS ======
elif menu == "Analisis Cepat (Gratis)":
    st.header("Analisis Cepat (Gratis)")
    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File berhasil diunggah!")
            tab1, tab2, tab3 = st.tabs(["🧾 Preview Data", "📈 Visualisasi", "🔗 Crosstab Sederhana"])

            with tab1:
                st.dataframe(df.head())
                st.write("Statistik deskriptif:")
                st.dataframe(df.describe(include='all'))
            with tab2:
                kolom_pilih = st.selectbox("Pilih kolom untuk visualisasi:", df.columns)
                fig = plot_frequency(df, kolom_pilih)
                st.pyplot(fig)
            with tab3:
                col1, col2 = st.columns(2)
                with col1:
                    col_x = st.selectbox("Kolom X:", df.columns)
                with col2:
                    col_y = st.selectbox("Kolom Y:", df.columns)
                st.dataframe(pd.crosstab(df[col_x], df[col_y]))
        except Exception as e:
            st.error(f"⚠️ Terjadi kesalahan: {e}")

# ====== Halaman BERBAYAR ======
elif menu == "Analisis Lengkap (Berbayar)":
    st.header("Analisis Lengkap (Berbayar)")
    st.markdown("""
        <div class='price-box'>
            <h4>💰 Biaya: Rp 25.000 per survei</h4>
            <p>Untuk konfirmasi pembayaran dan pemesanan layanan, hubungi kami di:</p>
            <p><a href='https://www.instagram.com/smart.survey1' target='_blank'>📩 Instagram @smart.survey1</a></p>
        </div>
    """, unsafe_allow_html=True)

    with st.form(key='form_pesan'):
        st.subheader("Form Pengajuan Analisis")
        uploaded_file = st.file_uploader("1️⃣ Upload File CSV", type=["csv"])
        email = st.text_input("2️⃣ Email (untuk pengiriman hasil)")
        deskripsi = st.text_area("3️⃣ Kebutuhan Analisis (jelaskan data dan tujuan)")
        bukti = st.file_uploader("4️⃣ Bukti Pembayaran (opsional, upload setelah konfirmasi IG)")

        kirim = st.form_submit_button("Kirim Pengajuan 📤")

        if kirim:
            if uploaded_file and email and deskripsi:
                st.success(f"🎉 Pengajuan berhasil! Hasil akan dikirim ke **{email}** setelah konfirmasi di Instagram.")
                confetti.confetti()
            else:
                st.warning("⚠️ Mohon lengkapi data sebelum mengirim.")

# ====== FOOTER ======
st.markdown("""
<div class='footer'>
© 2025 <b>SmartSurvey by Layla Ahmady</b> | <a href='https://www.instagram.com/smart.survey1?igsh=MWY0MHRrNzNqcDh6dw==' target='_blank'>@smart.survey1</a>
</div>
""", unsafe_allow_html=True)
