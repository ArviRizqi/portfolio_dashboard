# projects/_house_prediction/pages/model_app.py

import streamlit as st
import pandas as pd
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

MODEL_DIR = CURRENT_DIR.parent / "models"
GB_PATH   = str(MODEL_DIR / "gb_model.pkl")
SC_PATH   = str(MODEL_DIR / "scaler_house.pkl")

# Fitur yang digunakan pipeline (urutan harus sama persis saat training)
FEATURE_COLS = [
    'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
    'waterfront', 'view', 'condition', 'grade', 'sqft_above',
    'sqft_basement', 'sqft_living15', 'sqft_lot15', 'lat', 'long',
    'house_age', 'is_renovated', 'renovated_age', 'sqft_ratio',
    'total_rooms', 'basement_flag', 'sqft_living_log',
]

# Konfigurasi slider input (hanya fitur yang bisa diinput user)
INPUT_CONFIG = {
    'bedrooms':      {'label': 'Kamar Tidur',           'min': 0,    'max': 10,     'step': 1,    'default': 3,    'unit': ''},
    'bathrooms':     {'label': 'Kamar Mandi',           'min': 0.5,  'max': 8.0,    'step': 0.5,  'default': 2.0,  'unit': ''},
    'sqft_living':   {'label': 'Luas Bangunan',         'min': 300,  'max': 10000,  'step': 50,   'default': 1800, 'unit': 'sqft'},
    'sqft_lot':      {'label': 'Luas Lahan',            'min': 500,  'max': 100000, 'step': 500,  'default': 7000, 'unit': 'sqft'},
    'floors':        {'label': 'Jumlah Lantai',         'min': 1.0,  'max': 3.5,    'step': 0.5,  'default': 1.0,  'unit': ''},
    'waterfront':    {'label': 'Menghadap Air (Waterfront)', 'min': 0, 'max': 1,    'step': 1,    'default': 0,    'unit': ''},
    'view':          {'label': 'Skor Pemandangan (0–4)','min': 0,    'max': 4,      'step': 1,    'default': 0,    'unit': ''},
    'condition':     {'label': 'Kondisi Fisik (1–5)',   'min': 1,    'max': 5,      'step': 1,    'default': 3,    'unit': ''},
    'grade':         {'label': 'Grade Konstruksi (1–13)','min': 1,   'max': 13,     'step': 1,    'default': 7,    'unit': ''},
    'sqft_above':    {'label': 'Luas Atas Tanah',       'min': 300,  'max': 9000,   'step': 50,   'default': 1800, 'unit': 'sqft'},
    'sqft_basement': {'label': 'Luas Basement',         'min': 0,    'max': 4000,   'step': 50,   'default': 0,    'unit': 'sqft'},
    'sqft_living15': {'label': 'Luas Bangunan Tetangga','min': 400,  'max': 6000,   'step': 50,   'default': 1800, 'unit': 'sqft'},
    'sqft_lot15':    {'label': 'Luas Lahan Tetangga',   'min': 600,  'max': 50000,  'step': 500,  'default': 7000, 'unit': 'sqft'},
    'lat':           {'label': 'Latitude',              'min': 47.15,'max': 47.78,  'step': 0.01, 'default': 47.5, 'unit': '°N'},
    'long':          {'label': 'Longitude',             'min': -122.52,'max':-121.31,'step':0.01, 'default':-122.2,'unit': '°W'},
    'yr_built':      {'label': 'Tahun Dibangun',        'min': 1900, 'max': 2015,   'step': 1,    'default': 1985, 'unit': ''},
    'yr_renovated':  {'label': 'Tahun Renovasi (0 = belum)', 'min': 0, 'max': 2015,'step': 1,    'default': 0,    'unit': ''},
}


@st.cache_resource
def load_pipeline():
    import joblib
    gb     = joblib.load(GB_PATH)
    scaler = joblib.load(SC_PATH)
    return gb, scaler


def build_features(inputs: dict) -> pd.DataFrame:
    """Terapkan feature engineering persis seperti pipeline training."""
    yr_built     = inputs['yr_built']
    yr_renovated = inputs['yr_renovated']

    engineered = {
        'house_age':       2015 - yr_built,
        'is_renovated':    int(yr_renovated > 0),
        'renovated_age':   (2015 - yr_renovated) if yr_renovated > 0 else 0,
        'sqft_ratio':      inputs['sqft_living'] / (inputs['sqft_lot'] + 1),
        'total_rooms':     inputs['bedrooms'] + inputs['bathrooms'],
        'basement_flag':   int(inputs['sqft_basement'] > 0),
        'sqft_living_log': np.log1p(inputs['sqft_living']),
    }

    row = {k: inputs[k] for k in [
        'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
        'waterfront', 'view', 'condition', 'grade', 'sqft_above',
        'sqft_basement', 'sqft_living15', 'sqft_lot15', 'lat', 'long',
    ]}
    row.update(engineered)

    return pd.DataFrame([row])[FEATURE_COLS]


