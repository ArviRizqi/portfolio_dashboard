# projects/_depression_detection/pages/conclusion.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os, sys, warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/smmh_augmented__1_.csv")

COL_MAP = {
    '1. What is your age?': 'age',
    '2. Gender': 'gender',
    '3. Relationship Status': 'relationship',
    '4. Occupation Status': 'occupation',
    '8. What is the average time you spend on social media every day?': 'avg_time_per_day',
    '9. How often do you find yourself using Social media without a specific purpose?': 'without_purpose',
    '10. How often do you get distracted by Social media when you are busy doing something?': 'distracted',
    "11. Do you feel restless if you haven't used Social media in a while?": 'restless',
    '12. On a scale of 1 to 5, how easily distracted are you?': 'distracted_ease',
    '13. On a scale of 1 to 5, how much are you bothered by worries?': 'worries',
    '14. Do you find it difficult to concentrate on things?': 'concentration',
    '15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media?': 'compare_to_others',
    '17. How often do you look to seek validation from features of social media?': 'seek_validation',
    '18. How often do you feel depressed or down?': 'depressed',
    '19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate?': 'daily_activity_flux',
    '20. On a scale of 1 to 5, how often do you face issues regarding sleep?': 'sleeping_issues',
}

NUM_FEATURES = ['without_purpose', 'distracted', 'restless', 'distracted_ease',
                'worries', 'concentration', 'compare_to_others', 'seek_validation',
                'daily_activity_flux', 'sleeping_issues']
NUM_LABELS = {
    'without_purpose': 'Tanpa Tujuan', 'distracted': 'Terdistraksi',
    'restless': 'Gelisah', 'distracted_ease': 'Mudah Teralihkan',
    'worries': 'Kekhawatiran', 'concentration': 'Konsentrasi Sulit',
    'compare_to_others': 'Bandingkan Diri', 'seek_validation': 'Cari Validasi',
    'daily_activity_flux': 'Fluktuasi Aktivitas', 'sleeping_issues': 'Masalah Tidur',
}
DEPRESSION_LABEL = {1: 'Very Low', 2: 'Low', 3: 'Moderate', 4: 'High', 5: 'Very High'}


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.rename(columns=COL_MAP)
    df['depressed_label'] = df['depressed'].map(DEPRESSION_LABEL)
    return df


