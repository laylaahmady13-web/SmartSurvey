import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io 

# ====== Konfigurasi Halaman & Cache Data ======

# Menggunakan cache agar fungsi visualisasi tidak di-run berulang kali, menghemat resource.
@st.cache_data
def plot_frequency(df, column):
    """Membuat Bar Chart/Histogram yang cerdas berdasarkan tipe data kolom."""
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Deteksi data kategorikal (string atau uniknya sedikit)
    # Jika tipe data string ATAU jumlah nilai unik kurang dari 20 (asumsi data survei)
    if df[column].dtype == 'object' or df[column].nunique() < 20:
        # Gunakan countplot untuk data kategori survei (SS, S, dll.)
        sns.countplot(y=column, data=df, 
                      order=df[column].value_counts().index, # Urutkan dari yang terbanyak
                      palette="viridis", ax=ax)
        ax.set_title(f"Frekuensi Jawaban: {column}", fontsize=14)
        ax.set_xlabel("Jumlah Responden")
        ax.set_ylabel("") 
        
    else:
        # Gunakan histogram untuk data numerik (usia, skor, dll.)
        df[column].hist(ax=ax, bins=15, color='#b30086')
        ax.set_title(f"Distribusi Nilai: {column}", fontsize=14)
        ax.set_xlabel(column)
        ax.set_ylabel("Frekuensi")
        
    plt.tight_layout()
    return fig

# Konfigurasi halaman
st.set_page_config(page_title="SmartSurvey", page_icon="📊", layout="centered")

