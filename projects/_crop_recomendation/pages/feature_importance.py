# projects/_crop_recomendation/pages/feature_importance.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Crop_Recommendation.csv")
NUMERIC_COLS = ["N", "P", "K", "Temperature", "Humidity", "ph", "Rainfall"]


@st.cache_data(show_spinner="⭐ Menghitung feature importance...")
def get_feature_importance():
    df = pd.read_csv(DATA_PATH)
    X = df[NUMERIC_COLS]
    le = LabelEncoder()
    y = le.fit_transform(df["label"])

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)

    importance_df = pd.DataFrame({
        "Fitur":       NUMERIC_COLS,
        "Importance":  rf.feature_importances_,
    }).sort_values("Importance", ascending=False).reset_index(drop=True)
    importance_df["Rank"] = range(1, len(importance_df) + 1)

    # Per-class importance (mean decrease impurity per class tidak tersedia langsung,
    # gunakan permutation importance proxy dengan std)
    std = np.std([tree.feature_importances_ for tree in rf.estimators_], axis=0)
    importance_df["Std"] = std

    return importance_df


def render():
    section_header("🌾 Crop Recommendation — Feature Importance",
                   "Fitur tanah & iklim mana yang paling berpengaruh terhadap prediksi tanaman?")

    df = get_feature_importance()

    tab1, tab2 = st.tabs(["📊 Bar Chart", "📋 Tabel"])

    with tab1:
        # Horizontal bar dengan error bar
        df_plot = df.sort_values("Importance", ascending=True)

        fig = px.bar(df_plot, x="Importance", y="Fitur", orientation="h",
                     error_x="Std",
                     title="Feature Importance — Random Forest (100 Trees)",
                     template="plotly_white",
                     color="Importance", color_continuous_scale="Teal",
                     text=df_plot["Importance"].apply(lambda x: f"{x:.4f}"))
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False,
                          xaxis_title="Importance Score (Mean Decrease Impurity)",
                          yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        # Insight otomatis
        top = df.iloc[0]
        bottom = df.iloc[-1]
        st.info(
            f"💡 **{top['Fitur']}** adalah fitur paling penting "
            f"(score: **{top['Importance']:.4f}**), sedangkan "
            f"**{bottom['Fitur']}** memberikan kontribusi paling kecil "
            f"(score: **{bottom['Importance']:.4f}**)."
        )

    with tab2:
        display_df = df[["Rank", "Fitur", "Importance", "Std"]].copy()
        display_df["Importance"] = display_df["Importance"].apply(lambda x: f"{x:.4f}")
        display_df["Std"] = display_df["Std"].apply(lambda x: f"±{x:.4f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)