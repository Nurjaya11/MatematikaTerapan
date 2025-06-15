import streamlit as st
from scipy.optimize import linprog
import math

st.set_page_config(page_title="Model Matematika Interaktif", layout="wide")

tab1, tab2, tab3, tab4 = st.tabs([
    "Optimasi Produksi (Linear Programming)",
    "Model Persediaan (EOQ)",
    "Model Antrian (M/M/1)",
    "Model Matematika Lainnya"
])

# ================= TAB 1: LINEAR PROGRAMMING ====================
with tab1:
    st.header("Optimasi Produksi (Linear Programming)")

    st.write("Contoh: Maksimalkan profit berdasarkan batasan bahan baku")

    c1 = st.number_input("Profit per unit Produk A", value=20)
    c2 = st.number_input("Profit per unit Produk B", value=30)
    
    bahan1_a = st.number_input("Bahan baku 1 per unit Produk A", value=1)
    bahan1_b = st.number_input("Bahan baku 1 per unit Produk B", value=2)
    max_bahan1 = st.number_input("Jumlah maksimal bahan baku 1", value=40)

    bahan2_a = st.number_input("Bahan baku 2 per unit Produk A", value=3)
    bahan2_b = st.number_input("Bahan baku 2 per unit Produk B", value=1)
    max_bahan2 = st.number_input("Jumlah maksimal bahan baku 2", value=30)

    if st.button("Hitung Optimasi Produksi"):
        c = [-c1, -c2]  # negatif karena linprog melakukan minimisasi
        A = [
            [bahan1_a, bahan1_b],
            [bahan2_a, bahan2_b]
        ]
        b = [max_bahan1, max_bahan2]
        x_bounds = (0, None)
        res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, x_bounds], method='highs')

        if res.success:
            st.success("Solusi Ditemukan:")
            st.write(f"Produksi Produk A: {res.x[0]:.2f} unit")
            st.write(f"Produksi Produk B: {res.x[1]:.2f} unit")
            st.write(f"Total Profit Maksimum: {-res.fun:.2f}")
        else:
            st.error("Optimasi gagal. Silakan cek input.")

# ================= TAB 2: EOQ ====================
with tab2:
    st.header("Model Persediaan EOQ (Economic Order Quantity)")

    D = st.number_input("Permintaan tahunan (unit/tahun)", value=1000)
    S = st.number_input("Biaya pemesanan per pesanan", value=50)
    H = st.number_input("Biaya penyimpanan per unit per tahun", value=2)

    if st.button("Hitung EOQ"):
        try:
            EOQ = math.sqrt((2 * D * S) / H)
            st.success(f"EOQ: {EOQ:.2f} unit per pesanan")
        except:
            st.error("Terjadi kesalahan perhitungan")

# ================= TAB 3: M/M/1 ====================
with tab3:
    st.header("Model Antrian M/M/1")

    lambd = st.number_input("Laju kedatangan pelanggan (λ)", value=5.0)
    mu = st.number_input("Laju pelayanan pelanggan (μ)", value=8.0)

    if st.button("Hitung Model Antrian"):
        if lambd < mu:
            rho = lambd / mu
            Lq = (rho**2) / (1 - rho)
            L = rho / (1 - rho)
            Wq = Lq / lambd
            W = L / lambd

            st.success("Hasil Perhitungan:")
            st.write(f"Utilisasi (ρ): {rho:.2f}")
            st.write(f"Rata-rata pelanggan dalam antrian (Lq): {Lq:.2f}")
            st.write(f"Rata-rata pelanggan dalam sistem (L): {L:.2f}")
            st.write(f"Waktu tunggu dalam antrian (Wq): {Wq:.2f} jam")
            st.write(f"Waktu total dalam sistem (W): {W:.2f} jam")
        else:
            st.error("λ harus lebih kecil dari μ agar sistem stabil.")

# ================= TAB 4: MODEL MATEMATIK LAIN ====================
with tab4:
    st.header("Model Pertumbuhan Populasi Eksponensial")

    P0 = st.number_input("Populasi awal", value=100)
    r = st.number_input("Tingkat pertumbuhan (desimal)", value=0.05)
    t = st.number_input("Waktu (tahun)", value=10)

    if st.button("Hitung Pertumbuhan Populasi"):
        Pt = P0 * math.exp(r * t)
        st.success(f"Populasi setelah {t} tahun: {Pt:.2f}")
