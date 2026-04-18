# projects/_crop_recomendation/pages/conclusion.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import os, sys, warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header

BASE      = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE, "../data/Crop_Recommendation.csv")
RF_PATH   = os.path.join(BASE, "../models/rf_model.pkl")
LE_PATH   = os.path.join(BASE, "../models/label_encoder.pkl")
SC_PATH   = os.path.join(BASE, "../models/scaler.pkl")

FEATURES  = ["N", "P", "K", "Temperature", "Humidity", "ph", "Rainfall"]


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_pipeline():
    return (
        joblib.load(RF_PATH),
        joblib.load(SC_PATH),
        joblib.load(LE_PATH),
    )


def render():
    section_header("🌾 Crop Recommendation — Conclusion",
                   "Ringkasan temuan EDA, performa pipeline, dan rekomendasi penggunaan.")

    df          = load_data()
    rf, sc, le  = load_pipeline()

    # ── 1. Ringkasan Dataset ──────────────────────────────────────────────
    st.markdown("### 📦 Ringkasan Dataset")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sampel",   f"{len(df):,}")
    c2.metric("Fitur Input",    "7")
    c3.metric("Jumlah Kelas",   df["label"].nunique())
    c4.metric("Distribusi",     "Seimbang (100/kelas)")

    st.markdown("""
    Dataset **Crop Recommendation** berisi 2.200 sampel dengan 7 fitur agrikultur
    (N, P, K, suhu, kelembapan, pH, curah hujan) dan 22 kelas tanaman.
    Setiap kelas memiliki tepat **100 sampel**, sehingga dataset ini **perfectly balanced**
    dan tidak memerlukan teknik oversampling/undersampling.
    """)

    st.markdown("---")

    # ── 2. Temuan EDA ─────────────────────────────────────────────────────
    st.markdown("### 🔍 Temuan Utama EDA")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**Korelasi terhadap Label**")
        df2 = df.copy()
        df2["label_enc"] = le.transform(df2["label"])
        corr_label = df2[FEATURES + ["label_enc"]].corr()["label_enc"].drop("label_enc").sort_values()
        fig = px.bar(x=corr_label.values, y=corr_label.index, orientation="h",
                     template="plotly_white",
                     color=corr_label.values,
                     color_continuous_scale="RdBu_r",
                     text=[f"{v:.3f}" for v in corr_label.values],
                     title="Korelasi Fitur → Label")
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, height=320,
                          margin=dict(t=40,b=10,l=10,r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("**Feature Importance (Pipeline RF)**")
        fi  = rf.feature_importances_
        fi_df = pd.DataFrame({"Fitur": FEATURES, "Importance": fi}) \
                  .sort_values("Importance", ascending=True)
        fig2 = px.bar(fi_df, x="Importance", y="Fitur", orientation="h",
                      template="plotly_white",
                      color="Importance", color_continuous_scale="Teal",
                      text=fi_df["Importance"].apply(lambda x: f"{x:.3f}"),
                      title="Feature Importance (rf_model.pkl)")
        fig2.update_traces(textposition="outside")
        fig2.update_layout(coloraxis_showscale=False, height=320,
                           margin=dict(t=40,b=10,l=10,r=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    | Temuan | Detail |
    |--------|--------|
    | 🌧️ **Rainfall** paling berpengaruh | Importance 22.7% — curah hujan sangat menentukan jenis tanaman |
    | 💧 **Humidity** posisi kedua | Importance 21.1% — kelembapan udara sangat krusial |
    | 🧪 **K (Kalium)** faktor mineral utama | Importance 18.1% — mengungguli N dan P |
    | ⚗️ **ph** terendah | Importance hanya 5.2% — keasaman tanah relatif tidak dominan |
    | 📉 **P berkorelasi negatif kuat** | Korelasi -0.491 terhadap label — P tinggi → tanaman tertentu |
    """)

    st.markdown("---")

    # ── 3. Performa Model ─────────────────────────────────────────────────
    st.markdown("### 🤖 Performa Pipeline")

    st.markdown("""
    Pipeline menggunakan **Random Forest Classifier** dengan konfigurasi:
    - `n_estimators = 100`, `random_state = 42`
    - Preprocessing: **StandardScaler** → **LabelEncoder**
    - Split data: **80% train / 20% test**

    Berdasarkan notebook pelatihan, performa model pada test set:
    """)

    perf_df = pd.DataFrame({
        "Model":     ["Random Forest", "XGBoost", "MLP (Deep Learning)"],
        "Accuracy":  ["~99%", "~98%", "~98%"],
        "Keterangan":["✅ Digunakan di pipeline", "Alternatif", "Alternatif (lebih berat)"],
    })
    st.dataframe(perf_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── 4. Rekomendasi Penggunaan ─────────────────────────────────────────
    st.markdown("### 💡 Rekomendasi Penggunaan")

    st.success("""
    **Random Forest dipilih sebagai model produksi** karena:
    - Akurasi tertinggi (~99%) dibanding XGBoost dan MLP
    - Tidak memerlukan tuning ekstensif
    - Interpretable melalui feature importance
    - Cepat saat inference (tidak perlu GPU)
    """)

    st.info("""
    **Saran pengembangan ke depan:**
    - Tambah fitur lokasi geografis (latitude/longitude) untuk konteks regional
    - Validasi model dengan data lapangan nyata dari petani
    - Pertimbangkan model ensemble (stacking RF + XGBoost) untuk edge case
    - Tambahkan rekomendasi pupuk berdasarkan nilai N, P, K yang diinput
    """)

    st.markdown("---")
    st.caption("Model: `rf_model.pkl` | Scaler: `scaler.pkl` | Encoder: `label_encoder.pkl`")