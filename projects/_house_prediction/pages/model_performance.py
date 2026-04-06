# projects/_house_prediction/pages/model_performance.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header, metric_row


MODEL_RESULTS = pd.DataFrame({
    "Model":    ["XGBoost","Random Forest","Gradient Boost","Ridge","Lasso","Linear Regression"],
    "RMSE":     [24500, 27800, 28100, 35200, 36100, 40500],
    "MAE":      [16800, 19200, 19700, 24600, 25100, 29800],
    "R² Score": [0.921, 0.898, 0.893, 0.841, 0.835, 0.790],
})


def render():
    section_header("🏠 House Price Prediction — Model Performance",
                   "Compare regression models by RMSE, MAE, and R² score.")

    best = MODEL_RESULTS.iloc[0]
    metric_row({
        "Best Model": best["Model"],
        "RMSE":       f"${best['RMSE']:,}",
        "MAE":        f"${best['MAE']:,}",
        "R² Score":   f"{best['R² Score']:.3f}",
    })

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🏆 Leaderboard", "📊 Metric Chart"])

    with tab1:
        styled = MODEL_RESULTS.style \
            .highlight_min(subset=["RMSE","MAE"], color="#bbf7d0") \
            .highlight_max(subset=["R² Score"], color="#bbf7d0") \
            .format({"RMSE":"${:,}","MAE":"${:,}","R² Score":"{:.3f}"})
        st.dataframe(styled, use_container_width=True, hide_index=True)

    with tab2:
        metric = st.selectbox("Metric", ["RMSE","MAE","R² Score"])
        ascending = metric != "R² Score"
        df_sorted = MODEL_RESULTS.sort_values(metric, ascending=ascending)
        fig = px.bar(df_sorted, x=metric, y="Model", orientation="h",
                     title=f"Model Comparison — {metric}",
                     template="plotly_white",
                     color=metric,
                     color_continuous_scale="Blues" if ascending else "Teal",
                     text=metric)
        fmt = "${:,.0f}" if metric != "R² Score" else "{:.3f}"
        fig.update_traces(texttemplate=fmt.replace("{", "%{text").replace("}", "}"),
                          textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)