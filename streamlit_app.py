import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aplikasi dengan 4 Tab", layout="wide")

st.title("📊 Aplikasi Streamlit dengan 4 Tab")

# Membuat 4 Tab
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Beranda", "📈 Grafik", "📋 Tabel Data", "📝 Form Input"])

# ==================== TAB 1 ====================
with tab1:
    st.header("Selamat Datang di Aplikasi Streamlit")
    st.write("""
    Ini adalah halaman beranda. Anda bisa menambahkan deskripsi aplikasi, 
    petunjuk penggunaan, atau informasi umum lainnya di sini.
    """)
    st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", width=300)

# ==================== TAB 2 ====================
with tab2:
    st.header("Visualisasi Data (Grafik)")
    # Contoh data
    data = pd.DataFrame({
        'Hari': ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'],
        'Penjualan': np.random.randint(100, 500, size=5)
    })

    fig, ax = plt.subplots()
    ax.bar(data['Hari'], data['Penjualan'], color='skyblue')
    ax.set_ylabel("Jumlah Penjualan")
    ax.set_title("Grafik Penjualan Harian")
    st.pyplot(fig)

# ==================== TAB 3 ====================
with tab3:
    st.header("Tabel Data")
    # Contoh tabel data
    df = pd.DataFrame({
        "Nama": ["Andi", "Budi", "Citra", "Dina"],
        "Umur": [21, 22, 20, 23],
        "Nilai": [87, 90, 78, 85]
    })
    st.dataframe(df, use_container_width=True)

# ==================== TAB 4 ====================
with tab4:
    st.header("Formulir Input")
    with st.form("form_input"):
        nama = st.text_input("Nama Lengkap")
        usia = st.number_input("Usia", min_value=0, max_value=100)
        pilihan = st.selectbox("Pilih Jurusan", ["Teknik Informatika", "Sistem Informasi", "Data Science"])
        submit = st.form_submit_button("Kirim")

        if submit:
            st.success(f"Data berhasil dikirim! Halo {nama}, usia {usia} tahun, jurusan {pilihan}.")

