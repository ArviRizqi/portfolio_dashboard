import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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
DATA_PATH  = str(CURRENT_DIR.parent / "data" / "smmh_augmented.csv")

COLORS = px.colors.qualitative.Set2

# ── Mapping ──────────────────────────────────────────────────────────────────
COL_MAP = {
    '1. What is your age?': 'age',
    '2. Gender': 'gender',
    '3. Relationship Status': 'relationship',
    '4. Occupation Status': 'occupation',
    '5. What type of organizations are you affiliated with?': 'affiliate_organization',
    '6. Do you use social media?': 'use_sosmed',
    '7. What social media platforms do you commonly use?': 'sosmed_platform',
    '8. What is the average time you spend on social media every day?': 'avg_time_per_day',
    '9. How often do you find yourself using Social media without a specific purpose?': 'without_purpose',
    '10. How often do you get distracted by Social media when you are busy doing something?': 'distracted',
    "11. Do you feel restless if you haven't used Social media in a while?": 'restless',
    '12. On a scale of 1 to 5, how easily distracted are you?': 'distracted_ease',
    '13. On a scale of 1 to 5, how much are you bothered by worries?': 'worries',
    '14. Do you find it difficult to concentrate on things?': 'concentration',
    '15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media?': 'compare_to_others',
    '16. Following the previous question, how do you feel about these comparisons, generally speaking?': 'validation',
    '17. How often do you look to seek validation from features of social media?': 'seek_validation',
    '18. How often do you feel depressed or down?': 'depressed',
    '19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate?': 'daily_activity_flux',
    '20. On a scale of 1 to 5, how often do you face issues regarding sleep?': 'sleeping_issues',
}

DEPRESSION_LABEL = {1: 'Very Low', 2: 'Low', 3: 'Moderate', 4: 'High', 5: 'Very High'}

# ── Loaders ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.rename(columns=COL_MAP)
    df = df.drop(columns=['Timestamp'], errors='ignore')
    df['depressed_label'] = df['depressed'].map(DEPRESSION_LABEL)
    return df

# ── Render ───────────────────────────────────────────────────────────────────
def render():
    section_header("🧠 Depression Detection — EDA",
                   "Eksplorasi dataset SMMH: distribusi usia & gender, "
                   "korelasi indikator psikologis, serta tren penggunaan sosmed.")

    df = load_data()

    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Distribusi Demografis",
        "🔗 Korelasi Psikologis",
        "📱 Kebiasaan Sosmed",
        "📊 Perbandingan Depresi"
    ])

    # ── Tab 1: Demografis ─────────────────────────────────────────────────
    with tab1:
        c1, c2 = st.columns(2)
        
        with c1:
            fig = px.histogram(df, x="age", color="gender", nbins=40,
                               template="plotly_white",
                               title="Distribusi Usia & Gender Responden",
                               color_discrete_sequence=COLORS)
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            gender_cnt = df['gender'].value_counts().reset_index()
            gender_cnt.columns = ['Gender', 'Jumlah']
            fig2 = px.pie(gender_cnt, names="Gender", values="Jumlah",
                          title="Komposisi Gender", hole=0.4,
                          color_discrete_sequence=COLORS)
            st.plotly_chart(fig2, use_container_width=True)

        st.info("💡 Mayoritas responden berada di rentang usia remaja dan dewasa muda (18 - 30 tahun), dengan proporsi gender yang cukup representatif di berbagai demografi.")

    # ── Tab 2: Korelasi ───────────────────────────────────────────────────
    with tab2:
        st.markdown("##### Heatmap Korelasi Indikator Psikologis vs Tingkat Depresi")
        
        # Ambil kolom numerik/skor
        num_cols = ['without_purpose', 'distracted', 'restless', 'distracted_ease', 
                    'worries', 'concentration', 'compare_to_others', 'validation', 
                    'seek_validation', 'daily_activity_flux', 'sleeping_issues', 'depressed']
                    
        corr = df[num_cols].corr().round(2)

        fig = px.imshow(corr, text_auto=True, aspect="auto",
                        color_continuous_scale="RdBu_r",
                        zmin=-1, zmax=1,
                        title="Matriks Korelasi (Pearson)",
                        template="plotly_white")
        fig.update_layout(height=600, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        corr_label = corr["depressed"].drop("depressed").sort_values()
        fig2 = px.bar(
            x=corr_label.values,
            y=corr_label.index,
            orientation="h",
            title="Korelasi Setiap Fitur terhadap Level Depresi",
            template="plotly_white",
            color=corr_label.values,
            color_continuous_scale="RdBu_r",
            labels={"x": "Korelasi", "y": "Fitur psikologis"},
            text=[f"{v:.2f}" for v in corr_label.values]
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 3: Kebiasaan Sosmed ──────────────────────────────────────────
    with tab3:
        st.markdown("##### Waktu Penggunaan Sosmed per Hari")
        
        time_dist = df['avg_time_per_day'].value_counts().reset_index()
        time_dist.columns = ['Waktu per Hari', 'Frekuensi']
        
        fig = px.bar(time_dist, x='Frekuensi', y='Waktu per Hari', orientation='h',
                     title="Berapa lama mereka bermain Sosmed?", 
                     color_discrete_sequence=['#0ea5e9'], template="plotly_white")
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("##### Rata-rata Skor Depresi Berdasarkan Waktu di Sosmed")
        group_dep = df.groupby('avg_time_per_day')['depressed'].mean().sort_values().reset_index()
        fig2 = px.bar(group_dep, x='avg_time_per_day', y='depressed',
                      title="Apakah waktu layar memperburuk depresi?",
                      color='depressed', color_continuous_scale="Teal",
                      template="plotly_white",
                      text=[f"{v:.2f}" for v in group_dep['depressed']])
        fig2.update_traces(textposition="outside")
        fig2.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 4: Perbandingan Status ────────────────────────────────────────
    with tab4:
        c1, c2 = st.columns(2)
        with c1:
            fig_occ = px.box(df, x="occupation", y="depressed", color="occupation",
                             title="Tingkat Depresi berdasar Pekerjaan",
                             template="plotly_white", color_discrete_sequence=COLORS)
            fig_occ.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_occ, use_container_width=True)
            
        with c2:
            fig_rel = px.box(df, x="relationship", y="depressed", color="relationship",
                             title="Tingkat Depresi berdasar Status Hubungan",
                             template="plotly_white", color_discrete_sequence=COLORS)
            fig_rel.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_rel, use_container_width=True)