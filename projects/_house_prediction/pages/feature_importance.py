# projects/_house_prediction/pages/feature_importance.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header

from sklearn.ensemble import RandomForestRegressor

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/kc_house_data.csv")

FEATURES = ["sqft_living", "sqft_lot", "sqft_above", "sqft_basement",
            "bedrooms", "bathrooms", "floors", "waterfront", "view",
            "condition", "grade", "yr_built", "yr_renovated",
            "sqft_living15", "sqft_lot15"]

FEATURE_LABELS = {
    "sqft_living":   "Luas Dalam (sqft)",
    "sqft_lot":      "Luas Tanah (sqft)",
    "sqft_above":    "Luas Atas (sqft)",
    "sqft_basement": "Luas Basement (sqft)",
    "bedrooms":      "Kamar Tidur",
    "bathrooms":     "Kamar Mandi",
    "floors":        "Jumlah Lantai",
    "waterfront":    "Tepi Air",
    "view":          "View Score",
    "condition":     "Kondisi",
    "grade":         "Grade",
    "yr_built":      "Tahun Dibangun",
    "yr_renovated":  "Tahun Renovasi",
    "sqft_living15": "Luas Dalam Tetangga (sqft)",
    "sqft_lot15":    "Luas Tanah Tetangga (sqft)",
}


@st.cache_data(show_spinner="⭐ Menghitung feature importance...")
def get_feature_importance():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["price"] + FEATURES)
    df = df[df["bedrooms"] < 20]

    X = df[FEATURES]
    y = df["price"]

    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y)

    std = np.std([tree.feature_importances_ for tree in rf.estimators_], axis=0)

    importance_df = pd.DataFrame({
        "Fitur":        FEATURES,
        "Label":        [FEATURE_LABELS[f] for f in FEATURES],
        "Importance":   rf.feature_importances_,
        "Std":          std,
    }).sort_values("Importance", ascending=False).reset_index(drop=True)
    importance_df["Rank"] = range(1, len(importance_df) + 1)
    importance_df["Persen (%)"] = (importance_df["Importance"] * 100).round(2)

    return importance_df


def render():
    section_header("🏠 House Price Prediction — Feature Importance",
                   "Faktor struktural dan lokasi mana yang paling menentukan harga rumah?")

    df = get_feature_importance()

    tab1, tab2 = st.tabs(["📊 Bar Chart", "📋 Tabel"])

    with tab1:
        df_plot = df.sort_values("Importance", ascending=True)

        fig = px.bar(df_plot, x="Importance", y="Label", orientation="h",
                     error_x="Std",
                     title="Feature Importance — Random Forest Regressor (100 Trees)",
                     template="plotly_white",
                     color="Importance", color_continuous_scale="Blues",
                     text=df_plot["Persen (%)"].apply(lambda x: f"{x:.1f}%"))
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False,
                          xaxis_title="Importance Score",
                          yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        top = df.iloc[0]
        bottom = df.iloc[-1]
        st.info(
            f"💡 **{top['Label']}** adalah faktor paling dominan "
            f"({top['Persen (%)']:.1f}% kontribusi), diikuti oleh "
            f"**{df.iloc[1]['Label']}** ({df.iloc[1]['Persen (%)']:.1f}%). "
            f"**{bottom['Label']}** memiliki pengaruh paling kecil "
            f"({bottom['Persen (%)']:.1f}%)."
        )

    with tab2:
        display = df[["Rank", "Label", "Persen (%)", "Importance", "Std"]].copy()
        display["Importance"] = display["Importance"].apply(lambda x: f"{x:.5f}")
        display["Std"] = display["Std"].apply(lambda x: f"±{x:.5f}")
        st.dataframe(display, use_container_width=True, hide_index=True)