# ====== Gaya CSS ======
st.markdown("""
    <style>
    /* Styling Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffe6f2; /* pink lembut */
    }
    [data-testid="stSidebar"] * {
        color: #6a006a; /* teks ungu tua */
    }
    
    /* Styling Header Utama */
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
    
    /* Styling Info Box untuk Harga */
    .price-box {
        background-color: #f7e0f7; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #b30086;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ====== Sidebar Navigasi Utama ======
# Ini adalah kontrol navigasi yang reliable
menu = st.sidebar.radio("Menu Utama", ["Home", "Analisis Cepat (Gratis)", "Analisis Lengkap (Berbayar)"])

# ====== Halaman HOME ======
if menu == "Home":
    st.markdown("<div style='text-align: center;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>SmartSurvey</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Analisis survei otomatis — cepat, mudah, dan profesional</div>", unsafe_allow_html=True)

    st.write("""
    Selamat datang di **SmartSurvey**! Platform yang membantu Anda mengubah data survei mentah menjadi *insight* yang berharga. 
    
    **Silakan pilih layanan di Sidebar:**
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Analisis Cepat (Gratis)")
        st.write("""
        - Upload file CSV Anda dan lihat analisis deskriptif.  
        - Visualisasi 1 variabel pilihan Anda.  
        - **Coba dulu sebelum bayar!**
        """)

    with col2:
        st.subheader("Analisis Lengkap (Berbayar)")
        st.write("""
        - **Jasa Analisis Kustom** (Rp25.000).  
        - Hasil lengkap dikirim via email (*crosstab* mendalam, *insight*, & **Laporan PDF**).  
        - Cocok untuk skripsi atau laporan formal.
        """)

    st.markdown("---")
    st.info("Gunakan tombol di **Sidebar** di sebelah kiri untuk berpindah menu dan memulai analisis.")
    
# ====== Halaman GRATIS (Analisis Cepat) ======
elif menu == "Analisis Cepat (Gratis)":
    st.header("Analisis Cepat (Gratis)")
    st.write("Unggah file CSV Anda untuk melihat hasil analisis otomatis secara langsung. **Tidak ada data yang kami simpan.**")

    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file:
        try:
            # Karena ini mode cepat, hanya import library berat di sini
            import matplotlib.pyplot as plt
            import seaborn as sns 
            
            df = pd.read_csv(uploaded_file)
            st.success("✅ File berhasil diunggah!")
            
            # --- Pratinjau Data ---
            with st.expander("🧾 Pratinjau Data & Statistik", expanded=True):
                st.write("5 Baris Pertama Data")
                st.dataframe(df.head())

                st.write("Statistik Deskriptif")
                st.dataframe(df.describe(include='all'))

            # --- Visualisasi Otomatis ---
            st.write("### 🎨 Visualisasi Frekuensi Dasar")
            
            # Filter kolom yang mungkin tidak relevan (Cap Waktu, ID, Email)
            skip_keywords = ["cap waktu", "timestamp", "nama", "nim", "npm", "email", "asal instansi", "usia"]
            kolom_list = [c for c in df.columns if not any(k.lower() in c.lower() for k in skip_keywords)]
            
            if not kolom_list:
                kolom_list = df.columns.tolist()

            kolom_pilih = st.selectbox("Pilih satu variabel untuk divisualisasikan:", kolom_list)

            if kolom_pilih:
                fig = plot_frequency(df, kolom_pilih)
                st.pyplot(fig)
        
        except Exception as e:
            st.error(f"⚠️ Terjadi error saat membaca file. Pastikan file adalah CSV dan formatnya valid. Error: {e}")

        st.markdown("---")
        st.info("Butuh analisis mendalam (crosstab, insight, laporan PDF)? Pilih **Analisis Lengkap (Berbayar)** di Sidebar.")

# ====== Halaman BERBAYAR (Jasa Kustom) ======
elif menu == "Analisis Lengkap (Berbayar)":
    st.header("Analisis Lengkap (Jasa Kustom)")
    st.write("Layanan analisis data survei mendalam. Anda berikan instruksi, kami berikan Laporan PDF profesional.")

    # --- Informasi Harga dan Cara Bayar (Wajib Jelas) ---
    st.markdown(f"""
        <div class='price-box'>
            <h4 style='color: #6a006a; margin-top: 0;'>Biaya Jasa: Rp 25.000 / Survei</h4>
            <p><strong>Instruksi Pembayaran Manual:</strong></p>
            <ul>
                <li>Transfer ke DANA/Gopay: 0812xxxxxx (a.n. SmartSurvey)</li>
                <li>Transfer ke Bank ABC: 123456789 (a.n. Nama Anda)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # --- Formulir Pengajuan Jasa ---
    with st.form(key='custom_analysis_form'):
        st.subheader("Detail Pengajuan Proyek (Wajib Diisi)")
        
        uploaded_file = st.file_uploader("1. Upload file CSV Anda", type=["csv"])
        
        email = st.text_input("2. Email untuk Pengiriman Hasil (Wajib):", 
                                 help="Hasil laporan (PDF) akan dikirim ke alamat ini.")
        
        deskripsi = st.text_area("3. Kebutuhan Analisis Kustom Anda (Wajib):", 
                                 placeholder="Misal: analisis hubungan antara pola makan dan tingkat stres mahasiswa.",
                                 help="Sebutkan kolom demografi dan kolom jawaban yang ingin Anda fokuskan.")
        
        bukti_bayar = st.file_uploader("4. Upload Bukti Transfer (Wajib):", type=["jpg", "png", "pdf"])
        
        # Tombol submit form
        submit_button = st.form_submit_button(label='Kirim Pengajuan Analisis & Konfirmasi Bayar 📤')

    if submit_button:
        if uploaded_file and deskripsi and email and bukti_bayar:
            # Di sini, Anda menyimulasikan penerimaan data
            st.success(f"🎉 Pengajuan berhasil dikirim! Kami akan menganalisis data Anda secara kustom dan mengirimkan laporan ke **{email}** dalam 1x24 jam.")
            st.balloons() 
        else:
            st.error("⚠️ Mohon lengkapi semua kolom (File, Email, Kebutuhan Analisis, dan Bukti Bayar) sebelum mengirim.")

# ====== FOOTER ======
st.markdown("""
    <hr style="border: 0.5px solid #b30086;">
    <div style="text-align: center; color: #6a006a; font-size: 14px; margin-top: 20px;">
        © 2025 <b>SmartSurvey</b>
    </div>
""", unsafe_allow_html=True)
