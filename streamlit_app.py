import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulasi Gas Ideal", layout="centered")
st.title("🌡 Simulasi Gas Ideal dan Energi Termodinamika")

# Konstanta
R = 0.0821  # L·atm/mol·K
R_J = 8.314  # J/mol·K

st.header("🔢 Input Umum")
n = st.number_input("Jumlah mol (n)", value=1.0)
T_C = st.number_input("Suhu (°C)", value=25.0)
T = T_C + 273.15
V1 = st.number_input("Volume awal (L)", value=1.0)
V2 = st.number_input("Volume akhir (L)", value=2.0)
P = st.number_input("Tekanan (atm)", value=1.0)

# ================= PV = nRT ==================
st.markdown("## 📘 Hitung Variabel PV = nRT")
var = st.selectbox("Pilih variabel yang ingin dihitung", ["Tekanan (P)", "Volume (V)", "Mol (n)", "Suhu (T)"])

if st.button("Hitung Gas Ideal"):
    try:
        if var == "Tekanan (P)":
            result = (n * R * T) / V1
            st.success(f"Tekanan (P) = {result:.4f} atm")
        elif var == "Volume (V)":
            result = (n * R * T) / P
            st.success(f"Volume (V) = {result:.4f} L")
        elif var == "Mol (n)":
            result = (P * V1) / (R * T)
            st.success(f"Mol (n) = {result:.4f} mol")
        elif var == "Suhu (T)":
            result = (P * V1) / (n * R)
            st.success(f"Suhu = {result:.2f} K / {result - 273.15:.2f} °C")
    except:
        st.error("Input tidak valid (mungkin pembagian dengan nol).")

# ================= ENERGI ==================
st.markdown("## 🔥 Energi Gas (q, w, ΔU, ΔH)")
proses = st.selectbox("Pilih jenis proses", ["Isobarik", "Isokhorik", "Isotermal", "Adiabatik"])

Cp = 5 / 2 * R_J  # J/mol·K (diatomik)
Cv = 3 / 2 * R_J
gamma = Cp / Cv

if st.button("Hitung Energi"):
    try:
        deltaT = 0 if proses == "Isotermal" else T - 298.15  # asumsikan T1 = 25°C (298.15 K)
        if proses == "Isobarik":
            q = n * Cp * deltaT
            w = -P * (V2 - V1) * 101.325
            dU = n * Cv * deltaT
            dH = n * Cp * deltaT
        elif proses == "Isokhorik":
            q = n * Cv * deltaT
            w = 0
            dU = q
            dH = n * Cp * deltaT
        elif proses == "Isotermal":
            q = -n * R_J * T * np.log(V2 / V1)
            w = -q
            dU = 0
            dH = 0
        elif proses == "Adiabatik":
            q = 0
            w = (P * V1 - P * V2) / (1 - gamma)
            dU = -w
            dH = dU + P * (V2 - V1) * 101.325

        st.info(f"q (kalor) = {q:.2f} J")
        st.info(f"w (kerja) = {w:.2f} J")
        st.info(f"ΔU (energi dalam) = {dU:.2f} J")
        st.info(f"ΔH (entalpi) = {dH:.2f} J")
    except:
        st.error("Perhitungan gagal. Periksa input.")

# ================= GRAFIK ==================
st.markdown("## 📊 Grafik Isotermal P vs V")

if st.checkbox("Tampilkan grafik?"):
    V_range = np.linspace(0.1, 5, 200)
    P_vals = (n * R * T) / V_range

    fig, ax = plt.subplots()
    ax.plot(V_range, P_vals, label="Isotermal")
    ax.set_xlabel("Volume (L)")
    ax.set_ylabel("Tekanan (atm)")
    ax.set_title("Kurva Isotermal P vs V")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
