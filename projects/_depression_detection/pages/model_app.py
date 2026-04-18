# projects/_crop_recomendation/pages/model_app.py

import streamlit as st
import numpy as np
import sys, os, warnings
warnings.filterwarnings("ignore")
from pathlib import Path

# Resolve path
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from shared.utils import section_header

# ── Paths ────────────────────────────────────────────────────────────────────
BASE      = str(CURRENT_DIR)
RF_PATH   = os.path.join(BASE, "../models/rf_model.pkl")
SC_PATH   = os.path.join(BASE, "../models/scaler.pkl")
LE_PATH   = os.path.join(BASE, "../models/label_encoder.pkl")

FEATURES  = ["N", "P", "K", "Temperature", "Humidity", "ph", "Rainfall"]

# Emoji per tanaman
CROP_EMOJI = {
    "apple": "🍎", "banana": "🍌", "blackgram": "🫘", "chickpea": "🫘",
    "coconut": "🥥", "coffee": "☕", "cotton": "🌿", "grapes": "🍇",
    "jute": "🌾", "kidneybeans": "🫘", "lentil": "🫘", "maize": "🌽",
    "mango": "🥭", "mothbeans": "🫘", "mungbean": "🫘", "muskmelon": "🍈",
    "orange": "🍊", "papaya": "🍈", "pigeonpeas": "🫘", "pomegranate": "🍎",
    "rice": "🍚", "watermelon": "🍉",
}

# Range min-max dari dataset (untuk slider)
FEATURE_CONFIG = {
    "N":           {"label": "Nitrogen (N)",             "min": 0,    "max": 140,  "step": 1,    "default": 50,   "unit": "kg/ha"},
    "P":           {"label": "Phosphorus (P)",           "min": 5,    "max": 145,  "step": 1,    "default": 53,   "unit": "kg/ha"},
    "K":           {"label": "Potassium (K)",            "min": 5,    "max": 205,  "step": 1,    "default": 48,   "unit": "kg/ha"},
    "Temperature": {"label": "Suhu (Temperature)",       "min": 8.0,  "max": 43.0, "step": 0.1,  "default": 25.0, "unit": "°C"},
    "Humidity":    {"label": "Kelembapan (Humidity)",    "min": 14.0, "max": 100.0,"step": 0.1,  "default": 71.0, "unit": "%"},
    "ph":          {"label": "Keasaman Tanah (pH)",      "min": 3.5,  "max": 9.9,  "step": 0.01, "default": 6.5,  "unit": ""},
    "Rainfall":    {"label": "Curah Hujan (Rainfall)",   "min": 20.0, "max": 300.0,"step": 0.1,  "default": 103.0,"unit": "mm"},
}


@st.cache_resource
def load_pipeline():
    import joblib
    rf     = joblib.load(RF_PATH)
    scaler = joblib.load(SC_PATH)
    le     = joblib.load(LE_PATH)
    return rf, scaler, le


def render():
    section_header("🌾 Crop Recommendation — Model App",
                   "Masukkan kondisi tanah & iklim untuk mendapatkan rekomendasi tanaman "
                   "menggunakan pipeline Random Forest yang sudah dilatih.")

    rf, scaler, le = load_pipeline()

    st.markdown("#### 🎛️ Input Kondisi Lahan")
    st.caption("Geser slider sesuai kondisi lahan Anda, lalu klik **Prediksi**.")

    # ── Input form dengan slider ──────────────────────────────────────────
    col1, col2 = st.columns(2)
    inputs = {}

    feature_list = list(FEATURE_CONFIG.items())
    for i, (feat, cfg) in enumerate(feature_list):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            val = st.slider(
                label=f"**{cfg['label']}**" + (f" ({cfg['unit']})" if cfg['unit'] else ""),
                min_value=float(cfg["min"]),
                max_value=float(cfg["max"]),
                value=float(cfg["default"]),
                step=float(cfg["step"]),
                key=f"input_{feat}"
            )
            inputs[feat] = val

    st.markdown("---")

    # ── Tombol prediksi ───────────────────────────────────────────────────
    col_btn, col_space = st.columns([1, 3])
    with col_btn:
        predict_btn = st.button("🔍 Prediksi Tanaman", use_container_width=True, type="primary")

    if predict_btn:
        feature_values = [inputs[f] for f in FEATURES]

        # Scale menggunakan scaler dari pipeline
        features_scaled = scaler.transform([feature_values])

        # Prediksi label + probabilitas
        prediction    = rf.predict(features_scaled)
        probabilities = rf.predict_proba(features_scaled)[0]
        crop_label    = le.inverse_transform(prediction)[0]

        # Susun top-5 probabilitas
        prob_df = sorted(
            zip(le.classes_, probabilities),
            key=lambda x: x[1], reverse=True
        )[:5]

        # ── Hasil utama ───────────────────────────────────────────────────
        st.markdown("---")
        emoji = CROP_EMOJI.get(crop_label, "🌱")
        confidence = probabilities[prediction[0]] * 100

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0f766e, #1e3a5f);
            border-radius: 14px;
            padding: 2rem;
            text-align: center;
            color: white;
            margin-bottom: 1.5rem;
        ">
            <div style="font-size: 4rem;">{emoji}</div>
            <div style="font-size: 1rem; opacity: 0.8; margin-top: 0.5rem;">Rekomendasi Tanaman</div>
            <div style="font-size: 2.5rem; font-weight: 800; text-transform: capitalize;">
                {crop_label}
            </div>
            <div style="font-size: 1rem; opacity: 0.85; margin-top: 0.5rem;">
                Confidence: <strong>{confidence:.1f}%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Top-5 probabilitas ────────────────────────────────────────────
        st.markdown("##### 📊 Top 5 Kemungkinan Tanaman")
        for i, (crop, prob) in enumerate(prob_df):
            pct = prob * 100
            bar_color = "#0ea5e9" if i == 0 else "#94a3b8"
            em = CROP_EMOJI.get(crop, "🌱")
            st.markdown(f"""
            <div style="display:flex; align-items:center; margin-bottom:0.5rem; gap:0.75rem;">
                <div style="width:1.5rem; text-align:center;">{em}</div>
                <div style="width:130px; font-size:0.9rem; text-transform:capitalize;">
                    {'<strong>' if i==0 else ''}{crop}{'</strong>' if i==0 else ''}
                </div>
                <div style="flex:1; background:#e2e8f0; border-radius:999px; height:10px;">
                    <div style="width:{pct:.1f}%; background:{bar_color};
                                border-radius:999px; height:10px;"></div>
                </div>
                <div style="width:50px; font-size:0.85rem; text-align:right;">
                    {pct:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Ringkasan input ───────────────────────────────────────────────
        with st.expander("📋 Lihat detail input yang digunakan"):
            import pandas as pd
            input_df = pd.DataFrame({
                "Fitur":  [FEATURE_CONFIG[f]["label"] for f in FEATURES],
                "Nilai":  [f"{inputs[f]:.2f}" for f in FEATURES],
                "Satuan": [FEATURE_CONFIG[f]["unit"] for f in FEATURES],
            })
            st.dataframe(input_df, use_container_width=True, hide_index=True)