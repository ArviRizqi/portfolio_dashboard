# projects/_crop_recomendation/pages/model_performance.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header, metric_row

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, confusion_matrix)

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/Crop_Recommendation.csv")
NUMERIC_COLS = ["N", "P", "K", "Temperature", "Humidity", "ph", "Rainfall"]


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


@st.cache_data(show_spinner="🤖 Melatih model... harap tunggu")
def train_all_models():
    df = load_data()
    X = df[NUMERIC_COLS]
    le = LabelEncoder()
    y = le.fit_transform(df["label"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "Random Forest":      RandomForestClassifier(n_estimators=100, random_state=42),
        "Decision Tree":      DecisionTreeClassifier(random_state=42),
        "KNN":                KNeighborsClassifier(n_neighbors=5),
        "Naive Bayes":        GaussianNB(),
        "SVM":                SVC(kernel="rbf", random_state=42),
        "Gradient Boosting":  GradientBoostingClassifier(n_estimators=100, random_state=42),
    }

    results = []
    confusion_matrices = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results.append({
            "Model":     name,
            "Accuracy":  accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
            "Recall":    recall_score(y_test, y_pred, average="weighted", zero_division=0),
            "F1 Score":  f1_score(y_test, y_pred, average="weighted", zero_division=0),
        })
        confusion_matrices[name] = (confusion_matrix(y_test, y_pred), le.classes_)

    df_results = pd.DataFrame(results).sort_values("Accuracy", ascending=False).reset_index(drop=True)
    return df_results, confusion_matrices


def render():
    section_header("🌾 Crop Recommendation — Model Performance",
                   "Perbandingan 6 model klasifikasi pada data asli (80/20 split).")

    df_results, confusion_matrices = train_all_models()

    best = df_results.iloc[0]
    metric_row({
        "Best Model":    best["Model"],
        "Accuracy":      f"{best['Accuracy']*100:.2f}%",
        "F1 Score":      f"{best['F1 Score']*100:.2f}%",
        "Models Tested": len(df_results),
    })

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏆 Leaderboard", "📊 Perbandingan Metrik", "🔲 Confusion Matrix"])

    # ── Tab 1 ────────────────────────────────────────────────────────────
    with tab1:
        styled = df_results.style \
            .highlight_max(subset=["Accuracy","Precision","Recall","F1 Score"],
                           color="#bbf7d0") \
            .format({"Accuracy":"{:.4f}","Precision":"{:.4f}",
                     "Recall":"{:.4f}","F1 Score":"{:.4f}"})
        st.dataframe(styled, use_container_width=True, hide_index=True)

    # ── Tab 2 ────────────────────────────────────────────────────────────
    with tab2:
        metric = st.selectbox("Pilih metrik", ["Accuracy","Precision","Recall","F1 Score"])
        df_sorted = df_results.sort_values(metric)
        fig = px.bar(df_sorted, x=metric, y="Model", orientation="h",
                     title=f"Perbandingan Model — {metric}",
                     template="plotly_white",
                     color=metric, color_continuous_scale="Teal",
                     text=df_sorted[metric].apply(lambda x: f"{x:.4f}"))
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False,
                          xaxis_range=[df_results[metric].min() - 0.05, 1.01])
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 3 ────────────────────────────────────────────────────────────
    with tab3:
        model_name = st.selectbox("Pilih model", df_results["Model"].tolist())
        cm, classes = confusion_matrices[model_name]

        # Tampilkan hanya 10 kelas pertama agar tidak terlalu padat
        n = min(10, len(classes))
        cm_sub = cm[:n, :n]
        classes_sub = classes[:n]

        fig = px.imshow(cm_sub,
                        x=classes_sub, y=classes_sub,
                        text_auto=True, aspect="auto",
                        color_continuous_scale="Blues",
                        title=f"Confusion Matrix — {model_name} (10 kelas pertama)",
                        labels={"x": "Prediksi", "y": "Aktual"})
        fig.update_layout(xaxis_tickangle=-40)
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Menampilkan {n} dari {len(classes)} kelas. "
                   "Diagonal = prediksi benar.")