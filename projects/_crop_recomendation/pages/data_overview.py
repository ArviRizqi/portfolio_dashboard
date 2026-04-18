# projects/_crop_recomendation/pages/data_overview.py

import streamlit as st
import pandas as pd
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header, metric_row, show_dataframe

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Crop_Recommendation.csv")


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def render():
    section_header("🌾 Crop Recommendation — Data Overview",
                   "Menampilkan struktur data, tipe-tipe fitur, serta statistik dasar pada bagian berikutnya.")

    df = load_data()

    metric_row({
        "Total Records":  df.shape[0],
        "Fitur Input":    df.shape[1] - 1,
        "Jenis Tanaman":  df["label"].nunique(),
        "Missing Values": int(df.isnull().sum().sum()),
    })

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄 Sample Data", "📊 Statistik", "🌿 Distribusi Tanaman"])

    with tab1:
        show_dataframe(df, "10 baris pertama", max_rows=10)
        st.caption(f"Dataset: `Crop_Recommendation.csv` — {df.shape[0]:,} baris × {df.shape[1]} kolom")

    with tab2:
        st.markdown("**Statistik Deskriptif**")
        st.dataframe(df.describe().round(3), use_container_width=True)

        st.markdown("**Tipe Data per Kolom**")
        dtype_df = pd.DataFrame({
            "Kolom":       df.columns.tolist(),
            "Tipe Data":   [str(d) for d in df.dtypes],
            "Non-Null":    df.notnull().sum().tolist(),
            "Null":        df.isnull().sum().tolist(),
        })
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    with tab3:
        dist = df["label"].value_counts().reset_index()
        dist.columns = ["Tanaman", "Jumlah"]
        dist["Persentase (%)"] = (dist["Jumlah"] / len(df) * 100).round(1)
        st.dataframe(dist, use_container_width=True, hide_index=True)
        st.info(f"✅ Dataset **seimbang** — setiap kelas berisi tepat **{dist['Jumlah'].iloc[0]} sampel**.")