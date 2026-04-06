# projects/_house_prediction/pages/model_performance.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header, metric_row

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/kc_house_data.csv")

FEATURES = ["sqft_living", "sqft_lot", "sqft_above", "sqft_basement",
            "bedrooms", "bathrooms", "floors", "waterfront", "view",
            "condition", "grade", "yr_built", "yr_renovated",
            "sqft_living15", "sqft_lot15"]


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["price"] + FEATURES)
    # Filter outlier ekstrem (bedrooms == 33)
    df = df[df["bedrooms"] < 20]
    return df


@st.cache_data(show_spinner="🤖 Melatih model regresi... harap tunggu")
def train_all_models():
    df = load_data()
    X = df[FEATURES]
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    models = {
        "Linear Regression":    (LinearRegression(),  True),
        "Ridge":                (Ridge(alpha=1.0),     True),
        "Lasso":                (Lasso(alpha=100),     True),
        "Decision Tree":        (DecisionTreeRegressor(max_depth=10, random_state=42), False),
        "Random Forest":        (RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1), False),
        "Gradient Boosting":    (GradientBoostingRegressor(n_estimators=100, random_state=42), False),
    }

    results = []
    predictions = {}

    for name, (model, use_scaled) in models.items():
        Xtr = X_train_sc if use_scaled else X_train
        Xte = X_test_sc  if use_scaled else X_test
        model.fit(Xtr, y_train)
        y_pred = model.predict(Xte)

        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae  = mean_absolute_error(y_test, y_pred)
        r2   = r2_score(y_test, y_pred)

        results.append({
            "Model":    name,
            "RMSE":     rmse,
            "MAE":      mae,
            "R² Score": r2,
        })
        predictions[name] = (y_test.values, y_pred)

    df_results = pd.DataFrame(results).sort_values("R² Score", ascending=False).reset_index(drop=True)
    return df_results, predictions, y_test


def render():
    section_header("🏠 House Price Prediction — Model Performance",
                   "Perbandingan 6 model regresi pada data King County (80/20 split).")

    df_results, predictions, y_test = train_all_models()

    best = df_results.iloc[0]
    metric_row({
        "Best Model": best["Model"],
        "RMSE":       f"${best['RMSE']:,.0f}",
        "MAE":        f"${best['MAE']:,.0f}",
        "R² Score":   f"{best['R² Score']:.4f}",
    })

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏆 Leaderboard", "📊 Perbandingan Metrik", "🔍 Actual vs Predicted"])

    # ── Tab 1 ────────────────────────────────────────────────────────────
    with tab1:
        display = df_results.copy()
        display["RMSE"] = display["RMSE"].apply(lambda x: f"${x:,.0f}")
        display["MAE"]  = display["MAE"].apply(lambda x: f"${x:,.0f}")
        display["R² Score"] = display["R² Score"].apply(lambda x: f"{x:.4f}")
        st.dataframe(display, use_container_width=True, hide_index=True)
        st.caption("✅ Hijau = nilai terbaik per metrik. RMSE & MAE lebih kecil = lebih baik. R² lebih besar = lebih baik.")

    # ── Tab 2 ────────────────────────────────────────────────────────────
    with tab2:
        metric = st.selectbox("Pilih metrik", ["R² Score", "RMSE", "MAE"])
        ascending = metric in ["RMSE", "MAE"]
        df_sorted = df_results.sort_values(metric, ascending=ascending)

        fig = px.bar(df_sorted, x=metric, y="Model", orientation="h",
                     title=f"Perbandingan Model — {metric}",
                     template="plotly_white",
                     color=metric,
                     color_continuous_scale="Teal" if not ascending else "Blues_r",
                     text=df_sorted[metric].apply(
                         lambda x: f"${x:,.0f}" if metric != "R² Score" else f"{x:.4f}"
                     ))
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 3 ────────────────────────────────────────────────────────────
    with tab3:
        model_name = st.selectbox("Pilih model", df_results["Model"].tolist())
        y_actual, y_pred = predictions[model_name]

        # Sample 1000 agar tidak berat
        idx = np.random.choice(len(y_actual), size=min(1000, len(y_actual)), replace=False)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=y_actual[idx], y=y_pred[idx],
            mode="markers",
            marker=dict(color="#0ea5e9", opacity=0.5, size=5),
            name="Prediksi"
        ))
        # Garis ideal
        mn, mx = y_actual.min(), y_actual.max()
        fig.add_trace(go.Scatter(
            x=[mn, mx], y=[mn, mx],
            mode="lines",
            line=dict(color="red", dash="dash", width=2),
            name="Prediksi Sempurna"
        ))
        fig.update_layout(
            title=f"Actual vs Predicted — {model_name}",
            xaxis_title="Harga Aktual (USD)",
            yaxis_title="Harga Prediksi (USD)",
            xaxis_tickformat="$,.0f",
            yaxis_tickformat="$,.0f",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Titik yang mendekati garis merah putus-putus = prediksi mendekati nilai aktual.")