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

/* HERO BOX */
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
}

.hero-sub {
    font-size: 20px;
    color: #0059b3;
}

.motto {
    font-size: 18px;
    font-style: italic;
    color: #003566;
    margin-top: 10px;
}

/* BUTTON */
.button-primary {
    background-color: #4d9bf7;
    color: white !important;
    padding: 12px 18px;
    border-radius: 12px;
    font-size: 16px;
    text-decoration: none;
    display: inline-block;
}

.button-primary:hover {
    background-color: #1d7bea;
    color: white !important;
}

/* CARD STYLE */
.card-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 20px;
    margin-top: 5px;
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

.card-title {
    font-size: 18px;
    font-weight: 600;
    color: #003d80;
}

.card-price {
    font-size: 16px;
    font-weight: 600;
    color: #0066cc;
}

/* FOOTER */
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
    <img src="https://raw.githubusercontent.com/laylaahmady13-web/SmartSurvey/main/Logo%20SmartSurvey.png" width="150">
    <div class="hero-title">SmartSurvey</div>
    <div class="hero-sub">Layanan Survei & Analisis Data Digital</div>
    <div class="motto">“Kamu fokus di tugasnya, kami bereskan datanya.”</div>
    <br>
    <a class="button-primary" href="#layanan">Lihat Layanan</a>
</div>
""", unsafe_allow_html=True)


# ========================== SECTION: LAYANAN ==========================
st.markdown("<h2 id='layanan'>✨ Pilihan Layanan</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="card-container">

    <div class="card">
        <div class="card-title">Template Survei Dasar</div>
        <div class="card-price">Rp 15.000</div>
    </div>

    <div class="card">
        <div class="card-title">Template Survei Lengkap</div>
        <div class="card-price">Rp 25.000</div>
    </div>

    <div class="card">
        <div class="card-title">Uji Validitas</div>
        <div class="card-price">Rp 15.000</div>
    </div>

    <div class="card">
        <div class="card-title">Uji Reliabilitas</div>
        <div class="card-price">Rp 15.000</div>
    </div>

    <div class="card">
        <div class="card-title">Paket Hemat (Validitas + Reliabilitas)</div>
        <div class="card-price">Rp 25.000</div>
    </div>

    <div class="card">
        <div class="card-title">Analisis Dasar Premium</div>
        <div class="card-price">Rp 25.000</div>
    </div>

    <div class="card">
        <div class="card-title">Uji t / ANOVA / Chi-square</div>
        <div class="card-price">Rp 30.000</div>
    </div>

    <div class="card">
        <div class="card-title">Regresi / Korelasi / Logistik</div>
        <div class="card-price">Rp 35.000</div>
    </div>

    <div class="card">
        <div class="card-title">Paket Laporan PDF Lengkap</div>
        <div class="card-price">Rp 40.000 – Rp 60.000</div>
    </div>

</div>
""", unsafe_allow_html=True)


# ========================== ANALISIS CEPAT SECTION ==========================
st.markdown("## Analisis Cepat (Gratis)")
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
st.markdown("## Analisis Lengkap (Berbayar)")

st.write("Gunakan tombol di bawah untuk pemesanan atau konsultasi:")

colA, colB = st.columns(2)

with colA:
    st.markdown(
        f"<a class='button-primary' href='https://forms.gle/4GyXEF9xYGp78PXN7' target='_blank'>📄 Isi Form Pemesanan</a>",
        unsafe_allow_html=True,
    )

with colB:
    st.markdown(
        f"<a class='button-primary' href='https://api.whatsapp.com/send/?phone=62895604820884&text=Halo%20SmartSurvey%2C%20saya%20ingin%20konsultasi%20layanan.&type=phone_number&app_absent=0' target='_blank'>💬 Chat WhatsApp</a>",
        unsafe_allow_html=True,
    )


# ========================== FOOTER ==========================
st.markdown("""
<div class="footer">
© 2025 SmartSurvey by Layla Ahmady
</div>
""", unsafe_allow_html=True)
