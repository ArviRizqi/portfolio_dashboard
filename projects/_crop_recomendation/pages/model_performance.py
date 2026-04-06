# projects/_crop_recomendation/pages/model_performance.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header, metric_row


# ── Sample model results (replace with real model evaluation) ──────────────
MODEL_RESULTS = pd.DataFrame({
    "Model":     ["Random Forest", "XGBoost", "SVM", "KNN", "Decision Tree", "Naive Bayes"],
    "Accuracy":  [0.993, 0.987, 0.975, 0.962, 0.904, 0.881],
    "Precision": [0.991, 0.986, 0.974, 0.960, 0.901, 0.879],
    "Recall":    [0.993, 0.987, 0.975, 0.961, 0.904, 0.882],
    "F1 Score":  [0.992, 0.986, 0.974, 0.961, 0.902, 0.880],
})

CONFUSION = np.array([
    [98,  1,  0,  1],
    [ 0, 97,  2,  1],
    [ 1,  1, 96,  2],
    [ 0,  2,  1, 97],
])
CLASSES = ["rice", "maize", "chickpea", "kidney beans"]


def render():
    section_header("🌾 Crop Recommendation — Model Performance",
                   "Compare multiple classifiers on accuracy, precision, recall, and F1.")

    # ── Best model KPIs ────────────────────────────────────────────────
    best = MODEL_RESULTS.iloc[0]
    metric_row({
        "Best Model":  best["Model"],
        "Accuracy":    f"{best['Accuracy']*100:.1f}%",
        "F1 Score":    f"{best['F1 Score']*100:.1f}%",
        "Models Tested": len(MODEL_RESULTS),
    })

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏆 Leaderboard", "📊 Metric Chart", "🔲 Confusion Matrix"])

    # ── Tab 1 ────────────────────────────────────────────────────────
    with tab1:
        styled = MODEL_RESULTS.style \
            .highlight_max(subset=["Accuracy","Precision","Recall","F1 Score"],
                           color="#bbf7d0") \
            .format({"Accuracy":"{:.3f}","Precision":"{:.3f}",
                     "Recall":"{:.3f}","F1 Score":"{:.3f}"})
        st.dataframe(styled, use_container_width=True, hide_index=True)

    # ── Tab 2 ────────────────────────────────────────────────────────
    with tab2:
        metric = st.selectbox("Metric", ["Accuracy","Precision","Recall","F1 Score"])
        df_sorted = MODEL_RESULTS.sort_values(metric)
        fig = px.bar(df_sorted, x=metric, y="Model", orientation="h",
                     title=f"Model Comparison — {metric}",
                     template="plotly_white",
                     color=metric, color_continuous_scale="Teal",
                     text=metric)
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig.update_layout(coloraxis_showscale=False, xaxis_range=[0.85, 1.0])
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 3 ────────────────────────────────────────────────────────
    with tab3:
        st.caption("Confusion matrix for the best model (Random Forest) — top 4 classes shown.")
        fig = px.imshow(CONFUSION, x=CLASSES, y=CLASSES,
                        text_auto=True, aspect="auto",
                        color_continuous_scale="Blues",
                        title="Confusion Matrix — Random Forest",
                        labels={"x":"Predicted","y":"Actual"})
        st.plotly_chart(fig, use_container_width=True)