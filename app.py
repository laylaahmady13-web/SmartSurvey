import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io # Diperlukan untuk penanganan file upload
from PIL import Image # Diperlukan untuk memproses gambar bukti bayar

# ====== Konfigurasi Halaman & Gaya CSS ======
st.set_page_config(page_title="SmartSurvey", page_icon="📊", layout="centered")

# Menggunakan expander CSS untuk tampilan yang lebih modern
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

# ====== Sidebar Navigasi ======
menu = st.sidebar.radio("Menu Utama", ["Home", "Analisis Cepat (Gratis)", "Analisis Lengkap (Berbayar)"])

# --- Fungsi Pembantu untuk Visualisasi ---
@st.cache_data
def plot_frequency(df, column):
    """Membuat Bar Chart/Histogram yang cerdas berdasarkan tipe data kolom."""
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Deteksi data kategorikal (string atau uniknya sedikit)
    if df[column].dtype == 'object' or df[column].nunique() < 20:
        # Gunakan countplot untuk data kategori survei (SS, S, dll.)
        sns.countplot(y=column, data=df, 
                      order=df[column].value_counts().index, 
                      palette="viridis", ax=ax)
        ax.set_title(f"Frekuensi Jawaban: {column}")
        ax.set_xlabel("Jumlah Responden")
        ax.set_ylabel("") # Hapus label y
    else:
        # Gunakan histogram untuk data numerik (usia, skor, dll.)
        df[column].hist(ax=ax, bins=15, color='#b30086')
        ax.set_title(f"Distribusi Nilai: {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frekuensi")
        
    plt.tight_layout()
    return fig

# ====== Halaman HOME ======
if menu == "Home":
    # Catatan: Karena saya tidak dapat mengakses gambar Anda di GitHub, saya menggunakan placeholder
    st.markdown("<div style='text-align: center;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>SmartSurvey</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Analisis survei otomatis — cepat, mudah, dan profesional</div>", unsafe_allow_html=True)

    st.write("""
    Selamat datang di **SmartSurvey**! Kami mengubah data survei mentah Anda menjadi *insight* yang siap digunakan untuk laporan dan skripsi.
    
    ### Pilih layanan sesuai kebutuhanmu:
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Analisis Cepat (Gratis)")
        st.write("""
        - Upload file CSV kamu.  
        - Lihat analisis deskriptif & **visualisasi 1 variabel** langsung di sini.  
        - Cocok untuk uji coba *tool* dan kebutuhan data dasar.
        """)
        st.button("Mulai Analisis Gratis", on_click=lambda: st.session_state.update(menu="Analisis Cepat (Gratis)"))

    with col2:
        st.subheader("Analisis Lengkap (Berbayar)")
        st.write("""
        - **Jasa Analisis Kustom** (Rp25.000).
        - Hasil lengkap dikirim via email (*crosstab*, *insight*, & **Laporan PDF** profesional).
        - Termasuk *consultation* hasil.
        """)
        st.button("Ajukan Analisis Kustom", on_click=lambda: st.session_state.update(menu="Analisis Lengkap (Berbayar)"))

    st.markdown("---")
    st.write("📊 **SmartSurvey – Data Anda, Insight Kami.**")
    st.write("_Didukung oleh Python & Streamlit_")
    
# ====== Halaman GRATIS ======
elif menu == "Analisis Cepat (Gratis)":
    # Memastikan library berat di-import hanya di sini
    import matplotlib.pyplot as plt
    import seaborn as sns 
    
    st.header("Analisis Cepat (Gratis)")
    st.write("Unggah file CSV Anda. Kami akan menganalisis data Anda secara otomatis dan menampilkan hasilnya di halaman ini.")

    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File berhasil diunggah!")
            
            # --- 1. Pratinjau Data ---
            with st.expander("🧾 Pratinjau Data & Statistik", expanded=True):
                st.write("5 Baris Pertama Data")
                st.dataframe(df.head())

                st.write("Statistik Deskriptif")
                st.dataframe(df.describe(include='all'))

            # --- 2. Visualisasi Otomatis ---
            st.write("### 🎨 Visualisasi Frekuensi")
            
            # Filter kolom yang mungkin tidak relevan
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
        st.info("💡 Untuk analisis mendalam (crosstab, insight lanjutan, laporan PDF), gunakan menu **Analisis Lengkap (Berbayar)**.")

# ====== Halaman BERBAYAR (Jasa Kustom) ======
elif menu == "Analisis Lengkap (Berbayar)":
    st.header("Analisis Lengkap (Jasa Kustom)")
    st.write("Layanan analisis data survei mendalam. Anda berikan instruksi, kami berikan Laporan PDF profesional.")

    # --- Informasi Harga dan Cara Bayar ---
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
        st.subheader("Detail Pengajuan Proyek")
        
        uploaded_file = st.file_uploader("1. Upload file CSV Anda", type=["csv"])
        
        email = st.text_input("2. Email untuk Pengiriman Hasil (Wajib):", 
                                 help="Hasil laporan (PDF) akan dikirim ke alamat ini.")
        
        deskripsi = st.text_area("3. Kebutuhan Analisis Kustom Anda (Wajib):", 
                                 placeholder="Misal: Saya ingin melihat korelasi antara 'Angkatan' dan 'Tingkat Stres'.",
                                 help="Sebutkan kolom mana yang ingin dibandingkan atau difilter.")
        
        bukti_bayar = st.file_uploader("4. Upload Bukti Transfer (Gambar/PDF):", type=["jpg", "png", "pdf"])
        
        submit_button = st.form_submit_button(label='Kirim Pengajuan Analisis & Konfirmasi Bayar 📤')

    if submit_button:
        if uploaded_file and deskripsi and email and bukti_bayar:
            
            # Catatan: Di sini, Anda perlu mekanisme real-life untuk menyimpan/mengirim data ini
            # Contoh: Mengirim email notifikasi ke Anda (pemilik) berisi file dan instruksi
            
            st.success(f"🎉 Pengajuan berhasil dikirim! Kami akan menganalisis data Anda secara kustom dan mengirimkan laporan ke **{email}** dalam 1x24 jam.")
            st.balloons() 
            
            st.markdown("---")
            st.write("Terima kasih atas kepercayaan Anda!")
        else:
            st.error("⚠️ Mohon lengkapi semua kolom (File, Email, Kebutuhan Analisis, dan Bukti Bayar) sebelum mengirim.")

# ====== FOOTER ======
st.markdown("""
    <hr style="border: 0.5px solid #b30086;">
    <div style="text-align: center; color: #6a006a; font-size: 14px; margin-top: 20px;">
        © 2025 <b>SmartSurvey by Laylaa</b> – Dibuat dengan Streamlit dan Python
    </div>
""", unsafe_allow_html=True)
