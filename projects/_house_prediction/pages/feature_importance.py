# projects/_house_prediction/pages/feature_importance.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header


FEATURES    = ["OverallQual","GrLivArea","TotalBsmtSF","GarageCars",
               "YearBuilt","FullBath","BedroomAbvGr"]
IMPORTANCES = [0.371, 0.248, 0.142, 0.098, 0.075, 0.041, 0.025]


def render():
    section_header("🏠 House Price Prediction — Feature Importance",
                   "Which structural and quality factors drive house prices the most?")

    df = pd.DataFrame({"Feature": FEATURES, "Importance": IMPORTANCES}) \
           .sort_values("Importance", ascending=True)

    tab1, tab2 = st.tabs(["📊 Bar Chart", "🌡️ Table"])

    with tab1:
        fig = px.bar(df, x="Importance", y="Feature", orientation="h",
                     title="Feature Importance — XGBoost",
                     template="plotly_white",
                     color="Importance", color_continuous_scale="Blues",
                     text="Importance")
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig.update_layout(coloraxis_showscale=False,
                          xaxis_title="Importance Score",
                          yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        top = df.iloc[-1]
        st.info(f"💡 **{top['Feature']}** mendominasi prediksi harga rumah "
                f"dengan skor **{top['Importance']:.3f}**, menunjukkan bahwa "
                "kualitas keseluruhan rumah adalah faktor paling penentu harga.")

    with tab2:
        df_table = df.sort_values("Importance", ascending=False).copy()
        df_table["Importance"] = df_table["Importance"].apply(lambda x: f"{x:.3f}")
        df_table["Rank"] = range(1, len(df_table)+1)
        df_table = df_table[["Rank","Feature","Importance"]]
        st.dataframe(df_table, use_container_width=True, hide_index=True)