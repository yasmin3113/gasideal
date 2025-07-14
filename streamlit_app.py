import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# Konfigurasi halaman
st.set_page_config(
    page_title="Simulasi Gas Ideal Advanced", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling yang lebih menarik
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    .process-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header utama
st.markdown("""
<div class="main-header">
    <h1>🧪 Simulasi Gas Ideal & Termodinamika Advanced</h1>
    <p>Simulasi lengkap dengan visualisasi interaktif dan analisis mendalam</p>
</div>
""", unsafe_allow_html=True)

# Sidebar untuk kontrol utama
st.sidebar.header("🎛️ Kontrol Utama")
simulation_mode = st.sidebar.selectbox(
    "Pilih Mode Simulasi",
    ["Gas Ideal Dasar", "Proses Termodinamika", "Siklus Termodinamika", "Perbandingan Gas"]
)

# Konstanta
R = 0.0821  # L·atm/mol·K
R_J = 8.314  # J/mol·K
NA = 6.022e23  # Avogadro number

# Fungsi utility
def calculate_molecular_properties(T, M=28.014):  # Default untuk N2
    """Hitung properti molekular"""
    v_avg = np.sqrt(8 * R_J * T / (np.pi * M / 1000))  # m/s
    v_rms = np.sqrt(3 * R_J * T / (M / 1000))  # m/s
    v_mp = np.sqrt(2 * R_J * T / (M / 1000))  # m/s
    return v_avg, v_rms, v_mp

def maxwell_boltzmann(v, T, M=28.014):
    """Distribusi Maxwell-Boltzmann"""
    M_kg = M / 1000  # kg/mol
    return 4 * np.pi * (M_kg / (2 * np.pi * R_J * T))**(3/2) * v**2 * np.exp(-M_kg * v**2 / (2 * R_J * T))

def van_der_waals(T, V, n, a, b):
    """Persamaan Van der Waals"""
    return (n * R_J * T / (V - n * b)) - (a * n**2 / V**2)

# === MODE 1: GAS IDEAL DASAR ===
if simulation_mode == "Gas Ideal Dasar":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📊 Input Parameter")
        n = st.number_input("Jumlah mol (n)", value=1.0, min_value=0.1, max_value=10.0, step=0.1)
        T_C = st.number_input("Suhu (°C)", value=25.0, min_value=-273.0, max_value=1000.0, step=1.0)
        T = T_C + 273.15
        V = st.number_input("Volume (L)", value=1.0, min_value=0.1, max_value=100.0, step=0.1)
        P = st.number_input("Tekanan (atm)", value=1.0, min_value=0.1, max_value=50.0, step=0.1)
        
        # Pilihan gas
        gas_type = st.selectbox("Jenis Gas", ["N₂ (Nitrogen)", "O₂ (Oxygen)", "H₂ (Hydrogen)", "CO₂ (Carbon Dioxide)", "He (Helium)"])
        gas_properties = {
            "N₂ (Nitrogen)": {"M": 28.014, "Cp": 29.1, "Cv": 20.8},
            "O₂ (Oxygen)": {"M": 31.998, "Cp": 29.4, "Cv": 21.1},
            "H₂ (Hydrogen)": {"M": 2.016, "Cp": 28.8, "Cv": 20.4},
            "CO₂ (Carbon Dioxide)": {"M": 44.01, "Cp": 37.1, "Cv": 28.5},
            "He (Helium)": {"M": 4.003, "Cp": 20.8, "Cv": 12.5}
        }
        
        M = gas_properties[gas_type]["M"]
        Cp = gas_properties[gas_type]["Cp"]
        Cv = gas_properties[gas_type]["Cv"]
    
    with col2:
        st.header("🔢 Hasil Perhitungan")
        
        # Hitung PV = nRT
        var_to_calc = st.selectbox("Hitung variabel:", ["Tekanan (P)", "Volume (V)", "Mol (n)", "Suhu (T)"])
        
        if st.button("🧮 Hitung", key="calc_basic"):
            try:
                if var_to_calc == "Tekanan (P)":
                    result = (n * R * T) / V
                    st.success(f"**Tekanan (P) = {result:.4f} atm**")
                elif var_to_calc == "Volume (V)":
                    result = (n * R * T) / P
                    st.success(f"**Volume (V) = {result:.4f} L**")
                elif var_to_calc == "Mol (n)":
                    result = (P * V) / (R * T)
                    st.success(f"**Mol (n) = {result:.4f} mol**")
                elif var_to_calc == "Suhu (T)":
                    result = (P * V) / (n * R)
                    st.success(f"**Suhu = {result:.2f} K / {result - 273.15:.2f} °C**")
            except:
                st.error("❌ Input tidak valid!")
        
        # Properti molekular
        st.markdown("### 🔬 Properti Molekular")
        v_avg, v_rms, v_mp = calculate_molecular_properties(T, M)
        
        col2a, col2b = st.columns(2)
        with col2a:
            st.metric("Kecepatan Rata-rata", f"{v_avg:.1f} m/s")
            st.metric("Kecepatan RMS", f"{v_rms:.1f} m/s")
        with col2b:
            st.metric("Kecepatan Paling Mungkin", f"{v_mp:.1f} m/s")
            st.metric("Energi Kinetik Rata-rata", f"{3/2 * R_J * T:.1f} J/mol")
    
    # Visualisasi distribusi kecepatan
    st.header("📈 Distribusi Kecepatan Maxwell-Boltzmann")
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Distribusi Kecepatan', 'Perbandingan Suhu'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Plot 1: Distribusi kecepatan pada suhu tertentu
    v_range = np.linspace(0, 3000, 1000)
    prob_dist = maxwell_boltzmann(v_range, T, M)
    
    fig.add_trace(
        go.Scatter(x=v_range, y=prob_dist, name=f'T = {T:.1f} K', line=dict(color='blue', width=2)),
        row=1, col=1
    )
    
    # Plot 2: Perbandingan pada berbagai suhu
    temperatures = [200, 300, 400, 500]
    colors = ['blue', 'red', 'green', 'orange']
    
    for i, temp in enumerate(temperatures):
        prob_dist_temp = maxwell_boltzmann(v_range, temp, M)
        fig.add_trace(
            go.Scatter(x=v_range, y=prob_dist_temp, 
                      name=f'T = {temp} K', 
                      line=dict(color=colors[i], width=2)),
            row=1, col=2
        )
    
    fig.update_layout(height=400, showlegend=True)
    fig.update_xaxes(title_text="Kecepatan (m/s)", row=1, col=1)
    fig.update_xaxes(title_text="Kecepatan (m/s)", row=1, col=2)
    fig.update_yaxes(title_text="Probabilitas", row=1, col=1)
    fig.update_yaxes(title_text="Probabilitas", row=1, col=2)
    
    st.plotly_chart(fig, use_container_width=True)

# === MODE 2: PROSES TERMODINAMIKA ===
elif simulation_mode == "Proses Termodinamika":
    st.header("🔥 Analisis Proses Termodinamika")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Parameter Sistem")
        n = st.number_input("Jumlah mol (n)", value=1.0, min_value=0.1, max_value=10.0, step=0.1, key="thermo_n")
        T1_C = st.number_input("Suhu awal (°C)", value=25.0, min_value=-273.0, max_value=1000.0, step=1.0)
        T2_C = st.number_input("Suhu akhir (°C)", value=100.0, min_value=-273.0, max_value=1000.0, step=1.0)
        T1 = T1_C + 273.15
        T2 = T2_C + 273.15
        
        V1 = st.number_input("Volume awal (L)", value=1.0, min_value=0.1, max_value=100.0, step=0.1, key="thermo_v1")
        V2 = st.number_input("Volume akhir (L)", value=2.0, min_value=0.1, max_value=100.0, step=0.1, key="thermo_v2")
        P1 = st.number_input("Tekanan awal (atm)", value=1.0, min_value=0.1, max_value=50.0, step=0.1, key="thermo_p1")
        
        # Pilihan proses
        proses = st.selectbox("Jenis Proses", 
            ["Isobarik (P konstan)", "Isokhorik (V konstan)", "Isotermal (T konstan)", "Adiabatik (Q = 0)"])
        
        # Konstanta gas
        Cp = st.number_input("Cp (J/mol·K)", value=29.1, min_value=10.0, max_value=50.0, step=0.1)
        Cv = st.number_input("Cv (J/mol·K)", value=20.8, min_value=10.0, max_value=50.0, step=0.1)
        gamma = Cp / Cv
        
    with col2:
        st.subheader("📊 Hasil Perhitungan")
        
        if st.button("🔍 Analisis Proses", key="analyze_process"):
            try:
                # Hitung berdasarkan jenis proses
                if proses == "Isobarik (P konstan)":
                    P2 = P1  # Tekanan konstan
                    V2_calc = V1 * T2 / T1  # Hukum Charles
                    q = n * Cp * (T2 - T1)
                    w = -P1 * (V2_calc - V1) * 101.325  # Konversi ke J
                    dU = n * Cv * (T2 - T1)
                    dH = q
                    
                    st.success(f"**Proses Isobarik (P = {P1:.2f} atm)**")
                    st.info(f"Volume akhir: {V2_calc:.3f} L")
                    
                elif proses == "Isokhorik (V konstan)":
                    V2_calc = V1  # Volume konstan
                    P2 = P1 * T2 / T1  # Hukum Gay-Lussac
                    q = n * Cv * (T2 - T1)
                    w = 0  # Tidak ada kerja
                    dU = q
                    dH = n * Cp * (T2 - T1)
                    
                    st.success(f"**Proses Isokhorik (V = {V1:.2f} L)**")
                    st.info(f"Tekanan akhir: {P2:.3f} atm")
                    
                elif proses == "Isotermal (T konstan)":
                    T2 = T1  # Suhu konstan
                    P2 = P1 * V1 / V2  # Hukum Boyle
                    q = n * R_J * T1 * np.log(V2 / V1)
                    w = -q  # Untuk gas ideal isotermal
                    dU = 0  # Energi dalam konstan
                    dH = 0  # Entalpi konstan
                    
                    st.success(f"**Proses Isotermal (T = {T1:.1f} K)**")
                    st.info(f"Tekanan akhir: {P2:.3f} atm")
                    
                elif proses == "Adiabatik (Q = 0)":
                    # Untuk adiabatik: PV^γ = konstan, TV^(γ-1) = konstan
                    P2 = P1 * (V1/V2)**gamma
                    T2 = T1 * (V1/V2)**(gamma-1)
                    q = 0  # Tidak ada perpindahan panas
                    w = (P1 * V1 - P2 * V2) * 101.325 / (gamma - 1)
                    dU = -w
                    dH = dU + (P2 * V2 - P1 * V1) * 101.325
                    
                    st.success(f"**Proses Adiabatik (Q = 0)**")
                    st.info(f"Tekanan akhir: {P2:.3f} atm")
                    st.info(f"Suhu akhir: {T2:.1f} K ({T2-273.15:.1f} °C)")
                
                # Tampilkan hasil energi
                st.markdown("### 🔋 Energi Proses")
                
                energy_df = pd.DataFrame({
                    'Parameter': ['Kalor (q)', 'Kerja (w)', 'ΔU (Energi Dalam)', 'ΔH (Entalpi)'],
                    'Nilai (J)': [q, w, dU, dH],
                    'Keterangan': [
                        'Panas yang diserap/dilepas sistem',
                        'Kerja yang dilakukan oleh/pada sistem',
                        'Perubahan energi dalam sistem',
                        'Perubahan entalpi sistem'
                    ]
                })
                
                st.dataframe(energy_df, use_container_width=True)
                
                # Diagram P-V
                st.markdown("### 📈 Diagram P-V")
                
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if proses == "Isobarik (P konstan)":
                    ax.plot([V1, V2_calc], [P1, P1], 'b-', linewidth=3, label='Isobarik')
                    ax.fill_between([V1, V2_calc], [P1, P1], alpha=0.3, color='blue')
                    
                elif proses == "Isokhorik (V konstan)":
                    ax.plot([V1, V1], [P1, P2], 'r-', linewidth=3, label='Isokhorik')
                    
                elif proses == "Isotermal (T konstan)":
                    V_range = np.linspace(V1, V2, 100)
                    P_range = P1 * V1 / V_range
                    ax.plot(V_range, P_range, 'g-', linewidth=3, label='Isotermal')
                    ax.fill_between(V_range, P_range, alpha=0.3, color='green')
                    
                elif proses == "Adiabatik (Q = 0)":
                    V_range = np.linspace(V1, V2, 100)
                    P_range = P1 * (V1/V_range)**gamma
                    ax.plot(V_range, P_range, 'm-', linewidth=3, label='Adiabatik')
                    ax.fill_between(V_range, P_range, alpha=0.3, color='magenta')
                
                ax.scatter([V1, V2], [P1, P2 if 'P2' in locals() else P1], 
                          color='red', s=100, zorder=5)
                ax.set_xlabel('Volume (L)', fontsize=12)
                ax.set_ylabel('Tekanan (atm)', fontsize=12)
                ax.set_title(f'Diagram P-V untuk {proses}', fontsize=14)
                ax.grid(True, alpha=0.3)
                ax.legend(fontsize=12)
                
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"❌ Error dalam perhitungan: {str(e)}")

