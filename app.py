import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Tambahan opsional (efek confetti)
try:
    from streamlit_extras import confetti
    use_confetti = True
except ImportError:
    use_confetti = False


# ====== Fungsi Visualisasi ======
@st.cache_data
def plot_frequency(df, column):
    """Membuat Bar Chart/Histogram cerdas berdasarkan tipe data kolom."""
    fig, ax = plt.subplots(figsize=(8, 4))
    if df[column].dtype == 'object' or df[column].nunique() < 20:
        sns.countplot(y=column, data=df, order=df[column].value_counts().index, palette="viridis", ax=ax)
        ax.set_title(f"Frekuensi Jawaban: {column}", fontsize=14)
        ax.set_xlabel("Jumlah Responden")
    else:
        df[column].hist(ax=ax, bins=15, color='#b30086')
        ax.set_title(f"Distribusi Nilai: {column}", fontsize=14)
        ax.set_xlabel(column)
        ax.set_ylabel("Frekuensi")
    plt.tight_layout()
    return fig


# ====== Konfigurasi Halaman ======
st.set_page_config(page_title="SmartSurvey", page_icon="📊", layout="wide")

# ====== Styling CSS ======
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffe6f2 0%, #f7e0f7 100%);
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] * {
        color: #6a006a;
    }
    .main-title {
        text-align: center;
        color: #6a006a;
        font-size: 36px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #b30086;
        font-size: 20px;
        margin-bottom: 30px;
    }
    .price-box {
        background: linear-gradient(135deg, #f7e0f7 0%, #ffe6f2 100%);
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #b30086;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin: 10px;
        text-align: center;
    }
    .footer {
        text-align: center;
        color: #6a006a;
        font-size: 14px;
        margin-top: 40px;
        padding: 10px;
        background: #f7e0f7;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# ====== Sidebar Navigasi ======
menu = st.sidebar.radio("Menu Utama", ["Home", "Analisis Cepat (Gratis)", "Analisis Lengkap (Berbayar)"])


# ====== Halaman HOME ======
if menu == "Home":
    st.image("https://github.com/laylaahmady13-web/SmartSurvey/raw/main/Logo%20SmartSurvey.png", use_column_width=True)
    st.markdown("<div class='main-title'>SmartSurvey</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Cerdas membaca data, ringan melangkah bersama.</div>", unsafe_allow_html=True)

    st.write("""
    Selamat datang di **SmartSurvey**, platform analisis data survei otomatis!  
    Bantu mahasiswa & peneliti mengubah data mentah menjadi insight yang bermakna.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card'>
            <h3>📊 Analisis Cepat (Gratis)</h3>
            <p>Upload CSV, lihat preview data, dan buat visualisasi otomatis. Gratis & cepat!</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card'>
            <h3>💼 Analisis Lengkap (Berbayar)</h3>
            <p>Dapatkan laporan PDF profesional lengkap dengan insight & visualisasi mendalam.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("Gunakan menu di **Sidebar** untuk mulai analisis.")


# ====== Halaman GRATIS ======
elif menu == "Analisis Cepat (Gratis)":
    st.header("🎉 Analisis Cepat (Gratis)")
    st.write("Unggah file CSV Anda. **Data Anda aman dan tidak disimpan.**")

    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File berhasil diunggah!")

            tab1, tab2, tab3 = st.tabs(["🧾 Preview", "📈 Visualisasi", "🔗 Crosstab Sederhana"])
            with tab1:
                st.dataframe(df.head())
                st.write("**Statistik Deskriptif:**")
                st.dataframe(df.describe(include='all'))

            with tab2:
                skip_keywords = ["cap waktu", "timestamp", "nama", "nim", "npm", "email", "asal instansi", "usia"]
                kolom_list = [c for c in df.columns if not any(k.lower() in c.lower() for k in skip_keywords)]
                if not kolom_list:
                    kolom_list = df.columns.tolist()
                kolom_pilih = st.selectbox("Pilih variabel:", kolom_list)
                if kolom_pilih:
                    fig = plot_frequency(df, kolom_pilih)
                    st.pyplot(fig)

            with tab3:
                st.write("Pilih 2 kolom untuk tabel silang sederhana.")
                colx, coly = st.columns(2)
                with colx:
                    x = st.selectbox("Kolom X:", df.columns)
                with coly:
                    y = st.selectbox("Kolom Y:", df.columns)
                if x and y:
                    st.dataframe(pd.crosstab(df[x], df[y]))

        except Exception as e:
            st.error(f"⚠️ Gagal membaca file: {e}")

    st.info("Ingin hasil lebih lengkap? Coba **Analisis Lengkap (Berbayar)**!")


# ====== Halaman BERBAYAR ======
elif menu == "Analisis Lengkap (Berbayar)":
    st.header("💼 Analisis Lengkap (Jasa Kustom)")
    st.markdown("""
    <div class='price-box'>
        <h4>💰 Biaya: Rp 25.000 / survei</h4>
        <p><strong>Metode Pembayaran:</strong></p>
        <ul>
            <li>DANA / GoPay: 0812xxxxxxx (a.n. SmartSurvey)</li>
            <li>Bank ABC: 123456789 (a.n. Layla Ahmady)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    with st.form("berbayar_form"):
        st.subheader("📝 Formulir Pengajuan Analisis Kustom")
        file = st.file_uploader("1️⃣ Upload file CSV Anda", type=["csv"])
        email = st.text_input("2️⃣ Email untuk pengiriman hasil (wajib):")
        deskripsi = st.text_area("3️⃣ Jelaskan kebutuhan analisis Anda:")
        bukti = st.file_uploader("4️⃣ Upload bukti pembayaran:", type=["jpg", "png", "pdf"])
        submit = st.form_submit_button("Kirim Pengajuan 📤")

    if submit:
        if file and email and deskripsi and bukti:
            st.success(f"🎉 Pengajuan berhasil! Laporan akan dikirim ke {email} dalam 1x24 jam.")
            if use_confetti:
                confetti.confetti()
            else:
                st.balloons()
        else:
            st.error("⚠️ Harap lengkapi semua kolom sebelum mengirim.")


# ====== FOOTER ======
st.markdown("""
    <div class='footer'>
        © 2025 <b>SmartSurvey by Laylaa</b> — "Cerdas membaca data, ringan melangkah bersama."
    </div>
""", unsafe_allow_html=True)
