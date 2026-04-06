import streamlit as st
import pandas as pd
import plotly.express as px
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header, metric_row

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/kc_house_data.csv")


# =========================
# RAW DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%dT%H%M%S", errors="coerce")
    return df


# =========================
# CLEANING PIPELINE (SESUAI NOTEBOOK KAMU)
# =========================
@st.cache_data
def clean_data(df):
    df_clean = df.copy()

    # --- 1. Drop kolom (sesuai pipeline kamu)
    df_clean = df_clean.drop([
        "id", "date", "waterfront", "view", "sqft_above",
        "sqft_basement", "zipcode", "lat", "long",
        "sqft_living15", "sqft_lot15"
    ], axis=1)

    # --- 2. Handling Missing
    df_clean.dropna(how="any", inplace=True)

    # --- 3. Handling Duplicate
    df_clean.drop_duplicates(inplace=True)

    # --- 4. Fix anomali bedrooms
    df_clean["bedrooms"] = df_clean["bedrooms"].replace(11, 1)
    df_clean["bedrooms"] = df_clean["bedrooms"].replace(33, 3)

    # --- 5. Handling Outlier (IQR - price)
    Q1 = df_clean["price"].quantile(0.25)
    Q3 = df_clean["price"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df_clean = df_clean[(df_clean["price"] > lower) & (df_clean["price"] < upper)]

    return df_clean


def render():
    section_header("🏠 House Price Prediction — EDA",
                   "Eksplorasi data, cleaning, dan faktor penentu harga rumah.")

    df_raw = load_data()
    df = clean_data(df_raw)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🧹 Cleaning Data",
        "📊 Distribusi Harga",
        "🏷️ Faktor Kategorikal",
        "🔗 Korelasi"
    ])

    # =========================
    # TAB 1 — CLEANING STORY
    # =========================
    with tab1:
        st.subheader("Before vs After Cleaning")

        col1, col2 = st.columns(2)

        # BEFORE
        with col1:
            st.markdown("### 📉 Before")
            metric_row({
                "Rows": f"{df_raw.shape[0]:,}",
                "Missing": int(df_raw.isnull().sum().sum()),
                "Duplicates": int(df_raw.duplicated().sum())
            })

        # AFTER
        with col2:
            st.markdown("### ✅ After")
            metric_row({
                "Rows": f"{df.shape[0]:,}",
                "Missing": int(df.isnull().sum().sum()),
                "Duplicates": int(df.duplicated().sum())
            })

        st.markdown("---")

        # =========================
        # DETAIL CLEANING
        # =========================
        st.markdown("### 📘 Cleaning Process")

        missing_before = int(df_raw.isnull().sum().sum())
        duplicate_before = int(df_raw.duplicated().sum())

        # estimasi setelah cleaning step by step (untuk storytelling)
        df_tmp = df_raw.copy()
        df_tmp = df_tmp.drop([
            "id", "date", "waterfront", "view", "sqft_above",
            "sqft_basement", "zipcode", "lat", "long",
            "sqft_living15", "sqft_lot15"
        ], axis=1)

        df_tmp2 = df_tmp.dropna(how="any")
        missing_removed = len(df_tmp) - len(df_tmp2)

        df_tmp3 = df_tmp2.drop_duplicates()
        duplicate_removed = len(df_tmp2) - len(df_tmp3)

        # Outlier
        Q1 = df_tmp3["price"].quantile(0.25)
        Q3 = df_tmp3["price"].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df_tmp4 = df_tmp3[(df_tmp3["price"] > lower) & (df_tmp3["price"] < upper)]
        outlier_removed = len(df_tmp3) - len(df_tmp4)

        st.markdown(f"""
        **Langkah Cleaning:**
        - Missing values dihapus → **{missing_removed:,} baris terdampak**
        - Duplicate dihapus → **{duplicate_removed:,} baris**
        - Anomali `bedrooms` (11 & 33) diperbaiki
        - Outlier `price` (IQR) dihapus → **{outlier_removed:,} baris**

        **Total Data:**
        - Sebelum: **{len(df_raw):,}**
        - Setelah: **{len(df):,}**
        """)

        # =========================
        # VISUAL REDUCTION
        # =========================
        compare_df = pd.DataFrame({
            "Stage": ["Raw", "After Missing", "After Duplicate", "After Outlier"],
            "Rows": [
                len(df_raw),
                len(df_tmp2),
                len(df_tmp3),
                len(df_tmp4)
            ]
        })

        fig = px.line(compare_df, x="Stage", y="Rows", markers=True,
                      title="Penurunan Jumlah Data Selama Cleaning",
                      template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # TAB 2 — DISTRIBUSI
    # =========================
    with tab2:
        fig = px.histogram(df, x="price", nbins=80,
                           title="Distribusi Harga Setelah Cleaning",
                           template="plotly_white")
        fig.update_layout(xaxis_tickformat="$,.0f")
        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # TAB 3 — KATEGORIKAL
    # =========================
    with tab3:
        cat = st.selectbox("Pilih faktor", ["grade","condition","bedrooms","floors"])
        grp = df.groupby(cat)["price"].median().reset_index()

        fig = px.bar(grp, x=cat, y="price",
                     title=f"Median Harga berdasarkan {cat}",
                     template="plotly_white",
                     text=grp["price"].apply(lambda x: f"${x:,.0f}"))
        fig.update_layout(yaxis_tickformat="$,.0f")
        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # TAB 4 — KORELASI
    # =========================
    with tab4:
        corr = df.corr(numeric_only=True)

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu_r",
            aspect="auto",  # 🔥 ini kunci utama
            title="Korelasi Antar Fitur",
            template="plotly_white"
        )

        fig.update_layout(
            height=500,   # lebih pendek
            width=1000,   # lebih lebar (horizontal)
        )

        fig.update_xaxes(tickangle=45)  # biar label tidak numpuk

        st.plotly_chart(fig, use_container_width=True)