# === MODE 3: SIKLUS TERMODINAMIKA ===
elif simulation_mode == "Siklus Termodinamika":
    st.header("🔄 Siklus Termodinamika")
    
    cycle_type = st.selectbox("Pilih Siklus", 
        ["Siklus Carnot", "Siklus Otto", "Siklus Brayton", "Siklus Stirling"])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Parameter Siklus")
        n = st.number_input("Jumlah mol (n)", value=1.0, min_value=0.1, max_value=10.0, step=0.1, key="cycle_n")
        
        if cycle_type == "Siklus Carnot":
            T_hot = st.number_input("Suhu Reservoir Panas (K)", value=600.0, min_value=300.0, max_value=1000.0, step=10.0)
            T_cold = st.number_input("Suhu Reservoir Dingin (K)", value=300.0, min_value=200.0, max_value=500.0, step=10.0)
            V1 = st.number_input("Volume titik 1 (L)", value=1.0, min_value=0.1, max_value=10.0, step=0.1, key="carnot_v1")
            V2 = st.number_input("Volume titik 2 (L)", value=2.0, min_value=0.1, max_value=10.0, step=0.1, key="carnot_v2")
            
        elif cycle_type == "Siklus Otto":
            T1 = st.number_input("Suhu Awal (K)", value=300.0, min_value=200.0, max_value=500.0, step=10.0)
            compression_ratio = st.number_input("Rasio Kompresi", value=8.0, min_value=2.0, max_value=15.0, step=0.5)
            Q_in = st.number_input("Kalor Masuk (J)", value=1000.0, min_value=100.0, max_value=5000.0, step=100.0)
            
        gamma = st.number_input("Rasio Panas Spesifik (γ)", value=1.4, min_value=1.1, max_value=1.7, step=0.1, key="cycle_gamma")
        
    with col2:
        st.subheader("📊 Hasil Analisis")
        
        if st.button("🔄 Analisis Siklus", key="analyze_cycle"):
            try:
                if cycle_type == "Siklus Carnot":
                    # Efisiensi Carnot
                    eta_carnot = 1 - T_cold/T_hot
                    
                    # Titik-titik siklus (simplified)
                    P1 = n * R * T_hot / V1
                    P2 = n * R * T_hot / V2
                    V3 = V2 * (T_hot/T_cold)**(1/(gamma-1))
                    V4 = V1 * (T_hot/T_cold)**(1/(gamma-1))
                    P3 = n * R * T_cold / V3
                    P4 = n * R * T_cold / V4
                    
                    # Kerja dan kalor
                    W12 = n * R * T_hot * np.log(V2/V1)  # Ekspansi isotermal
                    W23 = n * R * T_hot / (gamma-1) * (1 - (T_cold/T_hot))  # Ekspansi adiabatik
                    W34 = n * R * T_cold * np.log(V4/V3)  # Kompresi isotermal
                    W41 = n * R * T_cold / (gamma-1) * (1 - (T_hot/T_cold))  # Kompresi adiabatik
                    
                    W_net = W12 + W23 + W34 + W41
                    Q_hot = W12
                    Q_cold = W34
                    
                    st.success(f"**Efisiensi Carnot: {eta_carnot:.3f} ({eta_carnot*100:.1f}%)**")
                    st.info(f"Kerja Net: {W_net:.1f} J")
                    st.info(f"Kalor dari Reservoir Panas: {Q_hot:.1f} J")
                    st.info(f"Kalor ke Reservoir Dingin: {abs(Q_cold):.1f} J")
                    
                elif cycle_type == "Siklus Otto":
                    # Efisiensi Otto
                    eta_otto = 1 - (1/compression_ratio)**(gamma-1)
                    
                    # Proses siklus Otto (simplified)
                    V1 = 1.0  # Volume awal
                    V2 = V1 / compression_ratio  # Volume setelah kompresi
                    
                    T2 = T1 * compression_ratio**(gamma-1)  # Suhu setelah kompresi
                    T3 = T2 + Q_in / (n * R / (gamma-1))  # Suhu setelah pembakaran
                    T4 = T3 / compression_ratio**(gamma-1)  # Suhu setelah ekspansi
                    
                    W_net = eta_otto * Q_in
                    Q_out = Q_in - W_net
                    
                    st.success(f"**Efisiensi Otto: {eta_otto:.3f} ({eta_otto*100:.1f}%)**")
                    st.info(f"Kerja Net: {W_net:.1f} J")
                    st.info(f"Kalor Keluar: {Q_out:.1f} J")
                    
                    # Tabel titik siklus
                    cycle_data = pd.DataFrame({
                        'Titik': ['1 (Awal)', '2 (Kompresi)', '3 (Pembakaran)', '4 (Ekspansi)'],
                        'Volume (L)': [V1, V2, V2, V1],
                        'Suhu (K)': [T1, T2, T3, T4],
                        'Tekanan (atm)': [
                            n * R * T1 / V1,
                            n * R * T2 / V2,
                            n * R * T3 / V2,
                            n * R * T4 / V1
                        ]
                    })
                    
                    st.dataframe(cycle_data, use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Error dalam perhitungan: {str(e)}")

# === MODE 4: PERBANDINGAN GAS ===
elif simulation_mode == "Perbandingan Gas":
    st.header("⚖️ Perbandingan Gas Real vs Ideal")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔧 Parameter")
        n = st.number_input("Jumlah mol (n)", value=1.0, min_value=0.1, max_value=10.0, step=0.1, key="comp_n")
        T_C = st.number_input("Suhu (°C)", value=25.0, min_value=-100.0, max_value=500.0, step=1.0, key="comp_T")
        T = T_C + 273.15
        
        # Parameter Van der Waals
        gas_vdw = st.selectbox("Gas untuk Van der Waals", 
            ["CO₂", "N₂", "O₂", "H₂O", "NH₃"])
        
        vdw_params = {
            "CO₂": {"a": 3.640, "b": 0.04267},
            "N₂": {"a": 1.390, "b": 0.03913},
            "O₂": {"a": 1.360, "b": 0.03183},
            "H₂O": {"a": 5.536, "b": 0.03049},
            "NH₃": {"a": 4.170, "b": 0.03707}
        }
        
        a = vdw_params[gas_vdw]["a"]
        b = vdw_params[gas_vdw]["b"]
        
        V_range = np.linspace(0.1, 5.0, 100)
        
    with col2:
        st.subheader("📈 Perbandingan P-V")
        
        # Hitung tekanan untuk gas ideal dan Van der Waals
        P_ideal = n * R * T / V_range
        P_vdw = []
        
        for V in V_range:
            try:
                P_vdw.append(van_der_waals(T, V, n, a, b))
            except:
                P_vdw.append(np.nan)
        
        P_vdw = np.array(P_vdw)
        
        # Plot perbandingan
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(V_range, P_ideal, 'b-', linewidth=2, label='Gas Ideal')
        ax.plot(V_range, P_vdw, 'r--', linewidth=2, label=f'Van der Waals ({gas_vdw})')
        
        ax.set_xlabel('Volume (L)', fontsize=12)
        ax.set_ylabel('Tekanan (atm)', fontsize=12)
        ax.set_title(f'Perbandingan Gas Ideal vs Van der Waals\n(T = {T:.1f} K, n = {n} mol)', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=12)
        ax.set_ylim(0, 50)
        
        st.pyplot(fig)
        
        # Tabel perbandingan pada volume tertentu
        st.subheader("📊 Perbandingan Numerik")
        
        V_test = [0.5, 1.0, 2.0, 3.0]
        comparison_data = []
        
        for V in V_test:
            P_ideal_val = n * R * T / V
            P_vdw_val = van_der_waals(T, V, n, a, b)
            deviation = abs(P_vdw_val - P_ideal_val) / P_ideal_val * 100
            
            comparison_data.append({
                'Volume (L)': V,
                'P Ideal (atm)': f"{P_ideal_val:.3f}",
                'P Van der Waals (atm)': f"{P_vdw_val:.3f}",
                'Deviasi (%)': f"{deviation:.2f}%"
            })
        
        comparison
