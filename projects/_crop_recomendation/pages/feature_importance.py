# projects/_crop_recomendation/pages/feature_importance.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header


FEATURES = ["rainfall","humidity","K","temperature","N","P","ph"]
IMPORTANCES = [0.312, 0.241, 0.148, 0.112, 0.087, 0.063, 0.037]


def render():
    section_header("🌾 Crop Recommendation — Feature Importance",
                   "Which soil & climate features matter most for crop prediction?")

    df = pd.DataFrame({"Feature": FEATURES, "Importance": IMPORTANCES}) \
           .sort_values("Importance", ascending=True)

    tab1, tab2 = st.tabs(["📊 Bar Chart", "🌡️ Table"])

    with tab1:
        fig = px.bar(df, x="Importance", y="Feature", orientation="h",
                     title="Feature Importance — Random Forest",
                     template="plotly_white",
                     color="Importance", color_continuous_scale="Teal",
                     text="Importance")
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig.update_layout(coloraxis_showscale=False,
                          xaxis_title="Importance Score",
                          yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        # Summary interpretation
        top = df.iloc[-1]
        st.info(f"💡 **{top['Feature']}** is the most important feature "
                f"with a score of **{top['Importance']:.3f}**, suggesting "
                "it has the strongest influence on crop type selection.")

    with tab2:
        df_table = df.sort_values("Importance", ascending=False).copy()
        df_table["Importance"] = df_table["Importance"].apply(lambda x: f"{x:.3f}")
        df_table["Rank"] = range(1, len(df_table)+1)
        df_table = df_table[["Rank","Feature","Importance"]]
        st.dataframe(df_table, use_container_width=True, hide_index=True)