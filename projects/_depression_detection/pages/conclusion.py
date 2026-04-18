import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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
BASE       = str(CURRENT_DIR)

def render():
    section_header("🧠 Depression Detection — Conclusion",
                   "Ringkasan profil SMMH, performa model XGBoost, "
                   "dan wawasan psikologis mengenai kecanduan sosial media.")

    # ── 1. Wawasan Psikologis Utama ───────────────────────────────────────────
    st.markdown("### 🔍 Wawasan Psikologis")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style="background:#fefce8;border-left:4px solid #ca8a04;
                    padding:1rem;border-radius:0 8px 8px 0; color:#000">
            <div style="font-size:1.5rem">📉</div>
            <strong>Kesulitan Konsentrasi & Validasi</strong><br>
            <small>Fitur `difficult_to_concentrate` dan kebiasaan `seek_validation` memiliki korelasi tertinggi dengan depresi.</small>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#eff6ff;border-left:4px solid #2563eb;
                    padding:1rem;border-radius:0 8px 8px 0; color:#000">
            <div style="font-size:1.5rem">📱</div>
            <strong>Screen Time & Depresi</strong><br>
            <small>Penggunaan > 5 jam sehari berbanding lurus dengan peningkatan level depresi akut.</small>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style="background:#f0fdf4;border-left:4px solid #16a34a;
                    padding:1rem;border-radius:0 8px 8px 0; color:#000">
            <div style="font-size:1.5rem">👥</div>
            <strong>Comparison Culture</strong><br>
            <small>Pengguna yang intens membandingkan dirinya dengan figur di sosial media menunjukkan kerentanan lebih tinggi (Comparison to others).</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 2. Implementasi Model Tensor-Flow ─────────────────────────────────
    st.markdown("### 🤖 Implementasi & Deployment")
    
    st.markdown("""
    Dalam pengaplikasian tingkat klasifikasi yang lebih sensitif seperti diagnosis, 
    model yang digunakan memanfaatkan kekuatan **XGBoost Classifier**.
    
    **Konfigurasi Model XGBoost (`.pkl`):**
    - Algoritma Gradient Boosting (XGBoost)
    - Input preprocessor menggunakan scikit-learn `ColumnTransformer` & Pipeline.
    - Support untuk klasifikasi multikelas (5 Levels) secara presisi dan efisien.
    """)

    st.markdown("---")

    # ── 3. Batasan dan Rekomendasi ──────────────────────────────────────────
    st.markdown("### 💡 Rekomendasi & Etika Penggunaan")

    st.warning("""
    **Catatan Skrining Klinis (Ethical Disclaimer):**
    Prediksi sistem yang dikeluarkan bersifat eksperimental (estimasi algoritma klasifikasi) dan hanya meninjau
    kebiasaan penggunaan media sosial berdasar Dataset *SMMH Augmented*.
    
    Prediksi komputer dari form tersebut **tidak dapat dan tidak boleh** digunakan untuk menggantikan diagnosis 
    psikologis profesional atau tenaga medis yang berizin.
    """)

    st.info("""
    **Saran Pengembangan ke Depan:**
    - Penambahan dimensi variabel seperti faktor ekternal lingkungan, latar belakang biologis keturunan.
    - Menurunkan model secara granular menjadi binary classification `[Depresi Klinis vs Ringan]` 
      dengan _threshold/confidence score_ yang bisa diatur untuk menekan angka *False Positives*.
    - Melakukan validasi eksternal terhadap responden non-berbahasa inggris untuk meminimalisasi cultural-bias 
      dalam kuesioner awal.
    """)

    st.markdown("---")
    st.caption("Deployment Artifacts: `depression_model.h5` | Pipeline: `preprocessor.pkl` | Dataset: SMMH")