def render():
    section_header("🏠 House Price Prediction — Model App",
                   "Masukkan spesifikasi rumah untuk mendapatkan estimasi harga "
                   "menggunakan pipeline Gradient Boosting King County.")

    # Cek apakah model sudah ada
    model_ready = os.path.exists(GB_PATH) and os.path.exists(SC_PATH)

    if not model_ready:
        st.warning("""
        ⚠️ **File model belum ditemukan.**

        Letakkan file berikut di folder `projects/_house_prediction/models/`:
        - `gb_model.pkl` — Gradient Boosting model
        - `scaler_house.pkl` — RobustScaler (untuk model linear; GB tidak wajib)

        Setelah diunggah, halaman ini akan aktif otomatis.
        """)

        # Tetap tampilkan form sebagai preview (tanpa prediksi)
        st.info("💡 Preview form input di bawah ini. Prediksi akan aktif setelah model diunggah.")
        st.markdown("---")

    # ── Input form ────────────────────────────────────────────────────────
    st.markdown("#### 🏡 Spesifikasi Rumah")

    col1, col2, col3 = st.columns(3)
    inputs = {}
    cfg_items = list(INPUT_CONFIG.items())

    for i, (feat, cfg) in enumerate(cfg_items):
        target_col = [col1, col2, col3][i % 3]
        with target_col:
            label = f"{cfg['label']}" + (f" ({cfg['unit']})" if cfg['unit'] else "")
            val = st.slider(
                label=label,
                min_value=float(cfg['min']),
                max_value=float(cfg['max']),
                value=float(cfg['default']),
                step=float(cfg['step']),
                key=f"house_{feat}"
            )
            inputs[feat] = val

    st.markdown("---")

    # ── Tombol prediksi ───────────────────────────────────────────────────
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        predict_btn = st.button("🔍 Estimasi Harga", use_container_width=True,
                                type="primary", disabled=not model_ready)

    if predict_btn and model_ready:
        gb, scaler = load_pipeline()

        # Build feature vector dengan engineering
        X_input = build_features(inputs)

        # Gradient Boosting tidak butuh scaling, tapi sediakan jika diperlukan
        pred_price = gb.predict(X_input)[0]

        # ── Hasil prediksi ────────────────────────────────────────────────
        st.markdown("---")
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e3a5f, #0f766e);
            border-radius: 14px;
            padding: 2rem;
            text-align: center;
            color: white;
            margin-bottom: 1.5rem;
        ">
            <div style="font-size: 1rem; opacity: 0.8;">Estimasi Harga Rumah</div>
            <div style="font-size: 3rem; font-weight: 800; margin: 0.5rem 0;">
                ${pred_price:,.0f}
            </div>
            <div style="font-size: 1.1rem; opacity: 0.85;">
                ≈ ${pred_price/1e3:.1f}K USD
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Konteks harga ─────────────────────────────────────────────────
        c1, c2, c3 = st.columns(3)
        c1.metric("Perbandingan Median KC", f"${450_000:,}",
                  delta=f"${pred_price - 450_000:+,.0f}")
        c2.metric("Perbandingan Mean KC",   f"${540_000:,}",
                  delta=f"${pred_price - 540_000:+,.0f}")
        c3.metric("Estimasi MAPE ±", "~12.9%",
                  help="Rata-rata error model di test set adalah 12.9% dari harga aktual")

        # ── Detail feature engineering ────────────────────────────────────
        with st.expander("📋 Detail input & feature engineering yang digunakan"):
            eng = build_features(inputs)
            eng_display = pd.DataFrame({
                'Fitur':  eng.columns.tolist(),
                'Nilai':  [f"{v:.4f}" if isinstance(v, float) else str(v)
                           for v in eng.iloc[0].tolist()],
                'Sumber': ['Input' if f in INPUT_CONFIG else 'Engineered'
                           for f in eng.columns]
            })
            st.dataframe(eng_display, use_container_width=True, hide_index=True)