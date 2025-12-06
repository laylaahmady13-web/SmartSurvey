import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========================== CONFIG ==============================
st.set_page_config(
    page_title="SmartSurvey",
    page_icon="📊",
    layout="wide"
)

# ========================== CUSTOM CSS ==========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.hero-box {
    background: linear-gradient(135deg, #dceaff 0%, #bcd8ff 100%);
    padding: 50px;
    border-radius: 25px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.hero-title {
    font-size: 48px;
    font-weight: 600;
    color: #003f7f;
    margin-bottom: 10px;
}

.hero-sub {
    font-size: 20px;
    color: #0059b3;
    margin-bottom: 25px;
}

.motto {
    font-size: 18px;
    font-style: italic;
    color: #003566;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.07);
    transition: 0.2s;
    border-left: 6px solid #4d9bf7;
}

.card:hover {
    transform: translateY(-5px);
}

.button-primary {
    background-color: #4d9bf7;
    color: white;
    padding: 12px 18px;
    border-radius: 12px;
    font-size: 16px;
    text-decoration: none;
}

.button-primary:hover {
    background-color: #1d7bea;
}

.footer {
    text-align: center;
    margin-top: 60px;
    padding: 10px;
    color: #003566;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# ========================== HERO SECTION ==========================
st.markdown("""
<div class="hero-box">
    <img src="https://raw.githubusercontent.com/laylaahmady13-web/SmartSurvey/main/Logo%20SmartSurvey.png" 
         width="150">

    <div class="hero-title">SmartSurvey</div>
    <div class="hero-sub">Layanan Survei & Analisis Data Digital</div>
    <div class="motto">“Kamu fokus di tugasnya, kami bereskan datanya.”</div>

    <a class="button-primary" href="#layanan">Lihat Layanan</a>
</div>
""", unsafe_allow_html=True)



# ========================== SECTION: LAYANAN ==========================
st.markdown("<h2 id='layanan'>✨ Pilihan Layanan</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="card">
            <h3>📊 Analisis Cepat (Gratis)</h3>
            <p>Cek data survei secara otomatis: statistik deskriptif & grafik instan.</p>
        </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
        <div class="card">
            <h3>📝 Analisis Lengkap (Berbayar)</h3>
            <p>Analisis mendalam + laporan PDF profesional, sesuai kebutuhan.</p>
        </div>
    """, unsafe_allow_html=True)

st.write("")


# ========================== ANALISIS CEPAT SECTION ==========================
st.markdown("## 📊 Analisis Cepat (Gratis)")
st.write("Upload file CSV untuk melihat visualisasi otomatis.")

upload = st.file_uploader("Upload file CSV", type=["csv"])

if upload:
    try:
        df = pd.read_csv(upload)
        st.success("File berhasil diunggah!")

        st.subheader("Pratinjau Data")
        st.dataframe(df.head())

        st.subheader("Statistik Deskriptif")
        st.dataframe(df.describe(include="all"))

        # ========================= Grafik =========================
        def plot_col(df, col):
            fig, ax = plt.subplots(figsize=(7, 4))
            if df[col].dtype == 'object' or df[col].nunique() < 20:
                sns.countplot(y=col, data=df, ax=ax)
            else:
                df[col].hist(ax=ax, bins=15)
            return fig
        
        pilih = st.selectbox("Pilih kolom untuk visualisasi", df.columns)

        if pilih:
            st.pyplot(plot_col(df, pilih))

    except Exception as e:
        st.error(f"Terjadi error: {e}")



# ========================== ANALISIS BERBAYAR SECTION ==========================
st.markdown("## 📝 Analisis Lengkap (Berbayar)")
st.write("Klik tombol di bawah untuk pemesanan:")

colA, colB = st.columns(2)

with colA:
    st.markdown(
        f"<a class='button-primary' href='https://forms.gle/4GyXEF9xYGp78PXN7' target='_blank'>📄 Isi Form Pemesanan</a>",
        unsafe_allow_html=True,
    )

with colB:
    st.markdown(
        f"<a class='button-primary' href='https://api.whatsapp.com/send/?phone=62895604820884&text=Halo%20SmartSurvey%2C%20saya%20ingin%20konsultasi%20layanan%20analisis.&type=phone_number&app_absent=0' target='_blank'>💬 Chat WhatsApp</a>",
        unsafe_allow_html=True,
    )

# ========================== FOOTER ==========================
st.markdown("""
<div class="footer">
© 2025 SmartSurvey by Layla Ahmady
</div>
""", unsafe_allow_html=True)
