import streamlit as st
import pandas as pd
import plotly.express as px
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header, metric_row

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/kc_house_data.csv")

NUMERIC_COLS = ["price", "sqft_living", "sqft_lot", "sqft_above",
                "sqft_basement", "sqft_living15", "sqft_lot15",
                "bedrooms", "bathrooms", "floors", "grade",
                "condition", "yr_built", "yr_renovated"]


# =========================
# RAW DATA (BEFORE CLEANING)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%dT%H%M%S", errors="coerce")
    return df


# =========================
# CLEANING PIPELINE
# =========================
@st.cache_data
def clean_data(df):
    df_clean = df.copy()

    # Drop missing penting
    df_clean = df_clean.dropna(subset=["price", "bedrooms", "bathrooms"])

    # Feature engineering
    df_clean["price_M"] = df_clean["price"] / 1_000_000
    df_clean["age"] = df_clean["date"].dt.year - df_clean["yr_built"]
    df_clean["renovated"] = df_clean["yr_renovated"].apply(lambda x: "Ya" if x > 0 else "Tidak")
    df_clean["waterfront_label"] = df_clean["waterfront"].apply(lambda x: "Waterfront" if x == 1 else "Non-Waterfront")

    # Outlier handling (IQR - price)
    Q1 = df_clean["price"].quantile(0.25)
    Q3 = df_clean["price"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df_clean = df_clean[(df_clean["price"] > lower) & (df_clean["price"] < upper)]

    return df_clean


def render():
    section_header("🏠 House Price Prediction — EDA",
                   "Eksplorasi distribusi harga, cleaning data, dan faktor penentu properti.")

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
            st.markdown("### 📉 Before Cleaning")
            metric_row({
                "Rows": f"{df_raw.shape[0]:,}",
                "Missing": int(df_raw.isnull().sum().sum()),
                "Duplicates": int(df_raw.duplicated().sum())
            })

        # AFTER
        with col2:
            st.markdown("### ✅ After Cleaning")
            metric_row({
                "Rows": f"{df.shape[0]:,}",
                "Missing": int(df.isnull().sum().sum()),
                "Duplicates": int(df.duplicated().sum())
            })

        st.markdown("---")

        # Cleaning log (ini bikin kamu terlihat expert)
        st.markdown("### 📘 Cleaning Summary")
        st.markdown(f"""
        - Missing values pada `price`, `bedrooms`, dan `bathrooms` dihapus  
        - Outlier pada `price` dihapus menggunakan metode IQR  
        - Feature engineering:
          - `age` (umur rumah)
          - `price_M` (harga dalam juta USD)
          - `renovated` (status renovasi)
        - Total data berkurang dari **{len(df_raw):,} → {len(df):,}**
        """)

        # Visual perbandingan
        compare_df = pd.DataFrame({
            "Stage": ["Before", "After"],
            "Rows": [len(df_raw), len(df)]
        })

        fig = px.bar(compare_df, x="Stage", y="Rows",
                     title="Perbandingan Jumlah Data",
                     template="plotly_white",
                     text="Rows")
        st.plotly_chart(fig, use_container_width=True)


    # =========================
    # TAB 2 — DISTRIBUSI
    # =========================
    with tab2:
        fig = px.histogram(df, x="price", nbins=80,
                           title="Distribusi Harga Rumah",
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
        corr_cols = ["price","sqft_living","grade","sqft_above",
                     "sqft_living15","bathrooms","bedrooms"]

        corr = df[corr_cols].corr()

        fig = px.imshow(corr, text_auto=True,
                        color_continuous_scale="RdBu_r",
                        title="Korelasi Fitur")
        st.plotly_chart(fig, use_container_width=True)