def render():
    section_header("🧠 Depression Detection — Conclusion",
                   "Ringkasan temuan, arsitektur model, dan rekomendasi.")

    df = load_data()

    # ── 1. Ringkasan Dataset ──────────────────────────────────────────────
    st.markdown("### 📦 Ringkasan Dataset")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Responden",  f"{len(df):,}")
    c2.metric("Fitur Model",      "14")
    c3.metric("Output Kelas",     "5 Level")
    c4.metric("Data Augmented",   "✅ Ya")

    st.markdown("""
    Dataset **SMMH (Social Media & Mental Health)** berisi 2.000 responden (setelah augmentasi)
    yang menjawab survei tentang kebiasaan penggunaan media sosial dan kondisi mental.
    Target variabel adalah **tingkat depresi (1–5)**: Very Low, Low, Moderate, High, Very High.
    Data telah diaugmentasi untuk mengatasi ketidakseimbangan kelas.
    """)

    st.markdown("---")

    # ── 2. Temuan Utama EDA ───────────────────────────────────────────────
    st.markdown("### 🔍 Temuan Utama EDA")

    col_left, col_right = st.columns(2)

    with col_left:
        corr = df[NUM_FEATURES + ['depressed']].corr()['depressed'].drop('depressed').sort_values(ascending=False)
        labels = [NUM_LABELS[f] for f in corr.index]
        fig = px.bar(x=corr.values, y=labels, orientation='h',
                     title='Korelasi Fitur → Level Depresi',
                     template='plotly_white',
                     color=corr.values, color_continuous_scale='RdBu_r',
                     text=[f'{v:.3f}' for v in corr.values])
        fig.update_traces(textposition='outside')
        fig.update_layout(coloraxis_showscale=False, height=320,
                          margin=dict(t=40, b=10, l=10, r=60))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        dep_cnt = df['depressed'].value_counts().sort_index().reset_index()
        dep_cnt.columns = ['Level', 'Jumlah']
        dep_cnt['Label'] = dep_cnt['Level'].map(DEPRESSION_LABEL)
        fig2 = px.bar(dep_cnt, x='Label', y='Jumlah',
                      title='Distribusi Level Depresi (Augmented)',
                      template='plotly_white',
                      color='Level',
                      color_continuous_scale='RdYlGn_r',
                      text='Jumlah')
        fig2.update_traces(textposition='outside')
        fig2.update_layout(coloraxis_showscale=False, height=320,
                           margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    | Temuan | Detail |
    |--------|--------|
    | 😴 **Masalah Tidur** korelasi tertinggi | Insomnia adalah indikator kuat depresi |
    | 😟 **Kekhawatiran & Fluktuasi Aktivitas** | Kedua fitur ini konsisten naik seiring level depresi |
    | 📱 **Durasi >5 jam/hari** | Pengguna sosmed >5 jam memiliki rata-rata depresi tertinggi |
    | 🎓 **University Student** paling rentan | Kelompok terbesar (61%) dengan rata-rata depresi moderat-tinggi |
    | 👩 **Female** sedikit lebih tinggi | Rata-rata depresi wanita sedikit lebih tinggi dari pria |
    """)

    st.markdown("---")

    # ── 3. Arsitektur Model ───────────────────────────────────────────────
    st.markdown("### 🤖 Arsitektur Model (MLP)")

    st.markdown("""
    Model menggunakan **Multi-Layer Perceptron (MLP)** dengan TensorFlow/Keras:
    """)

    arch_df = pd.DataFrame({
        'Layer':      ['Input', 'Dense (ReLU)', 'Dense (ReLU)', 'Dense (ReLU)', 'Output (Softmax)'],
        'Units':      ['14 fitur', '64', '128', '64', '5 kelas'],
        'Activation': ['-', 'ReLU', 'ReLU', 'ReLU', 'Softmax'],
        'Keterangan': [
            'Fitur hasil preprocessing (OHE + Scaling)',
            'Hidden layer 1', 'Hidden layer 2 (terlebar)',
            'Hidden layer 3', 'Output probabilitas 5 kelas depresi',
        ]
    })
    st.dataframe(arch_df, use_container_width=True, hide_index=True)

    st.markdown("""
    **Konfigurasi training:**
    - Optimizer: **Adam**
    - Loss: **Sparse Categorical Crossentropy**
    - Epochs: **50**, Batch size: **16**
    - Preprocessing: **OneHotEncoder** (kategorical) + **StandardScaler** (numerik)
    - Deployment awal: **Gradio** interface + Google Sheets logging
    """)

    st.markdown("---")

    # ── 4. Rekomendasi ────────────────────────────────────────────────────
    st.markdown("### 💡 Rekomendasi")

    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
        <div style="background:#f0fdf4;border-left:4px solid #16a34a;
                    padding:1rem;border-radius:0 8px 8px 0">
            <div style="font-size:1.5rem">🎯</div>
            <strong>Fokus Intervensi</strong><br>
            <small>Prioritaskan pengguna sosmed >5 jam/hari dan yang sering bandingkan diri dengan orang lain.</small>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div style="background:#eff6ff;border-left:4px solid #2563eb;
                    padding:1rem;border-radius:0 8px 8px 0">
            <div style="font-size:1.5rem">🔬</div>
            <strong>Pengembangan Model</strong><br>
            <small>Coba LSTM atau Transformer untuk pola sekuensial. Tambah fitur konten yang dikonsumsi.</small>
        </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
        <div style="background:#fefce8;border-left:4px solid #ca8a04;
                    padding:1rem;border-radius:0 8px 8px 0">
            <div style="font-size:1.5rem">⚠️</div>
            <strong>Etika & Batasan</strong><br>
            <small>Model ini tidak menggantikan diagnosis klinis. Selalu sertakan disclaimer pada setiap prediksi.</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Model: `depression_model.h5` (MLP/Keras) | "
               "Preprocessor: `preprocessor.pkl` | "
               "Data: `smmh_augmented__1_.csv` | 2.000 responden")