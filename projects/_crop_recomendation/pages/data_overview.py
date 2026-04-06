# projects/_crop_recomendation/pages/data_overview.py

import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header, metric_row, show_dataframe


def render():
    section_header("🌾 Crop Recommendation — Data Overview",
                   "Dataset structure, feature types, and basic statistics.")

    # ── Load data ──────────────────────────────────────────────────────────
    # Replace with: df = pd.read_csv("projects/_crop_recomendation/data/crop_data.csv")
    np.random.seed(42)
    n = 2200
    crops = ["rice","maize","chickpea","kidney beans","pigeonpeas",
             "mothbeans","mungbean","blackgram","lentil","pomegranate",
             "banana","mango","grapes","watermelon","muskmelon","apple",
             "orange","papaya","coconut","cotton","jute","coffee"]
    df = pd.DataFrame({
        "N":         np.random.randint(0, 140, n),
        "P":         np.random.randint(5, 145, n),
        "K":         np.random.randint(5, 205, n),
        "temperature": np.random.uniform(8.0, 43.0, n).round(2),
        "humidity":  np.random.uniform(14.0, 99.0, n).round(2),
        "ph":        np.random.uniform(3.5, 9.9, n).round(2),
        "rainfall":  np.random.uniform(20.0, 298.0, n).round(2),
        "label":     np.random.choice(crops, n)
    })

    # ── KPIs ───────────────────────────────────────────────────────────────
    metric_row({
        "Total Records":   df.shape[0],
        "Features":        df.shape[1] - 1,
        "Target Classes":  df["label"].nunique(),
        "Missing Values":  int(df.isnull().sum().sum()),
    })

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📄 Sample Data", "📊 Statistics", "🏷️ Class Distribution"])

    with tab1:
        show_dataframe(df, "First 10 rows", max_rows=10)

    with tab2:
        st.markdown("**Descriptive Statistics**")
        st.dataframe(df.describe().round(2), use_container_width=True)

    with tab3:
        dist = df["label"].value_counts().reset_index()
        dist.columns = ["Crop", "Count"]
        dist["Percentage"] = (dist["Count"] / len(df) * 100).round(1)
        st.dataframe(dist, use_container_width=True, hide_index=True)