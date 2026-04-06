# projects/_house_prediction/pages/eda.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header


def _make_sample_df():
    np.random.seed(7)
    n = 1000
    return pd.DataFrame({
        "GrLivArea":    np.random.randint(500, 4000, n),
        "BedroomAbvGr": np.random.randint(1, 6, n),
        "FullBath":     np.random.randint(1, 4, n),
        "YearBuilt":    np.random.randint(1880, 2022, n),
        "OverallQual":  np.random.randint(1, 11, n),
        "GarageCars":   np.random.randint(0, 4, n),
        "TotalBsmtSF":  np.random.randint(0, 2500, n),
        "Neighborhood": np.random.choice(
            ["NAmes","CollgCr","OldTown","Edwards","Somerst","Gilbert"], n),
        "SalePrice":    np.random.randint(80000, 750000, n),
    })


def render():
    section_header("🏠 House Price Prediction — EDA",
                   "Distribution, correlation, and price pattern analysis.")

    df = _make_sample_df()
    numeric_cols = [c for c in df.columns if c not in ["Neighborhood","SalePrice"]]

    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Price Distribution", "🔗 Correlation",
        "📊 Feature vs Price", "🏘️ By Neighborhood"
    ])

    with tab1:
        fig = px.histogram(df, x="SalePrice", nbins=50,
                           title="Sale Price Distribution",
                           template="plotly_white",
                           color_discrete_sequence=["#0ea5e9"])
        fig.update_layout(xaxis_tickformat="$,.0f")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        corr = df[numeric_cols + ["SalePrice"]].corr().round(2)
        fig = px.imshow(corr, text_auto=True, aspect="auto",
                        color_continuous_scale="RdBu_r",
                        title="Correlation Heatmap",
                        template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        feat = st.selectbox("Select feature", numeric_cols)
        fig = px.scatter(df, x=feat, y="SalePrice",
                         trendline="ols", template="plotly_white",
                         title=f"{feat} vs Sale Price",
                         color_discrete_sequence=["#0ea5e9"])
        fig.update_layout(yaxis_tickformat="$,.0f")
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        fig = px.box(df, x="Neighborhood", y="SalePrice",
                     title="Sale Price by Neighborhood",
                     template="plotly_white",
                     color="Neighborhood",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(showlegend=False, yaxis_tickformat="$,.0f")
        st.plotly_chart(fig, use_container_width=True)