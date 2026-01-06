# ============================================
# FILE: app.py
# Main Dashboard Page
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set matplotlib style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Konfigurasi halaman
st.set_page_config(
    page_title="ML Projects Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .project-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s;
    }
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# ML Dashboard")
    st.markdown("---")
    st.markdown("### Navigation")
    st.info("Gunakan menu di atas untuk navigasi antar halaman")
    
    st.markdown("---")
    st.markdown("### Quick Info")
    st.markdown("""
    **Crop Prediction**: Model ML untuk rekomendasi tanaman
    
    **House Price**: Prediksi harga properti
    
    **Data Analysis**: Visualisasi dan analisis
    """)
    
    st.markdown("---")
    st.markdown("### Developer")
    st.markdown("**Your Name**")
    st.markdown("Email: contact@example.com")
    st.markdown("GitHub: github.com/yourusername")

# Halaman Home
st.markdown('<p class="main-header">Machine Learning Projects Dashboard</p>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 3rem;'>
    <p style='font-size: 1.2rem; color: #666;'>
        Selamat datang di dashboard Machine Learning Projects! 
        <br>Pilih project dari sidebar untuk mulai menggunakan model prediksi.
    </p>
</div>
""", unsafe_allow_html=True)

# Overview Statistics
st.markdown("## Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Projects",
        value="3",
        delta="+1",
        help="Jumlah project yang tersedia"
    )

with col2:
    st.metric(
        label="Models Deployed",
        value="1",
        delta="+1",
        help="Model yang sudah di-deploy"
    )

with col3:
    st.metric(
        label="Avg Accuracy",
        value="95%",
        delta="+2%",
        help="Rata-rata akurasi model"
    )

with col4:
    st.metric(
        label="Predictions",
        value="1,234",
        delta="+89",
        help="Total prediksi yang dilakukan"
    )

st.markdown("---")

# Project Cards
st.markdown("## Available Projects")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='project-card'>
        <h2 style='text-align: center;'>CROP</h2>
        <h3 style='text-align: center;'>Crop Prediction</h3>
        <p style='text-align: center;'>Prediksi rekomendasi tanaman berdasarkan kondisi tanah dan iklim</p>
        <p style='text-align: center; margin-top: 1rem;'>
            <strong>Status:</strong> Active<br>
            <strong>Model:</strong> Random Forest<br>
            <strong>Accuracy:</strong> 95%
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='project-card'>
        <h2 style='text-align: center;'>HOUSE</h2>
        <h3 style='text-align: center;'>House Price Prediction</h3>
        <p style='text-align: center;'>Estimasi harga properti berdasarkan berbagai fitur rumah</p>
        <p style='text-align: center; margin-top: 1rem;'>
            <strong>Status:</strong> Coming Soon<br>
            <strong>Model:</strong> TBD<br>
            <strong>Accuracy:</strong> -
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='project-card'>
        <h2 style='text-align: center;'>DATA</h2>
        <h3 style='text-align: center;'>Data Analysis</h3>
        <p style='text-align: center;'>Visualisasi dan analisis data interaktif</p>
        <p style='text-align: center; margin-top: 1rem;'>
            <strong>Status:</strong> Coming Soon<br>
            <strong>Type:</strong> Visualization<br>
            <strong>Tools:</strong> Matplotlib
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Recent Activity
st.markdown("## Recent Activity")

activity_col1, activity_col2 = st.columns([1, 3])

with activity_col1:
    st.markdown("### Today")
    st.markdown("**5** predictions")
    st.markdown("**12** active users")
    st.markdown("**98%** uptime")
    
with activity_col2:
    # Sample data untuk chart
    activity_data = pd.DataFrame({
        'Time': ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00'],
        'Predictions': [5, 12, 8, 15, 10, 18]
    })
    
    # Create matplotlib chart
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(activity_data['Time'], activity_data['Predictions'], 
            marker='o', linewidth=2, markersize=8, color='#667eea')
    ax.fill_between(activity_data['Time'], activity_data['Predictions'], 
                     alpha=0.3, color='#667eea')
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Predictions', fontsize=12)
    ax.set_title('Predictions Over Time', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# Performance Chart
st.markdown("## Model Performance")

col_perf1, col_perf2 = st.columns(2)

with col_perf1:
    # Bar chart - Model Accuracy
    models_data = pd.DataFrame({
        'Model': ['Random Forest', 'Decision Tree', 'SVM', 'Neural Network'],
        'Accuracy': [95, 88, 91, 93]
    })
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(models_data['Model'], models_data['Accuracy'], color='#764ba2')
    ax.set_xlabel('Accuracy (%)', fontsize=12)
    ax.set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 100)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                f'{width}%', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_perf2:
    # Pie chart - Dataset Distribution
    dataset_data = pd.DataFrame({
        'Category': ['Training', 'Validation', 'Testing'],
        'Percentage': [70, 15, 15]
    })
    
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#667eea', '#764ba2', '#a8a8ff']
    ax.pie(dataset_data['Percentage'], labels=dataset_data['Category'], 
           autopct='%1.1f%%', startangle=90, colors=colors,
           textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('Dataset Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# Instructions
with st.expander("Cara Menggunakan Dashboard"):
    st.markdown("""
    ### Panduan Penggunaan:
    
    1. **Pilih Project** dari sidebar di sebelah kiri
    2. **Input Data** sesuai dengan parameter yang diminta
    3. **Klik Predict** untuk mendapatkan hasil prediksi
    4. **Lihat Visualisasi** dan analisis hasil
    
    ### Tips:
    - Pastikan semua input data valid
    - Gunakan nilai yang realistis untuk hasil terbaik
    - Eksplorasi berbagai kombinasi parameter
    
    ### Troubleshooting:
    - Jika ada error, cek apakah semua dependencies terinstall
    - Pastikan file model ada di folder model/
    - Refresh halaman jika ada masalah
    """)

# System Info
with st.expander("System Info"):
    st.write("**Streamlit Version:**", st.__version__)
    st.write("**Pandas Version:**", pd.__version__)
    st.write("**NumPy Version:**", np.__version__)
    st.write("**Matplotlib Version:**", matplotlib.__version__)
    st.write("**Seaborn Version:**", sns.__version__)
