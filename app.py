import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Smart Survey", layout="wide")

# Styling global
st.markdown("""
    <style>
    .stApp { background-color: #ffe6f0; }
    h1, h2, h3, h4 { color: #b30086; }
    .center { text-align: center; }
    .card {
        background-color: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header utama
st.markdown("<h1 class='center'>Smart Survey Dashboard</h1>", unsafe_allow_html=True)
st.write("Unggah data survei Anda dan pilih jenis analisis yang diinginkan.")

# Tabel perbandingan
st.subheader("📊 Perbandingan Analisis & Harga")
price_table = pd.DataFrame({
    "Jenis Analisis": ["Analisis Cepat (Gratis)", "Analisis Lengkap (Kustom)"],
    "Harga": ["Gratis (Preview)", "Rp25.000 / survey"],
    "Fitur Utama": [
        "Ringkasan statistik + Visualisasi 1 variabel + Preview data mentah",
        "Analisis mendalam + Crosstab + Laporan PDF via email (manual)"
    ]
})
st.table(price_table)

# Sidebar
st.sidebar.title("⚙️ Pengaturan Smart Survey")
uploaded_file = st.sidebar.file_uploader("Upload File CSV Anda", type="csv")
analysis_type = st.sidebar.radio(
    "Pilih Mode Analisis:",
    ("Analisis Cepat (Gratis)", "Analisis Lengkap (Kustom Berbayar)")
)

# --- Jika file diupload ---
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ File berhasil diupload!")

        # --- MODE GRATIS ---
        if analysis_type == "Analisis Cepat (Gratis)":
            st.markdown("<h2>Hasil Analisis Cepat (Preview)</h2>", unsafe_allow_html=True)
            st.info("Analisis otomatis untuk melihat ringkasan dan distribusi dasar dari data Anda.")

            # Ringkasan Statistik
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("📈 Ringkasan Statistik")
                try:
                    st.dataframe(df.describe(include='all'))
                except Exception:
                    st.warning("Tidak dapat menampilkan statistik karena format data tidak sesuai.")
                st.markdown("</div>", unsafe_allow_html=True)

            # Pilih kolom untuk visualisasi
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("📊 Visualisasi Frekuensi")
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
            st.markdown("</div>", unsafe_allow_html=True)

            st.warning("Untuk analisis mendalam (crosstab, insight lanjutan, laporan PDF), gunakan mode **Analisis Lengkap (Kustom)**.")

        # --- MODE BERBAYAR ---
        elif analysis_type == "Analisis Lengkap (Kustom Berbayar)":
            st.markdown("<h2>📝 Formulir Pengajuan Analisis Kustom</h2>", unsafe_allow_html=True)
            st.info("Kami akan menganalisis data Anda secara mendalam dan mengirimkan laporan hasil ke email Anda dalam 1x24 jam setelah pembayaran.")

            with st.form(key='form_premium'):
                st.subheader("📌 Detail Pemesanan")
                email_user = st.text_input("1️⃣ Email untuk pengiriman hasil")
                kebutuhan = st.text_area("2️⃣ Jelaskan kebutuhan analisis Anda", 
                                         help="Contoh: Bandingkan tingkat stres berdasarkan angkatan.")
                st.markdown("---")
                st.subheader("Konfirmasi Pembayaran")
                st.write("Transfer Rp25.000 ke DANA: **0812-xxxx-xxxx a.n. Layla** (contoh).")
                bukti = st.file_uploader("Upload bukti transfer (gambar/pdf):", type=["jpg", "png", "pdf"])
                submit = st.form_submit_button("✅ Kirim Pengajuan")

            if submit:
                if email_user and kebutuhan and bukti:
                    st.success("🎉 Pengajuan Berhasil!")
                    st.info(f"Laporan hasil akan dikirim ke **{email_user}** paling lambat dalam 1x24 jam.")
                    st.write("Terima kasih telah menggunakan Smart Survey Premium 💗")
                else:
                    st.error("⚠️ Harap isi semua kolom dan upload bukti pembayaran.")

    except Exception as e:
        st.error(f"Gagal membaca file: {e}")

else:
    st.info("📂 Silakan upload file CSV Anda melalui sidebar untuk memulai analisis.")

# Footer
st.markdown("<br><hr><p style='text-align:center; color:#b30086;'>© 2025 SmartSurvey by Layla Ahmady</p>", unsafe_allow_html=True)
