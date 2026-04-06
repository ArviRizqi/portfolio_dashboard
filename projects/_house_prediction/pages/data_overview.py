# projects/_house_prediction/pages/data_overview.py

import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header, metric_row, show_dataframe


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
    section_header("🏠 House Price Prediction — Data Overview",
                   "Explore the housing dataset structure and key statistics.")

    df = _make_sample_df()

    metric_row({
        "Total Records":  df.shape[0],
        "Features":       df.shape[1] - 1,
        "Avg Sale Price": f"${df['SalePrice'].mean():,.0f}",
        "Missing Values": int(df.isnull().sum().sum()),
    })

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄 Sample Data", "📊 Statistics", "🏘️ By Neighborhood"])

    with tab1:
        show_dataframe(df, "First 10 rows", max_rows=10)

    with tab2:
        st.dataframe(df.describe().round(2), use_container_width=True)

    with tab3:
        nb = df.groupby("Neighborhood")["SalePrice"].agg(["mean","count"]).reset_index()
        nb.columns = ["Neighborhood","Avg Price","Count"]
        nb["Avg Price"] = nb["Avg Price"].apply(lambda x: f"${x:,.0f}")
        st.dataframe(nb, use_container_width=True, hide_index=True)