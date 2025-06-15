import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import linprog
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# Set page config
st.set_page_config(
    page_title="PT TechnoMax Electronics - Operations Research Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏭 PT TechnoMax Electronics</h1>
    <h3>Operations Research Dashboard</h3>
    <p>Optimasi Operasional Terintegrasi</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📋 Navigation")
    st.markdown("Pilih tab untuk mengakses model:")
    st.markdown("- 📈 **Linear Programming**: Optimasi Produksi")
    st.markdown("- 📦 **EOQ Model**: Manajemen Persediaan")
    st.markdown("- ⏱️ **Queueing Model**: Analisis Antrian")
    st.markdown("- 🔢 **Other Models**: Model Tambahan")
    
    st.markdown("---")
    st.markdown("### 🎯 Tujuan")
    st.markdown("Dashboard ini membantu dalam:")
    st.markdown("- Optimasi produksi dan profit")
    st.markdown("- Manajemen persediaan efisien")
    st.markdown("- Analisis kinerja sistem antrian")
    st.markdown("- Perencanaan strategis")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Linear Programming", "📦 EOQ Model", "⏱️ Queueing Model", "🔢 Other Models"])

# TAB 1: LINEAR PROGRAMMING
with tab1:
    st.header("🎯 Optimasi Produksi - Linear Programming")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Parameter Input")
        
        # Product data input
        st.markdown("#### 📱 Data Produk")
        profit_smartphone = st.number_input("Profit Smartphone (Rp)", value=500000, step=10000)
        profit_tablet = st.number_input("Profit Tablet (Rp)", value=750000, step=10000)
        profit_laptop = st.number_input("Profit Laptop (Rp)", value=1200000, step=10000)
        
        st.markdown("#### ⏰ Waktu Produksi (jam/unit)")
        time_smartphone = st.number_input("Waktu Smartphone", value=2.0, step=0.1)
        time_tablet = st.number_input("Waktu Tablet", value=3.0, step=0.1)
        time_laptop = st.number_input("Waktu Laptop", value=4.0, step=0.1)
        
        st.markdown("#### 🏭 Batasan Sumber Daya")
        max_time = st.number_input("Waktu Tersedia (jam/bulan)", value=8000, step=100)
        max_material_a = st.number_input("Bahan Baku A (kg/bulan)", value=2000, step=50)
        max_material_b = st.number_input("Bahan Baku B (kg/bulan)", value=1200, step=50)
        min_smartphone = st.number_input("Min Smartphone", value=500, step=10)
        max_laptop = st.number_input("Max Laptop", value=800, step=10)
    
    with col2:
        st.subheader("📊 Hasil Optimasi")
        
        # Material usage per unit
        material_a = [0.5, 0.8, 1.2]  # Smartphone, Tablet, Laptop
        material_b = [0.3, 0.4, 0.6]
        
        # Optimization using scipy.optimize.linprog
        # Coefficients (negative because linprog minimizes)
        c = [-profit_smartphone, -profit_tablet, -profit_laptop]
        
        # Constraint matrix A_ub * x <= b_ub
        A_ub = [
            [time_smartphone, time_tablet, time_laptop],  # Time constraint
            [material_a[0], material_a[1], material_a[2]],  # Material A
            [material_b[0], material_b[1], material_b[2]],  # Material B
            [0, 0, 1],  # Max laptop
            [-1, 0, 0]  # Min smartphone (converted to negative)
        ]
        
        b_ub = [max_time, max_material_a, max_material_b, max_laptop, -min_smartphone]
        
        # Bounds
        bounds = [(0, None), (0, None), (0, None)]
        
        # Solve
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        
        if result.success:
            x1, x2, x3 = result.x
            max_profit = -result.fun
            
            # Display results
            st.markdown("#### 🎯 Solusi Optimal")
            
            col2_1, col2_2, col2_3 = st.columns(3)
            with col2_1:
                st.metric("📱 Smartphone", f"{int(x1):,} unit")
            with col2_2:
                st.metric("📱 Tablet", f"{int(x2):,} unit")
            with col2_3:
                st.metric("💻 Laptop", f"{int(x3):,} unit")
            
            st.markdown("#### 💰 Profit Maksimal")
            st.success(f"**Rp {max_profit:,.0f}** per bulan")
            
            # Resource utilization
            st.markdown("#### 📈 Utilisasi Sumber Daya")
            time_used = x1*time_smartphone + x2*time_tablet + x3*time_laptop
            material_a_used = x1*material_a[0] + x2*material_a[1] + x3*material_a[2]
            material_b_used = x1*material_b[0] + x2*material_b[1] + x3*material_b[2]
            
            utilization_data = {
                'Sumber Daya': ['Waktu Produksi', 'Bahan Baku A', 'Bahan Baku B'],
                'Digunakan': [time_used, material_a_used, material_b_used],
                'Tersedia': [max_time, max_material_a, max_material_b],
                'Utilisasi (%)': [
                    (time_used/max_time)*100,
                    (material_a_used/max_material_a)*100,
                    (material_b_used/max_material_b)*100
                ]
            }
            
            df_util = pd.DataFrame(utilization_data)
            st.dataframe(df_util.round(2))
            
            # Visualization
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Digunakan',
                x=df_util['Sumber Daya'],
                y=df_util['Digunakan'],
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                name='Tersedia',
                x=df_util['Sumber Daya'],
                y=df_util['Tersedia'],
                marker_color='lightcoral'
            ))
            fig.update_layout(
                title='Utilisasi Sumber Daya',
                barmode='group',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.error("❌ Optimasi gagal. Periksa kembali batasan-batasan yang diberikan.")

# TAB 2: EOQ MODEL
with tab2:
    st.header("📦 Model Persediaan - Economic Order Quantity (EOQ)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Parameter Input")
        
        annual_demand = st.number_input("Permintaan Tahunan (D)", value=24000, step=1000)
        ordering_cost = st.number_input("Biaya Pemesanan (S) - Rp", value=200000, step=10000)
        holding_cost = st.number_input("Biaya Penyimpanan (H) - Rp/unit/tahun", value=50000, step=5000)
        unit_cost = st.number_input("Harga per Unit - Rp", value=500000, step=10000)
        lead_time_days = st.number_input("Lead Time (hari)", value=14, step=1)
        std_demand = st.number_input("Std Deviasi Permintaan (Lead Time)", value=100, step=10)
        service_level = st.slider("Service Level (%)", min_value=80, max_value=99, value=95) / 100
        
        # Z-score table (simplified)
        z_scores = {0.80: 0.84, 0.85: 1.04, 0.90: 1.28, 0.95: 1.645, 0.975: 1.96, 0.99: 2.33}
        z_value = z_scores.get(service_level, 1.645)
    
    with col2:
        st.subheader("📊 Hasil Analisis EOQ")
        
        # EOQ Calculation
        eoq = math.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
        
        # Other calculations
        order_frequency = annual_demand / eoq
        order_interval = 365 / order_frequency
        total_ordering_cost = (annual_demand / eoq) * ordering_cost
        total_holding_cost = (eoq / 2) * holding_cost
        total_inventory_cost = total_ordering_cost + total_holding_cost
        
        # Safety stock and Reorder Point
        daily_demand = annual_demand / 365
        safety_stock = z_value * std_demand
        reorder_point = (daily_demand * lead_time_days) + safety_stock
        
        # Display results
        st.markdown("#### 🎯 EOQ Optimal")
        
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.metric("📦 EOQ", f"{eoq:.0f} unit")
            st.metric("📅 Frekuensi Pesan", f"{order_frequency:.0f} kali/tahun")
            st.metric("⏰ Interval Pesan", f"{order_interval:.0f} hari")
        
        with col2_2:
            st.metric("🛡️ Safety Stock", f"{safety_stock:.0f} unit")
            st.metric("🔄 Reorder Point", f"{reorder_point:.0f} unit")
            st.metric("📊 Service Level", f"{service_level*100:.0f}%")
        
        st.markdown("#### 💰 Analisis Biaya")
        cost_data = {
            'Jenis Biaya': ['Biaya Pemesanan', 'Biaya Penyimpanan', 'Total Biaya'],
            'Biaya (Rp)': [total_ordering_cost, total_holding_cost, total_inventory_cost]
        }
        df_cost = pd.DataFrame(cost_data)
        st.dataframe(df_cost.style.format({'Biaya (Rp)': 'Rp {:,.0f}'}))
        
        # EOQ Chart
        st.markdown("#### 📈 Grafik Biaya EOQ")
        
        q_range = np.linspace(100, eoq*2, 100)
        ordering_costs = (annual_demand / q_range) * ordering_cost
        holding_costs = (q_range / 2) * holding_cost
        total_costs = ordering_costs + holding_costs
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=q_range, y=ordering_costs, name='Biaya Pemesanan', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=q_range, y=holding_costs, name='Biaya Penyimpanan', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=q_range, y=total_costs, name='Total Biaya', line=dict(color='green', width=3)))
        fig.add_vline(x=eoq, line_dash="dash", line_color="black", annotation_text=f"EOQ = {eoq:.0f}")
        
        fig.update_layout(
            title='Grafik Biaya EOQ',
            xaxis_title='Kuantitas Pemesanan (Q)',
            yaxis_title='Biaya (Rp)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: QUEUEING MODEL
with tab3:
    st.header("⏱️ Model Antrian - M/M/1 Queue")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Parameter Input")
        
        arrival_rate = st.number_input("Tingkat Kedatangan (λ) - per jam", value=15.0, step=0.5)
        service_rate = st.number_input("Tingkat Pelayanan (μ) - per jam", value=20.0, step=0.5)
        operating_hours = st.number_input("Jam Operasi per Hari", value=8, step=1)
        operating_days = st.number_input("Hari Operasi per Bulan", value=25, step=1)
        waiting_cost = st.number_input("Biaya Menunggu (Rp/jam/unit)", value=100000, step=10000)
        service_cost = st.number_input("Biaya Pelayanan (Rp/jam)", value=200000, step=10000)
    
    with col2:
        st.subheader("📊 Analisis Sistem Antrian")
        
        if service_rate > arrival_rate:
            # System parameters
            rho = arrival_rate / service_rate  # Utilization
            
            # Performance measures
            L = arrival_rate / (service_rate - arrival_rate)  # Average number in system
            Lq = (arrival_rate ** 2) / (service_rate * (service_rate - arrival_rate))  # Average number in queue
            W = 1 / (service_rate - arrival_rate)  # Average time in system
            Wq = arrival_rate / (service_rate * (service_rate - arrival_rate))  # Average time in queue
            P0 = 1 - rho  # Probability system is empty
            
            # Display results
            st.markdown("#### 🎯 Kinerja Sistem")
            
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                st.metric("📊 Utilisasi (ρ)", f"{rho:.3f}")
                st.metric("👥 Jumlah dalam Sistem (L)", f"{L:.2f}")
                st.metric("⏰ Waktu dalam Sistem (W)", f"{W*60:.1f} menit")
            
            with col2_2:
                st.metric("🔄 Probabilitas Kosong (P₀)", f"{P0:.3f}")
                st.metric("📋 Jumlah dalam Antrian (Lq)", f"{Lq:.2f}")
                st.metric("⌛ Waktu dalam Antrian (Wq)", f"{Wq*60:.1f} menit")
            
            # Cost Analysis
            st.markdown("#### 💰 Analisis Biaya")
            hourly_waiting_cost = L * waiting_cost
            total_hourly_cost = hourly_waiting_cost + service_cost
            daily_cost = total_hourly_cost * operating_hours
            monthly_cost = daily_cost * operating_days
            
            cost_summary = {
                'Periode': ['Per Jam', 'Per Hari', 'Per Bulan'],
                'Biaya Menunggu': [hourly_waiting_cost, hourly_waiting_cost * operating_hours, 
                                 hourly_waiting_cost * operating_hours * operating_days],
                'Biaya Pelayanan': [service_cost, service_cost * operating_hours, 
                                  service_cost * operating_hours * operating_days],
                'Total Biaya': [total_hourly_cost, daily_cost, monthly_cost]
            }
            
            df_cost_queue = pd.DataFrame(cost_summary)
            st.dataframe(df_cost_queue.style.format({
                'Biaya Menunggu': 'Rp {:,.0f}',
                'Biaya Pelayanan': 'Rp {:,.0f}',
                'Total Biaya': 'Rp {:,.0f}'
            }))
            
            # Probability Distribution
            st.markdown("#### 📈 Distribusi Probabilitas")
            
            n_values = list(range(0, 11))
            probabilities = [P0 * (rho ** n) for n in n_values]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=n_values,
                y=probabilities,
                name='P(n)',
                marker_color='lightblue'
            ))
            fig.update_layout(
                title='Probabilitas n Pelanggan dalam Sistem',
                xaxis_title='Jumlah Pelanggan (n)',
                yaxis_title='Probabilitas P(n)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # System Performance Metrics Table
            st.markdown("#### 📋 Ringkasan Metrik Kinerja")
            metrics_data = {
                'Metrik': ['Tingkat Kedatangan (λ)', 'Tingkat Pelayanan (μ)', 'Utilisasi (ρ)',
                          'Rata-rata dalam Sistem (L)', 'Rata-rata dalam Antrian (Lq)',
                          'Waktu dalam Sistem (W)', 'Waktu dalam Antrian (Wq)',
                          'Probabilitas Sistem Kosong (P₀)'],
                'Nilai': [f"{arrival_rate:.1f} /jam", f"{service_rate:.1f} /jam", f"{rho:.3f}",
                         f"{L:.2f}", f"{Lq:.2f}", f"{W*60:.1f} menit", f"{Wq*60:.1f} menit", f"{P0:.3f}"],
                'Interpretasi': ['Kedatangan pelanggan', 'Kapasitas pelayanan', 'Tingkat kesibukan',
                               'Pelanggan rata-rata', 'Antrian rata-rata', 'Lama total proses',
                               'Lama menunggu', 'Sistem tidak sibuk']
            }
            
            df_metrics = pd.DataFrame(metrics_data)
            st.dataframe(df_metrics)
            
        else:
            st.error("⚠️ Sistem tidak stabil! Tingkat pelayanan (μ) harus lebih besar dari tingkat kedatangan (λ)")

# TAB 4: OTHER MODELS
with tab4:
    st.header("🔢 Model Matematika Lainnya")
    
    # Sub-tabs for different models
    subtab1, subtab2, subtab3 = st.tabs(["🚚 Model Transportasi", "👷 Model Penugasan", "📊 Forecasting"])
    
    with subtab1:
        st.subheader("🚚 Model Transportasi")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 🏭 Data Pabrik dan Distribusi")
            
            # Supply data
            supply_1 = st.number_input("Kapasitas Pabrik 1", value=1000, step=50)
            supply_2 = st.number_input("Kapasitas Pabrik 2", value=1500, step=50)
            supply_3 = st.number_input("Kapasitas Pabrik 3", value=1200, step=50)
            
            # Demand data
            demand_1 = st.number_input("Permintaan DC 1", value=800, step=50)
            demand_2 = st.number_input("Permintaan DC 2", value=900, step=50)
            demand_3 = st.number_input("Permintaan DC 3", value=700, step=50)
            demand_4 = st.number_input("Permintaan DC 4", value=500, step=50)
        
        with col2:
            st.markdown("#### 💰 Matriks Biaya Transportasi (Rp/unit)")
            
            # Cost matrix input
            cost_data = []
            for i in range(3):
                row = []
                cols = st.columns(4)
                for j in range(4):
                    default_costs = [[8000, 6000, 10000, 9000],
                                   [9000, 7000, 8000, 7000],
                                   [7000, 8000, 6000, 10000]]
                    with cols[j]:
                        cost = st.number_input(f"P{i+1}→DC{j+1}", value=default_costs[i][j], step=500, key=f"cost_{i}_{j}")
                        row.append(cost)
                cost_data.append(row)
            
            # Display cost matrix
            cost_df = pd.DataFrame(cost_data, 
                                 columns=['DC 1', 'DC 2', 'DC 3', 'DC 4'],
                                 index=['Pabrik 1', 'Pabrik 2', 'Pabrik 3'])
            st.markdown("#### 📋 Matriks Biaya")
            st.dataframe(cost_df.style.format('Rp {:,.0f}'))
            
            # Check balance
            total_supply = supply_1 + supply_2 + supply_3
            total_demand = demand_1 + demand_2 + demand_3 + demand_4
            
            if total_supply == total_demand:
                st.success(f"✅ Balanced Problem: Supply = Demand = {total_supply:,} unit")
            else:
                st.warning(f"⚠️ Unbalanced Problem: Supply = {total_supply:,}, Demand = {total_demand:,}")
    
    with subtab2:
        st.subheader("👷 Model Penugasan")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### ⏰ Matriks Waktu Penyelesaian (jam)")
            
            # Assignment matrix input
            assignment_data = []
            default_times = [[8, 6, 2, 4],
                           [5, 7, 9, 3],
                           [4, 2, 6, 5],
                           [3, 8, 7, 6]]
            
            for i in range(4):
                row = []
                cols = st.columns(4)
                for j in range(4):
                    with cols[j]:
                        time = st.number_input(f"T{i+1}→M{j+1}", value=default_times[i][j], step=1, key=f"assign_{i}_{j}")
                        row.append(time)
                assignment_data.append(row)
        
        with col2:
            # Display assignment matrix
            assign_df = pd.DataFrame(assignment_data,
                                   columns=['Mesin A', 'Mesin B', 'Mesin C', 'Mesin D'],
                                   index=['Teknisi 1', 'Teknisi 2', 'Teknisi 3', 'Teknisi 4'])
            st.markdown("#### 📋 Matriks Waktu")
            st.dataframe(assign_df.style.format('{:.0f} jam'))
            
            # Hungarian Algorithm (simplified demonstration)
            st.markdown("#### 🎯 Solusi Optimal (Heuristik)")
            
            # Simple greedy assignment for demonstration
            min_times = []
            assignments = []
            available_machines = list(range(4))
            
            for i in range(4):
                min_time = float('inf')
                best_machine = -1
                for j in available_machines:
                    if assignment_data[i][j] < min_time:
                        min_time = assignment_data[i][j]
                        best_machine = j
                
                min_times.append(min_time)
                assignments.append(best_machine)
                available_machines.remove(best_machine)
            
            total_time = sum(min_times)
            
            assignment_result = {
                'Teknisi': [f'Teknisi {i+1}' for i in range(4)],
                'Mesin': [f'Mesin {chr(65+assignments[i])}' for i in range(4)],
                'Waktu': min_times
            }
            
            result_df = pd.DataFrame(assignment_result)
            st.dataframe(result_df)
            st.success(f"⏰ Total Waktu Optimal: {total_time} jam")
    
    with subtab3:
        st.subheader("📊 Model Forecasting")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📈 Data Penjualan Historis")
            
            # Historical data input
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des']
            
            sales_data = []
            default_sales = [1200, 1350, 1500, 1400, 1600, 1650,
                           1800, 1750, 1900, 2100, 2200, 2000]
            
            for i, month in enumerate(months):
                sales = st.number_input(f"Penjualan {month}", value=default_sales[i], step=50, key=f"sales_{i}")
                sales_data.append(sales)
        
        with col2:
            st.markdown("#### 📊 Analisis Trend")
            
            # Linear regression
            x = np.array(range(1, 13))
            y = np.array(sales_data)
            
            # Calculate linear trend
            n = len(x)
            sum_x = np.sum(x)
            sum_y = np.sum(y)
            sum_xy = np.sum(x * y)
            sum_x2 = np.sum(x ** 2)
            
            b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
            a = (sum_y - b * sum_x) / n
            
            # Correlation coefficient
            mean_x = np.mean(x)
            mean_y = np.mean(y)
            
            numerator = np.sum((x - mean_x) * (y - mean_y))
            denominator = np.sqrt(np.sum((x - mean_x) ** 2) * np.sum((y - mean_y) ** 2))
            r = numerator / denominator
            
            st.metric("📈 Slope (b)", f"{b:.2f}")
            st.metric("📊 Intercept (a)", f"{a:.2f}")
            st.metric("🎯 Korelasi (r)", f"{r:.3f}")
            
            # Forecast next 6 months
            st.markdown("#### 🔮 Proyeksi 6 Bulan")
            
            forecast_months = []
            forecast_values = []
            
            for i in range(13, 19):
                forecast = a + b * i
                forecast_months.append(f"Bulan {i}")
                forecast_values.append(int(forecast))
            
            forecast_df = pd.DataFrame({
                'Periode': forecast_months,
                'Proyeksi': forecast_values
            })
            
            st.dataframe(forecast_df.style.format({'Proyeksi': '{:,} unit'}))
            
            # Visualization
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=months,
                y=sales_data,
                mode='lines+markers',
                name='Data Historis',
                line=dict(color='blue')
            ))
            
            # Trend line
            trend_line = [a + b
