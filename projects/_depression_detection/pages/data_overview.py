# projects/_depression_detection/pages/data_overview.py

import streamlit as st
import pandas as pd
import numpy as np
import sys, os, warnings
warnings.filterwarnings("ignore")
from pathlib import Path

# Resolve path
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from shared.utils import section_header, metric_row, show_dataframe

DATA_PATH = str(CURRENT_DIR.parent / "data" / "smmh_augmented__1_.csv")

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


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.rename(columns=COL_MAP)
    df = df.drop(columns=['Timestamp'], errors='ignore')
    df['depressed_label'] = df['depressed'].map(DEPRESSION_LABEL)
    return df


def render():
    section_header("🧠 Depression Detection — Data Overview",
                   "Dataset survei penggunaan media sosial dan tingkat depresi (SMMH Augmented, 2.000 responden).")

    df = load_data()

    metric_row({
        "Total Responden":    f"{len(df):,}",
        "Fitur Input":        "14",
        "Level Depresi":      "5 (Very Low – Very High)",
        "Missing Values":     int(df.isnull().sum().sum()),
    })

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄 Sample Data", "📊 Statistik", "📋 Info Kolom"])

    with tab1:
        show_dataframe(df.drop(columns=['depressed_label']), max_rows=8)
        st.caption(f"Dataset: `smmh_augmented__1_.csv` — {len(df):,} baris × {df.shape[1]-1} kolom")

    with tab2:
        st.markdown("**Statistik Deskriptif — Fitur Numerik**")
        num_cols = ['age', 'without_purpose', 'distracted', 'restless',
                    'distracted_ease', 'worries', 'concentration',
                    'compare_to_others', 'validation', 'seek_validation',
                    'daily_activity_flux', 'sleeping_issues', 'depressed']
        st.dataframe(df[num_cols].describe().round(2), use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Rata-rata Usia",    f"{df['age'].mean():.1f} tahun")
        c2.metric("Median Depresi",    f"{df['depressed'].median():.0f} / 5")
        c3.metric("Mayoritas Responden", df['occupation'].value_counts().index[0])

    with tab3:
        info_df = pd.DataFrame({
            "Kolom (renamed)": df.columns.drop('depressed_label').tolist(),
            "Tipe Data":       [str(df[c].dtype) for c in df.columns if c != 'depressed_label'],
            "Non-Null":        [df[c].notnull().sum() for c in df.columns if c != 'depressed_label'],
            "Unique Values":   [df[c].nunique() for c in df.columns if c != 'depressed_label'],
        })
        st.dataframe(info_df, use_container_width=True, hide_index=True)

        st.markdown("**Distribusi Level Depresi (Target)**")
        dist = df['depressed'].value_counts().sort_index().reset_index()
        dist.columns = ['Level', 'Jumlah']
        dist['Label']       = dist['Level'].map(DEPRESSION_LABEL)
        dist['Persentase']  = (dist['Jumlah'] / len(df) * 100).round(1).astype(str) + '%'
        st.dataframe(dist[['Level', 'Label', 'Jumlah', 'Persentase']],
                     use_container_width=True, hide_index=True)