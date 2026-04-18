# projects/_crop_recomendation/pages/eda.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import sys, os, warnings
warnings.filterwarnings("ignore")
from pathlib import Path

# Resolve path
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from shared.utils import section_header

# ── Paths ────────────────────────────────────────────────────────────────────
DATA_PATH  = str(CURRENT_DIR.parent / "data" / "Crop_Recommendation.csv")
MODEL_DIR  = CURRENT_DIR.parent / "models"
RF_PATH    = str(MODEL_DIR / "rf_model.pkl")
LE_PATH    = str(MODEL_DIR / "label_encoder.pkl")

FEATURES   = ["N", "P", "K", "Temperature", "Humidity", "ph", "Rainfall"]
COLORS     = px.colors.qualitative.Set2


# ── Loaders ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

@st.cache_resource
def load_pipeline():
    rf = joblib.load(RF_PATH)
    le = joblib.load(LE_PATH)
    return rf, le


# ── Render ───────────────────────────────────────────────────────────────────
def render():
    section_header("🌾 Crop Recommendation — EDA",
                   "Eksplorasi data, korelasi antar fitur, distribusi per tanaman, "
                   "dan feature importance dari pipeline Random Forest.")

    df      = load_data()
    rf, le  = load_pipeline()

    # Tambah kolom label encoded untuk korelasi
    df["label_enc"] = le.transform(df["label"])

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Distribusi Fitur",
        "🔗 Korelasi",
        "🌿 Rata-rata per Tanaman",
        "🔵 Scatter Plot",
        "⭐ Feature Importance",
    ])

    # ── Tab 1: Distribusi ─────────────────────────────────────────────────
    with tab1:
        col_sel = st.selectbox("Pilih fitur", FEATURES, key="dist_col")
        show_split = st.checkbox("Pisahkan per tanaman", value=False)

        if show_split:
            fig = px.histogram(df, x=col_sel, color="label", nbins=40,
                               template="plotly_white",
                               title=f"Distribusi {col_sel} per Tanaman",
                               color_discrete_sequence=COLORS,
                               barmode="overlay", opacity=0.55)
        else:
            fig = px.histogram(df, x=col_sel, nbins=40,
                               template="plotly_white",
                               title=f"Distribusi {col_sel}",
                               color_discrete_sequence=["#0ea5e9"])
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.box(df, x="label", y=col_sel,
                      title=f"Boxplot {col_sel} per Tanaman",
                      template="plotly_white",
                      color="label",
                      color_discrete_sequence=COLORS)
        fig2.update_layout(showlegend=False, xaxis_tickangle=-40,
                           xaxis_title="", yaxis_title=col_sel)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 2: Korelasi ───────────────────────────────────────────────────
    with tab2:
        st.markdown("##### Korelasi Antar Fitur Numerik")
        st.caption("Sesuai dengan pipeline training — menggunakan semua 7 fitur input.")

        corr = df[FEATURES + ["label_enc"]].corr().round(3)

        fig = px.imshow(corr, text_auto=True, aspect="auto",
                        color_continuous_scale="RdBu_r",
                        zmin=-1, zmax=1,
                        title="Heatmap Korelasi (termasuk Label Encoded)",
                        template="plotly_white")
        fig.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

        # Bar korelasi terhadap label
        corr_label = corr["label_enc"].drop("label_enc").sort_values()
        fig2 = px.bar(
            x=corr_label.values,
            y=corr_label.index,
            orientation="h",
            title="Korelasi Fitur terhadap Label (encoded)",
            template="plotly_white",
            color=corr_label.values,
            color_continuous_scale="RdBu_r",
            text=[f"{v:.3f}" for v in corr_label.values],
            labels={"x": "Korelasi", "y": "Fitur"},
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(coloraxis_showscale=False, xaxis_range=[-0.65, 0.35])
        st.plotly_chart(fig2, use_container_width=True)

        st.info("💡 **P** dan **K** memiliki korelasi negatif terkuat terhadap label, "
                "artinya nilai P/K yang tinggi cenderung mengarah ke tanaman tertentu "
                "di urutan awal alfabet (apple, banana, dll).")

    # ── Tab 3: Rata-rata per tanaman ──────────────────────────────────────
    with tab3:
        feat = st.selectbox("Pilih fitur", FEATURES, key="crop_feat")
        grouped = (df.groupby("label")[feat]
                     .mean()
                     .sort_values(ascending=False)
                     .reset_index())
        grouped.columns = ["Tanaman", "Rata-rata"]

        fig = px.bar(grouped, x="Tanaman", y="Rata-rata",
                     title=f"Rata-rata {feat} per Tanaman",
                     template="plotly_white",
                     color="Rata-rata",
                     color_continuous_scale="Teal",
                     text=grouped["Rata-rata"].apply(lambda x: f"{x:.1f}"))
        fig.update_traces(textposition="outside")
        fig.update_layout(xaxis_tickangle=-40, coloraxis_showscale=False,
                          xaxis_title="", yaxis_title=f"Rata-rata {feat}")
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 4: Scatter ────────────────────────────────────────────────────
    with tab4:
        c1, c2 = st.columns(2)
        x_col = c1.selectbox("Sumbu X", FEATURES, index=0, key="sx")
        y_col = c2.selectbox("Sumbu Y", FEATURES, index=1, key="sy")

        filter_crops = st.multiselect(
            "Filter tanaman (opsional — kosong = tampilkan semua)",
            sorted(df["label"].unique().tolist()),
            default=[], key="scatter_filter"
        )
        plot_df = df[df["label"].isin(filter_crops)] if filter_crops else df

        fig = px.scatter(plot_df, x=x_col, y=y_col, color="label",
                         title=f"{x_col} vs {y_col}",
                         template="plotly_white",
                         opacity=0.7,
                         color_discrete_sequence=COLORS,
                         hover_data={"label": True, x_col: ":.2f", y_col: ":.2f"})
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 5: Feature Importance dari pipeline ───────────────────────────
    with tab5:
        st.caption("Diambil langsung dari `rf_model.pkl` — Random Forest 100 trees "
                   "yang digunakan dalam pipeline prediksi.")

        fi   = rf.feature_importances_
        std  = np.std([t.feature_importances_ for t in rf.estimators_], axis=0)
        pct  = fi * 100

        fi_df = pd.DataFrame({
            "Fitur":      FEATURES,
            "Importance": fi,
            "Std":        std,
            "Persen (%)": pct,
        }).sort_values("Importance", ascending=True).reset_index(drop=True)

        fig = px.bar(fi_df, x="Importance", y="Fitur",
                     orientation="h",
                     error_x="Std",
                     title="Feature Importance — rf_model.pkl (Pipeline Asli)",
                     template="plotly_white",
                     color="Importance",
                     color_continuous_scale="Teal",
                     text=fi_df["Persen (%)"].apply(lambda x: f"{x:.1f}%"))
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False,
                          xaxis_title="Importance Score (Mean Decrease Impurity)",
                          yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        # Tabel ringkas
        tbl = fi_df.sort_values("Importance", ascending=False).copy()
        tbl.insert(0, "Rank", range(1, len(tbl)+1))
        tbl["Importance"] = tbl["Importance"].apply(lambda x: f"{x:.4f}")
        tbl["Std"]        = tbl["Std"].apply(lambda x: f"±{x:.4f}")
        tbl["Persen (%)"] = tbl["Persen (%)"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(tbl[["Rank","Fitur","Persen (%)","Importance","Std"]],
                     use_container_width=True, hide_index=True)

        top = fi_df.iloc[-1]
        st.info(f"💡 **{top['Fitur']}** adalah fitur paling penting "
                f"({top['Persen (%)']:.1f}% kontribusi) dalam model pipeline, "
                "menunjukkan bahwa curah hujan sangat menentukan jenis tanaman yang cocok.")