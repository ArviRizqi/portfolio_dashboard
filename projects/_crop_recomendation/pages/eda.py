# projects/_crop_recomendation/pages/eda.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Crop_Recommendation.csv")

NUMERIC_COLS = ["N", "P", "K", "Temperature", "Humidity", "ph", "Rainfall"]
COLORS = px.colors.qualitative.Set2


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def render():
    section_header("🌾 Crop Recommendation — EDA",
                   "Eksplorasi distribusi, korelasi, dan pola antar fitur.")

    df = load_data()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Distribusi Fitur",
        "🔗 Korelasi",
        "🌿 Rata-rata per Tanaman",
        "🔵 Scatter Plot",
    ])

    # ── Tab 1: Histogram ─────────────────────────────────────────────────
    with tab1:
        col = st.selectbox("Pilih fitur", NUMERIC_COLS, key="dist_col")
        show_by_crop = st.checkbox("Pisahkan per tanaman", value=False)

        if show_by_crop:
            fig = px.histogram(df, x=col, color="label", nbins=40,
                               template="plotly_white",
                               title=f"Distribusi {col} per Tanaman",
                               color_discrete_sequence=COLORS,
                               barmode="overlay", opacity=0.6)
            fig.update_layout(showlegend=True)
        else:
            fig = px.histogram(df, x=col, nbins=40,
                               template="plotly_white",
                               title=f"Distribusi {col}",
                               color_discrete_sequence=["#0ea5e9"])
        st.plotly_chart(fig, use_container_width=True)

        # Box plot ringkasan
        fig2 = px.box(df, x="label", y=col,
                      title=f"Boxplot {col} per Tanaman",
                      template="plotly_white",
                      color="label", color_discrete_sequence=COLORS)
        fig2.update_layout(showlegend=False, xaxis_tickangle=-40)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 2: Korelasi ──────────────────────────────────────────────────
    with tab2:
        corr = df[NUMERIC_COLS].corr().round(3)
        fig = px.imshow(corr, text_auto=True, aspect="auto",
                        color_continuous_scale="RdBu_r",
                        zmin=-1, zmax=1,
                        title="Heatmap Korelasi Antar Fitur",
                        template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        # Pair yang paling berkorelasi
        corr_pairs = (corr.where(
            ~(corr == 1.0))
            .stack()
            .reset_index()
        )
        corr_pairs.columns = ["Fitur A", "Fitur B", "Korelasi"]
        corr_pairs["abs"] = corr_pairs["Korelasi"].abs()
        corr_pairs = corr_pairs.sort_values("abs", ascending=False).drop_duplicates(subset=["abs"])
        top5 = corr_pairs.head(5).drop(columns="abs")
        top5["Korelasi"] = top5["Korelasi"].round(3)
        st.markdown("**Top 5 pasangan fitur berkorelasi:**")
        st.dataframe(top5, use_container_width=True, hide_index=True)

    # ── Tab 3: Rata-rata per tanaman ──────────────────────────────────────
    with tab3:
        feat = st.selectbox("Pilih fitur", NUMERIC_COLS, key="crop_feat")
        grouped = df.groupby("label")[feat].mean().sort_values(ascending=False).reset_index()
        grouped.columns = ["Tanaman", "Rata-rata"]

        fig = px.bar(grouped, x="Tanaman", y="Rata-rata",
                     title=f"Rata-rata {feat} per Tanaman",
                     template="plotly_white",
                     color="Rata-rata", color_continuous_scale="Teal",
                     text="Rata-rata")
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig.update_layout(xaxis_tickangle=-40, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 4: Scatter ──────────────────────────────────────────────────
    with tab4:
        c1, c2 = st.columns(2)
        x_col = c1.selectbox("Sumbu X", NUMERIC_COLS, index=0, key="sx")
        y_col = c2.selectbox("Sumbu Y", NUMERIC_COLS, index=1, key="sy")

        crops = ["Semua"] + sorted(df["label"].unique().tolist())
        selected = st.multiselect("Filter tanaman (opsional)", crops[1:],
                                  default=[], key="scatter_filter")

        plot_df = df[df["label"].isin(selected)] if selected else df

        fig = px.scatter(plot_df, x=x_col, y=y_col, color="label",
                         title=f"{x_col} vs {y_col}",
                         template="plotly_white", opacity=0.7,
                         color_discrete_sequence=COLORS,
                         hover_data=["label"])
        st.plotly_chart(fig, use_container_width=True)