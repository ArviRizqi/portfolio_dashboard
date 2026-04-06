# projects/_crop_recomendation/pages/eda.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header


def _make_sample_df():
    np.random.seed(42)
    n = 2200
    crops = ["rice","maize","chickpea","kidney beans","pigeonpeas",
             "mothbeans","mungbean","blackgram","lentil","pomegranate",
             "banana","mango","grapes","watermelon","muskmelon","apple",
             "orange","papaya","coconut","cotton","jute","coffee"]
    return pd.DataFrame({
        "N":           np.random.randint(0, 140, n),
        "P":           np.random.randint(5, 145, n),
        "K":           np.random.randint(5, 205, n),
        "temperature": np.random.uniform(8.0, 43.0, n).round(2),
        "humidity":    np.random.uniform(14.0, 99.0, n).round(2),
        "ph":          np.random.uniform(3.5, 9.9, n).round(2),
        "rainfall":    np.random.uniform(20.0, 298.0, n).round(2),
        "label":       np.random.choice(crops, n)
    })


def render():
    section_header("🌾 Crop Recommendation — EDA",
                   "Explore distributions, correlations, and patterns in the dataset.")

    # Replace with actual data load
    df = _make_sample_df()
    numeric_cols = [c for c in df.columns if c != "label"]

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribution", "🔗 Correlation", "🌿 By Crop", "🌧️ Scatter"])

    # ── Tab 1: Distribution ─────────────────────────────────────────────
    with tab1:
        col = st.selectbox("Select feature", numeric_cols, key="dist_col")
        fig = px.histogram(df, x=col, color="label", nbins=40,
                           title=f"Distribution of {col}",
                           template="plotly_white",
                           color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 2: Correlation heatmap ──────────────────────────────────────
    with tab2:
        corr = df[numeric_cols].corr().round(2)
        fig = px.imshow(corr, text_auto=True, aspect="auto",
                        color_continuous_scale="RdBu_r",
                        title="Feature Correlation Matrix",
                        template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 3: Mean values by crop ──────────────────────────────────────
    with tab3:
        feat = st.selectbox("Select feature", numeric_cols, key="crop_feat")
        grouped = df.groupby("label")[feat].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(grouped, x="label", y=feat,
                     title=f"Average {feat} by Crop",
                     template="plotly_white",
                     color=feat, color_continuous_scale="Teal")
        fig.update_layout(xaxis_tickangle=-40)
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 4: Scatter ──────────────────────────────────────────────────
    with tab4:
        c1, c2 = st.columns(2)
        x_col = c1.selectbox("X axis", numeric_cols, index=0, key="sx")
        y_col = c2.selectbox("Y axis", numeric_cols, index=1, key="sy")
        fig = px.scatter(df, x=x_col, y=y_col, color="label",
                         title=f"{x_col} vs {y_col}",
                         template="plotly_white", opacity=0.6,
                         color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)