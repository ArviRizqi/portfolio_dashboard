# ============================================
# FILE: pages/1_🌾_Crop_Prediction.py
# Letakkan di folder: pages/
# ============================================

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Crop Prediction", page_icon="🌾", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌾 Prediksi Rekomendasi Tanaman")
st.markdown("---")

# Info Model
with st.expander("ℹ️ Tentang Model", expanded=False):
    st.write("""
    Model ini menggunakan **Random Forest Classifier** untuk merekomendasikan tanaman 
    yang paling cocok berdasarkan kondisi tanah dan iklim.
    
    **Parameter Input:**
    - **N, P, K**: Kandungan Nitrogen, Fosfor, dan Kalium dalam tanah
    - **Temperature**: Suhu rata-rata dalam Celsius (°C)
    - **Humidity**: Kelembaban relatif dalam persen (%)
    - **pH**: Tingkat keasaman tanah
    - **Rainfall**: Curah hujan dalam milimeter (mm)
    
    **Akurasi Model**: ~95%
    **Algoritma**: Random Forest Classifier
    **Total Classes**: 22 jenis tanaman
    """)

# Form Input
col1, col2 = st.columns(2)

feature_order = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

feature_info = {
    'N': {'label': 'Nitrogen (N)', 'hint': 'Kandungan Nitrogen', 'example': '90', 'min': 0.0, 'max': 140.0},
    'P': {'label': 'Fosfor (P)', 'hint': 'Kandungan Fosfor', 'example': '42', 'min': 5.0, 'max': 145.0},
    'K': {'label': 'Kalium (K)', 'hint': 'Kandungan Kalium', 'example': '43', 'min': 5.0, 'max': 205.0},
    'ph': {'label': 'pH Tanah', 'hint': 'Tingkat keasaman tanah', 'example': '6.5', 'min': 3.5, 'max': 9.5},
    'temperature': {'label': 'Temperature (°C)', 'hint': 'Suhu rata-rata', 'example': '20.8', 'min': 8.0, 'max': 44.0},
    'humidity': {'label': 'Humidity (%)', 'hint': 'Kelembaban relatif', 'example': '82.0', 'min': 14.0, 'max': 100.0},
    'rainfall': {'label': 'Rainfall (mm)', 'hint': 'Curah hujan', 'example': '202.9', 'min': 20.0, 'max': 300.0}
}

inputs = {}

with col1:
    st.markdown("#### 🧪 Nutrisi Tanah")
    for feature in ['N', 'P', 'K', 'ph']:
        info = feature_info[feature]
        inputs[feature] = st.number_input(
            info['label'],
            min_value=info['min'],
            max_value=info['max'],
            value=0.0,
            step=0.1,
            help=f"{info['hint']}. Contoh: {info['example']}"
        )

with col2:
    st.markdown("#### 🌤️ Kondisi Iklim")
    for feature in ['temperature', 'humidity', 'rainfall']:
        info = feature_info[feature]
        inputs[feature] = st.number_input(
            info['label'],
            min_value=info['min'],
            max_value=info['max'],
            value=0.0,
            step=0.1,
            help=f"{info['hint']}. Contoh: {info['example']}"
        )

st.markdown("---")

# Quick Fill Buttons (Contoh data untuk testing)
st.markdown("#### 🎯 Quick Fill Examples")
col_ex1, col_ex2, col_ex3 = st.columns(3)

with col_ex1:
    if st.button("🌾 Example: Rice"):
        st.session_state.example = "rice"

with col_ex2:
    if st.button("🌽 Example: Corn"):
        st.session_state.example = "corn"

with col_ex3:
    if st.button("☕ Example: Coffee"):
        st.session_state.example = "coffee"

# Apply example data
if 'example' in st.session_state:
    if st.session_state.example == "rice":
        inputs = {'N': 80, 'P': 40, 'K': 40, 'temperature': 25, 'humidity': 80, 'ph': 6.5, 'rainfall': 200}
    elif st.session_state.example == "corn":
        inputs = {'N': 70, 'P': 50, 'K': 20, 'temperature': 22, 'humidity': 65, 'ph': 6.0, 'rainfall': 100}
    elif st.session_state.example == "coffee":
        inputs = {'N': 100, 'P': 20, 'K': 30, 'temperature': 23, 'humidity': 70, 'ph': 6.5, 'rainfall': 150}
    st.rerun()

st.markdown("---")

# Tombol Prediksi
col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    predict_button = st.button('🔮 Prediksi Tanaman', use_container_width=True)

