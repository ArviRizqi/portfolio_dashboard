# projects/_house_prediction/pages/eda.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/kc_house_data.csv")

NUMERIC_COLS = ["price", "sqft_living", "sqft_lot", "sqft_above",
                "sqft_basement", "sqft_living15", "sqft_lot15",
                "bedrooms", "bathrooms", "floors", "grade",
                "condition", "yr_built", "yr_renovated"]


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%dT%H%M%S", errors="coerce")
    df = df.dropna(subset=["price"])
    df["price_M"] = df["price"] / 1_000_000  # dalam juta USD
    df["age"] = df["date"].dt.year - df["yr_built"]
    df["renovated"] = df["yr_renovated"].apply(lambda x: "Ya" if x > 0 else "Tidak")
    df["waterfront_label"] = df["waterfront"].apply(lambda x: "Waterfront" if x == 1 else "Non-Waterfront")
    return df.dropna(subset=["bedrooms", "bathrooms"])


def render():
    section_header("🏠 House Price Prediction — EDA",
                   "Eksplorasi distribusi harga, korelasi, dan faktor penentu nilai properti.")

    df = load_data()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Distribusi Harga",
        "🔗 Korelasi",
        "📐 Luas vs Harga",
        "🏘️ Faktor Kategorikal",
        "🗓️ Tren Waktu",
    ])

    # ── Tab 1: Distribusi harga ──────────────────────────────────────────
    with tab1:
        fig = px.histogram(df, x="price", nbins=80,
                           title="Distribusi Harga Rumah (King County, WA)",
                           template="plotly_white",
                           color_discrete_sequence=["#0ea5e9"],
                           labels={"price": "Harga (USD)"})
        fig.update_layout(xaxis_tickformat="$,.0f",
                          xaxis_title="Harga (USD)", yaxis_title="Frekuensi")
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        # Log scale
        fig2 = px.histogram(df, x="price", nbins=80,
                            title="Distribusi Harga (Log Scale)",
                            template="plotly_white",
                            color_discrete_sequence=["#0f766e"],
                            log_y=True,
                            labels={"price": "Harga (USD)"})
        fig2.update_layout(xaxis_tickformat="$,.0f")
        c1.plotly_chart(fig2, use_container_width=True)

        fig3 = px.box(df, x="waterfront_label", y="price",
                      title="Harga: Waterfront vs Non-Waterfront",
                      template="plotly_white",
                      color="waterfront_label",
                      color_discrete_sequence=["#0ea5e9","#f59e0b"])
        fig3.update_layout(showlegend=False, yaxis_tickformat="$,.0f",
                           xaxis_title="", yaxis_title="Harga (USD)")
        c2.plotly_chart(fig3, use_container_width=True)

    # ── Tab 2: Korelasi ──────────────────────────────────────────────────
    with tab2:
        corr_cols = ["price","sqft_living","grade","sqft_above",
                     "sqft_living15","bathrooms","bedrooms","floors",
                     "condition","yr_built"]
        corr = df[corr_cols].corr().round(3)
        fig = px.imshow(corr, text_auto=True, aspect="auto",
                        color_continuous_scale="RdBu_r",
                        zmin=-1, zmax=1,
                        title="Korelasi Antar Fitur Utama",
                        template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        # Bar korelasi dengan price
        price_corr = corr["price"].drop("price").sort_values(ascending=False)
        fig2 = px.bar(x=price_corr.index, y=price_corr.values,
                      title="Korelasi Fitur terhadap Harga",
                      template="plotly_white",
                      labels={"x":"Fitur","y":"Korelasi"},
                      color=price_corr.values,
                      color_continuous_scale="RdBu_r")
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 3: Luas vs Harga ─────────────────────────────────────────────
    with tab3:
        feat = st.selectbox("Pilih fitur luas", 
                            ["sqft_living","sqft_lot","sqft_above","sqft_basement","sqft_living15"])
        sample = df.sample(min(3000, len(df)), random_state=42)
        fig = px.scatter(sample, x=feat, y="price",
                         color="grade",
                         trendline="ols",
                         title=f"{feat} vs Harga (sample 3,000 data, warna = grade)",
                         template="plotly_white",
                         opacity=0.6,
                         color_continuous_scale="Viridis",
                         labels={feat: f"{feat} (sqft)", "price":"Harga (USD)"})
        fig.update_layout(yaxis_tickformat="$,.0f")
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 4: Faktor Kategorikal ────────────────────────────────────────
    with tab4:
        cat = st.selectbox("Pilih faktor", ["grade","condition","bedrooms","floors"])
        grp = df.groupby(cat)["price"].median().reset_index()
        grp.columns = [cat, "Median Harga"]

        fig = px.bar(grp, x=cat, y="Median Harga",
                     title=f"Median Harga berdasarkan {cat}",
                     template="plotly_white",
                     color="Median Harga",
                     color_continuous_scale="Blues",
                     text=grp["Median Harga"].apply(lambda x: f"${x:,.0f}"))
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, yaxis_tickformat="$,.0f")
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 5: Tren Waktu ────────────────────────────────────────────────
    with tab5:
        df["year_month"] = df["date"].dt.to_period("M").astype(str)
        monthly = df.groupby("year_month").agg(
            median_price=("price", "median"),
            jumlah=("price", "count")
        ).reset_index()

        fig = px.line(monthly, x="year_month", y="median_price",
                      title="Tren Median Harga Rumah per Bulan",
                      template="plotly_white",
                      markers=True,
                      labels={"year_month":"Bulan","median_price":"Median Harga (USD)"})
        fig.update_layout(yaxis_tickformat="$,.0f")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(monthly, x="year_month", y="jumlah",
                      title="Jumlah Transaksi per Bulan",
                      template="plotly_white",
                      color="jumlah", color_continuous_scale="Blues")
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)