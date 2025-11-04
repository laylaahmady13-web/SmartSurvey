import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# ====== Fungsi Visualisasi ======
@st.cache_data
def plot_frequency(df, column):
    """Membuat Bar Chart/Histogram berdasarkan tipe data kolom."""
    fig, ax = plt.subplots(figsize=(8, 4))
    if df[column].dtype == 'object' or df[column].nunique() < 20:
        sns.countplot(y=column, data=df,
                      order=df[column].value_counts().index,
                      palette="Blues", ax=ax)
        ax.set_title(f"Frekuensi Jawaban: {column}", fontsize=14)
        ax.set_xlabel("Jumlah Responden")
        ax.set_ylabel("")
    else:
        df[column].hist(ax=ax, bins=15, color='#007acc')
        ax.set_title(f"Distribusi Nilai: {column}", fontsize=14)
        ax.set_xlabel(column)
        ax.set_ylabel("Frekuensi")
    plt.tight_layout()
    return fig

# ====== Konfigurasi Halaman ======
st.set_page_config(page_title="SmartSurvey", page_icon="📊", layout="wide")

# ====== Gaya CSS (Soft Blue Tema Profesional) ======
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&display=swap');
    body { font-family: 'Poppins', sans-serif; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e6f0ff 0%, #f0f6ff 100%);
        box-shadow: 2px 0 10px rgba(0,0,0,0.05);
    }
    [data-testid="stSidebar"] * {
        color: #003366;
    }

    .main-title {
        text-align: center;
        color: #004080;
        font-size: 36px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #007acc;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .price-box {
        background: linear-gradient(135deg, #e6f2ff 0%, #cce6ff 100%);
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #007acc;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .footer {
        text-align: center;
        color: #004080;
        font-size: 14px;
        margin-top: 40px;
        padding: 10px;
        background: #e6f0ff;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ====== Sidebar ======
menu = st.sidebar.radio("Menu Utama", ["Home", "Analisis Cepat (Gratis)", "Analisis Lengkap (Berbayar)"])

# ====== HOME ======
if menu == "Home":
    st.image("https://raw.githubusercontent.com/laylaahmady13-web/SmartSurvey/main/Logo%20SmartSurvey.png", width=230)
    st.markdown("<div class='main-title'>SmartSurvey</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Analisis survei otomatis — cepat, mudah, dan profesional</div>", unsafe_allow_html=True)

    st.write("""
    Selamat datang di **SmartSurvey**  
    Platform analisis survei yang membantu mahasiswa, peneliti muda, dan pelaku usaha memahami data dengan cepat dan efisien.

    Pilih layanan sesuai kebutuhan Anda 👇
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background-color:white; padding:20px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.1); text-align:center;'>
        <h3>Analisis Cepat (Gratis)</h3>
        <p>Upload data survei Anda dan lihat ringkasan serta visualisasi otomatis secara instan.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color:white; padding:20px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.1); text-align:center;'>
        <h3>Analisis Lengkap (Berbayar)</h3>
        <p>Analisis kustom mendalam + laporan PDF profesional.  
        Cocok untuk tugas, proyek, dan penelitian.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("Gunakan menu di **Sidebar kiri** untuk memulai analisis.")

# ====== ANALISIS CEPAT ======
elif menu == "Analisis Cepat (Gratis)":
    st.header("Analisis Cepat (Gratis)")
    st.write("Unggah file CSV Anda untuk melihat hasil analisis otomatis. **Data Anda tidak akan disimpan.**")

    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File berhasil diunggah!")

            with st.expander("🧾 Pratinjau Data", expanded=True):
                st.write("5 Baris Pertama:")
                st.dataframe(df.head())
                st.write("Statistik Deskriptif:")
                st.dataframe(df.describe(include='all'))

            st.write("### 📈 Visualisasi Frekuensi")
            skip_keywords = ["cap waktu", "timestamp", "nama", "nim", "npm", "email", "asal instansi"]
            kolom_list = [c for c in df.columns if not any(k.lower() in c.lower() for k in skip_keywords)]
            kolom_pilih = st.selectbox("Pilih kolom:", kolom_list)
            if kolom_pilih:
                fig = plot_frequency(df, kolom_pilih)
                st.pyplot(fig)

        except Exception as e:
            st.error(f"⚠️ Terjadi error saat membaca file: {e}")

    st.info("Butuh analisis lengkap dan laporan PDF? Pilih **Analisis Lengkap (Berbayar)** di sidebar.")

# ====== ANALISIS LENGKAP ======
elif menu == "Analisis Lengkap (Berbayar)":
    st.header("Analisis Lengkap (Jasa Kustom)")
    st.write("Layanan analisis mendalam dengan hasil laporan PDF profesional. Konfirmasi pembayaran dilakukan via Instagram kami.")

    st.markdown("""
        <div class='price-box'>
            <h4>💰 Biaya Layanan: Rp 25.000 / Survei</h4>
            <p>Untuk konfirmasi pembayaran, silakan hubungi kami melalui Instagram:</p>
            <p><a href="https://www.instagram.com/smart.survey1?igsh=MWY0MHRrNzNqcDh6dw==" target="_blank">@smart.survey1</a></p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form(key='form_premium'):
        st.subheader("📝 Form Pengajuan Analisis")
        uploaded_file = st.file_uploader("1️⃣ Upload file CSV Anda", type=["csv"])
        email_user = st.text_input("2️⃣ Email untuk hasil laporan")
        kebutuhan = st.text_area("3️⃣ Jelaskan kebutuhan analisis Anda")
        bukti = st.file_uploader("4️⃣ Upload bukti transfer (opsional)", type=["jpg", "png", "pdf"])
        submit = st.form_submit_button("Kirim Pengajuan")

    if submit:
        if email_user and kebutuhan and uploaded_file:
            st.success(f"✅ Pengajuan berhasil dikirim! Hasil akan dikirim ke {email_user} dalam 1x24 jam.")
        else:
            st.error("⚠️ Lengkapi semua kolom terlebih dahulu.")

# ====== FOOTER ======
st.markdown("""
    <div class='footer'>
        © 2025 <b>SmartSurvey by Layla Ahmady</b> | Konfirmasi via <a href='https://www.instagram.com/smart.survey1?igsh=MWY0MHRrNzNqcDh6dw==' target='_blank'>@smart.survey1</a>
    </div>
""", unsafe_allow_html=True)