if predict_button:
    if all(inputs[key] == 0.0 for key in feature_order):
        st.warning("⚠️ Mohon masukkan nilai untuk setidaknya satu parameter!")
    else:
        try:
            with st.spinner('🔄 Memproses prediksi...'):
                # Load model
                model = joblib.load('model/rf_model.pkl')
                scaler = joblib.load('model/scaler.pkl')
                label_encoder = joblib.load('model/label_encoder.pkl')
                
                # Prepare data
                features = [float(inputs[key]) for key in feature_order]
                features_scaled = scaler.transform([features])
                
                # Predict
                prediction = model.predict(features_scaled)
                predicted_label = label_encoder.inverse_transform(prediction)[0]
                
                # Get confidence
                if hasattr(model, 'predict_proba'):
                    probabilities = model.predict_proba(features_scaled)[0]
                    confidence = np.max(probabilities) * 100
                    
                    # Get top 3 predictions
                    top_3_idx = np.argsort(probabilities)[-3:][::-1]
                    top_3_labels = label_encoder.inverse_transform(top_3_idx)
                    top_3_probs = probabilities[top_3_idx] * 100
                else:
                    confidence = 95.0
                    top_3_labels = [predicted_label]
                    top_3_probs = [95.0]
                
                # Display Results
                st.markdown("---")
                st.markdown("### 🎯 Hasil Prediksi")
                
                result_col1, result_col2 = st.columns([2, 1])
                
                with result_col1:
                    st.success(f"### 🌾 Tanaman yang Direkomendasikan: **{predicted_label}**")
                    st.info(f"📊 Tingkat Kepercayaan: **{confidence:.2f}%**")
                    
                    # Top 3 predictions
                    st.markdown("#### 🏆 Top 3 Rekomendasi:")
                    for i, (label, prob) in enumerate(zip(top_3_labels, top_3_probs), 1):
                        st.markdown(f"{i}. **{label}** - {prob:.2f}%")
                    
                    if confidence > 90:
                        st.balloons()
                
                with result_col2:
                    # Gauge chart
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=confidence,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Confidence"},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 75], 'color': "gray"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Visualizations
                st.markdown("### 📊 Visualisasi Parameter Input")
                
                viz_col1, viz_col2 = st.columns(2)
                
                with viz_col1:
                    # Nutrient Bar Chart
                    nutrient_data = pd.DataFrame({
                        'Nutrient': ['Nitrogen', 'Fosfor', 'Kalium'],
                        'Value': [inputs['N'], inputs['P'], inputs['K']]
                    })
                    fig_nutrient = px.bar(
                        nutrient_data,
                        x='Nutrient',
                        y='Value',
                        title='Kandungan Nutrisi Tanah',
                        color='Value',
                        color_continuous_scale='Viridis',
                        text='Value'
                    )
                    fig_nutrient.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                    fig_nutrient.update_layout(showlegend=False, height=300)
                    st.plotly_chart(fig_nutrient, use_container_width=True)
                
                with viz_col2:
                    # Climate Bar Chart
                    climate_data = pd.DataFrame({
                        'Parameter': ['Temperature', 'Humidity', 'Rainfall'],
                        'Value': [inputs['temperature'], inputs['humidity'], inputs['rainfall']]
                    })
                    fig_climate = px.bar(
                        climate_data,
                        x='Parameter',
                        y='Value',
                        title='Kondisi Iklim',
                        color='Value',
                        color_continuous_scale='RdYlBu',
                        text='Value'
                    )
                    fig_climate.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                    fig_climate.update_layout(showlegend=False, height=300)
                    st.plotly_chart(fig_climate, use_container_width=True)
                
                # Radar Chart - All Parameters
                st.markdown("### 🎯 Radar Chart - Semua Parameter")
                
                # Normalize values for radar chart
                radar_data = pd.DataFrame({
                    'Parameter': list(feature_info.keys()),
                    'Value': [inputs[key] for key in feature_order],
                    'Max': [feature_info[key]['max'] for key in feature_order]
                })
                radar_data['Normalized'] = (radar_data['Value'] / radar_data['Max']) * 100
                
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=radar_data['Normalized'].tolist() + [radar_data['Normalized'].iloc[0]],
                    theta=radar_data['Parameter'].tolist() + [radar_data['Parameter'].iloc[0]],
                    fill='toself',
                    name='Input Values'
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig_radar, use_container_width=True)
                
        except FileNotFoundError:
            st.error("❌ File model tidak ditemukan! Pastikan file model tersimpan di folder 'model/'")
            st.info("📁 Struktur folder yang diperlukan:\n```\nproject/\n├── model/\n│   ├── rf_model.pkl\n│   ├── scaler.pkl\n│   └── label_encoder.pkl\n```")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {str(e)}")
            st.info("💡 Pastikan model telah di-train dan disimpan dengan benar.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 <strong>Tips:</strong> Gunakan nilai yang sesuai dengan kondisi lahan Anda untuk hasil prediksi yang optimal.</p>
</div>
""", unsafe_allow_html=True)
