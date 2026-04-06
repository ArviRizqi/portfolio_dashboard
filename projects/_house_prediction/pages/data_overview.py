# projects/_house_prediction/pages/data_overview.py

import streamlit as st
import pandas as pd
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header, metric_row, show_dataframe

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/kc_house_data.csv")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    # Parse date
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%dT%H%M%S", errors="coerce")
    # Drop kolom tidak relevan untuk analisis
    df = df.drop(columns=["id"], errors="ignore")
    # Hapus baris dengan nilai null di price
    df = df.dropna(subset=["price"])
    return df


def render():
    section_header("🏠 House Price Prediction — Data Overview",
                   "Dataset King County, WA — transaksi rumah 2014–2015.")

    df = load_data()

    metric_row({
        "Total Transaksi": f"{df.shape[0]:,}",
        "Fitur":           df.shape[1] - 1,
        "Rata-rata Harga": f"${df['price'].mean():,.0f}",
        "Missing Values":  int(df.isnull().sum().sum()),
    })

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄 Sample Data", "📊 Statistik", "📋 Info Kolom"])

    with tab1:
        show_dataframe(df, "10 baris pertama", max_rows=10)
        st.caption(f"Dataset: `kc_house_data.csv` — {df.shape[0]:,} baris × {df.shape[1]} kolom")

    with tab2:
        num_df = df.select_dtypes(include="number")
        st.markdown("**Statistik Deskriptif (Numerik)**")
        st.dataframe(num_df.describe().round(2), use_container_width=True)

        # Harga statistik highlight
        c1, c2, c3 = st.columns(3)
        c1.metric("Harga Minimum",  f"${df['price'].min():,.0f}")
        c2.metric("Median Harga",   f"${df['price'].median():,.0f}")
        c3.metric("Harga Maksimum", f"${df['price'].max():,.0f}")

    with tab3:
        info_df = pd.DataFrame({
            "Kolom":      df.columns.tolist(),
            "Tipe Data":  [str(d) for d in df.dtypes],
            "Non-Null":   df.notnull().sum().tolist(),
            "Null":       df.isnull().sum().tolist(),
            "Unique":     [df[c].nunique() for c in df.columns],
        })
        st.dataframe(info_df, use_container_width=True, hide_index=True)

        nulls = df.isnull().sum()
        null_cols = nulls[nulls > 0]
        if len(null_cols) > 0:
            st.warning(f"⚠️ Kolom dengan missing values: {', '.join(null_cols.index.tolist())}")
        else:
            st.success("✅ Tidak ada missing values pada kolom utama.")