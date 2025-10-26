import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Smart Survey", layout="wide")

# Header
st.title("Smart Survey Dashboard")
st.write("Upload data survey dan pilih jenis analisis.")

# Tabel perbandingan harga & fitur
st.subheader("Perbandingan Analisis & Harga")
price_table = pd.DataFrame({
    "Jenis Analisis": ["Analisis Cepat", "Analisis Lengkap"],
    "Harga": ["Rp10.000 / survey", "Rp25.000 / survey"],
    "Fitur Utama": [
        "Ringkasan statistik + histogram + CSV",
        "Semua Cepat + filter/segmentasi + insight + export lengkap"
    ]
})
st.table(price_table)

# Sidebar
st.sidebar.title("Pengaturan Survey")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")
analysis_type = st.sidebar.radio("Jenis Analisis:", ("Analisis Cepat", "Analisis Lengkap"))

st.sidebar.write("**Harga:**")
if analysis_type == "Analisis Cepat":
    st.sidebar.write("Rp10.000 / survey")
else:
    st.sidebar.write("Rp25.000 / survey")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File berhasil diupload!")

    if st.sidebar.button("Bayar Sekarang"):
        st.success("Pembayaran berhasil! 🎉")

        st.header("Hasil Analisis Survey")

        # Layout 3 kolom
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Ringkasan Statistik")
            st.dataframe(df.describe())

        with col2:
            st.subheader("Visualisasi")
            for col in df.select_dtypes(include=['int64', 'float64']).columns:
                fig, ax = plt.subplots()
                df[col].hist(ax=ax, bins=10 if analysis_type == "Analisis Cepat" else 15)
                ax.set_title(f'{col}')
                st.pyplot(fig)

        with col3:
            st.subheader("Export Hasil")
            csv = df.to_csv(index=False).encode('utf-8')
            filename = "hasil_survey_cepat.csv" if analysis_type == "Analisis Cepat" else "hasil_survey_lengkap.csv"
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=filename,
                mime="text/csv",
            )

            if analysis_type == "Analisis Lengkap":
                st.write("**Filter / Segmentasi**")
                for col in df.select_dtypes(include=['object']).columns:
                    unique_vals = df[col].unique()
                    selected = st.multiselect(f"Pilih {col}:", unique_vals, default=unique_vals)
                    filtered = df[df[col].isin(selected)]
                    st.dataframe(filtered.describe())
