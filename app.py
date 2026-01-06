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
    <img src="https://raw.githubusercontent.com/laylaahmady13-web/SmartSurvey/main/biru%20modern%20huruf%20LM%20logo.png" width="150">
    <div class="hero-title">SmartSurvey</div>
    <div class="hero-sub">Layanan Survei & Analisis Data Digital</div>
    <div class="motto">“Kamu fokus di tugasnya, kami bereskan datanya.”</div>
    <br>
    <a class="button-primary" href="#layanan">Lihat Layanan</a>
</div>
""", unsafe_allow_html=True)


# ========================== SECTION: LAYANAN (FIXED INDENTATION) ==========================
st.markdown("<h2 id='layanan'>✨ Pilihan Layanan</h2>", unsafe_allow_html=True)

# Perhatian: Semua tag HTML di bawah ini DILARANG memiliki spasi/tab di awal baris
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
<div class="card-title">Paket Uji Asumsi Regresi</div>
<div class="card-price">Rp 30.000</div>
</div>

<div class="card">
<div class="card-title">Ujii F dan Uji T</div>
<div class="card-price">Rp 30.000</div>
</div>

<div class="card">
<div class="card-title">Uji yang diperlukan</div>
<div class="card-price">Rp 35.000</div>
</div>

<div class="card">
<div class="card-title">Custom Laporan PDF</div>
<div class="card-price">Rp 5.000 – Rp 10.000</div>
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
        
        # -------------------------------------------------------------
        # FITUR BARU 1: BAR CHART NILAI HILANG (MISSING VALUES)
        # -------------------------------------------------------------
        st.subheader("Analisis Nilai Hilang (Missing Values)")
        missing_values = df.isnull().sum().sort_values(ascending=False)
        missing_values = missing_values[missing_values > 0]

        if missing_values.empty:
            st.info("🎉 Data Anda bersih! Tidak ditemukan nilai yang hilang.")
        else:
            fig_miss, ax_miss = plt.subplots(figsize=(10, 5))
            sns.barplot(x=missing_values.index, y=missing_values.values, ax=ax_miss, palette="Blues_d")
                
            plt.xticks(rotation=45, ha='right')
            ax_miss.set_ylabel("Jumlah Nilai Hilang")
            ax_miss.set_xlabel("Kolom")
            ax_miss.set_title("Jumlah Nilai Hilang per Kolom")
            st.pyplot(fig_miss)
            
        # -------------------------------------------------------------
        # FITUR BARU 2: FUNGSI PLOT KOLOM DENGAN BOX PLOT & HISTOGRAM
        # -------------------------------------------------------------
        
        def plot_col(df, col):
            # Cek apakah kolom adalah datetime (Cap waktu)
            try:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    # Jika datetime, kita buat kolom baru: Jam (Hour)
                    df['Jam Survei'] = df[col].dt.hour
                    col_to_plot = 'Jam Survei'
                    st.subheader(f"Frekuensi Berdasarkan {col_to_plot}")
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    # Gunakan Bar Plot biasa, bukan Countplot, untuk mengontrol sumbu X
                    df[col_to_plot].value_counts().sort_index().plot(kind='bar', ax=ax, color='#4d9bf7')
                    ax.set_title(f'Distribusi Pengisian Survei berdasarkan Jam (0-23)')
                    ax.set_xlabel("Jam")
                    ax.set_ylabel("Frekuensi")
                    plt.xticks(rotation=0)
                    st.pyplot(fig)
                    
                    # Hapus kolom sementara
                    df.drop(columns=['Jam Survei'], inplace=True)
                    return
        
            except Exception:
                # Jika bukan datetime, lanjutkan ke pemrosesan kategori/numerik
                pass
        
            # Logika Kategori/Numerik
            is_categorical = (df[col].dtype == 'object') or (df[col].nunique() <= 20 and df[col].nunique() > 1)
            
            if is_categorical:
                # Visualisasi untuk data Kategorikal/Diskrit (Countplot)
                st.subheader(f"Frekuensi {col}")
                
                # Logika: Jika terlalu banyak kategori, tampilkan vertikal
                if df[col].nunique() > 10:
                    figsize = (10, max(5, df[col].nunique() * 0.4)) # Ukuran figure dinamis
                    fig, ax = plt.subplots(figsize=figsize)
                    sns.countplot(y=col, data=df, ax=ax, order=df[col].value_counts().index, palette="viridis")
                    ax.set_title(f'Distribusi {col}')
                    plt.tight_layout() # Mencegah label tumpang tindih
                    st.pyplot(fig)
                else:
                    # Standar Bar Chart Vertikal (untuk kategori sedikit)
                    fig, ax = plt.subplots(figsize=(10, 5))
                    sns.countplot(x=col, data=df, ax=ax, order=df[col].value_counts().index, palette="viridis")
                    ax.set_title(f'Distribusi {col}')
                    plt.xticks(rotation=45, ha='right') # Putar label X untuk kategori
                    st.pyplot(fig)
        
            else:
                # Visualisasi untuk data Numerik/Kontinu (Histogram & Boxplot)
                if df[col].dtype == 'number':
                    st.subheader(f"Distribusi {col} (Histogram)")
                    fig_hist, ax_hist = plt.subplots(figsize=(7, 4))
                    df[col].hist(ax=ax_hist, bins=15, color='#4d9bf7', edgecolor='black')
                    ax_hist.set_title(f'Histogram {col}')
                    st.pyplot(fig_hist)
                    
                    # Tambahan Box Plot
                    st.subheader(f"Distribusi {col} (Box Plot)")
                    fig_box, ax_box = plt.subplots(figsize=(7, 2))
                    sns.boxplot(x=df[col], ax=ax_box, color='lightcoral')
                    ax_box.set_title(f'Box Plot {col}')
                    st.pyplot(fig_box)
                else:
                     # Jika ada kolom object dengan banyak unique values (> 20) yang tidak cocok untuk countplot
                    st.info(f"Kolom '{col}' memiliki terlalu banyak nilai unik ({df[col].nunique()}). Visualisasi Countplot tidak disarankan.")
        
        # -------------------------------------------------------------
        
        pilih = st.selectbox("Pilih kolom untuk visualisasi", df.columns)

        if pilih:
            plot_col(df, pilih) 

    except Exception as e:
        st.error(f"Terjadi error saat memproses data: Pastikan format CSV sudah benar. Error: {e}")


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
