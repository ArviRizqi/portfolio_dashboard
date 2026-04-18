# projects/_depression_detection/pages/eda.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
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
COLORS_DEP = ['#22c55e', '#84cc16', '#f59e0b', '#f97316', '#ef4444']

NUM_FEATURES = [
    'without_purpose', 'distracted', 'restless', 'distracted_ease',
    'worries', 'concentration', 'compare_to_others', 'seek_validation',
    'daily_activity_flux', 'sleeping_issues',
]
NUM_LABELS = {
    'without_purpose': 'Tanpa Tujuan',
    'distracted': 'Terdistraksi',
    'restless': 'Gelisah',
    'distracted_ease': 'Mudah Teralihkan',
    'worries': 'Kekhawatiran',
    'concentration': 'Konsentrasi Sulit',
    'compare_to_others': 'Bandingkan Diri',
    'seek_validation': 'Cari Validasi',
    'daily_activity_flux': 'Fluktuasi Aktivitas',
    'sleeping_issues': 'Masalah Tidur',
}

TIME_ORDER = [
    'Less than an Hour', 'Between 1 and 2 hours', 'Between 2 and 3 hours',
    'Between 3 and 4 hours', 'Between 4 and 5 hours', 'More than 5 hours',
]


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.rename(columns=COL_MAP)
    df = df.drop(columns=['Timestamp'], errors='ignore')
    df['depressed_label'] = df['depressed'].map(DEPRESSION_LABEL)
    # Normalize gender
    def norm_gender(g):
        g = str(g).strip().lower()
        if 'female' in g: return 'Female'
        if 'male' in g: return 'Male'
        return 'Other'
    df['gender_group'] = df['gender'].apply(norm_gender)
    return df


def render():
    section_header("🧠 Depression Detection — EDA",
                   "Analisis pola penggunaan media sosial, demografi, dan hubungannya dengan tingkat depresi.")

    df = load_data()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 Demografi",
        "📱 Penggunaan Sosmed",
        "🧪 Fitur vs Depresi",
        "🔗 Korelasi",
        "📊 Distribusi Target",
    ])

    # ── Tab 1: Demografi ──────────────────────────────────────────────────
    with tab1:
        c1, c2 = st.columns(2)

        with c1:
            gender_cnt = df['gender_group'].value_counts().reset_index()
            gender_cnt.columns = ['Gender', 'Jumlah']
            fig = px.pie(gender_cnt, names='Gender', values='Jumlah',
                         title='Distribusi Gender',
                         template='plotly_white',
                         color_discrete_sequence=['#0ea5e9', '#f472b6', '#94a3b8'])
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            occ_cnt = df['occupation'].value_counts().reset_index()
            occ_cnt.columns = ['Occupation', 'Jumlah']
            fig2 = px.bar(occ_cnt, x='Jumlah', y='Occupation', orientation='h',
                          title='Distribusi Pekerjaan',
                          template='plotly_white',
                          color='Jumlah', color_continuous_scale='Blues',
                          text='Jumlah')
            fig2.update_traces(textposition='outside')
            fig2.update_layout(coloraxis_showscale=False, yaxis_title='')
            st.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns(2)

        with c3:
            fig3 = px.histogram(df, x='age', nbins=30,
                                title='Distribusi Usia Responden',
                                template='plotly_white',
                                color_discrete_sequence=['#0ea5e9'],
                                labels={'age': 'Usia'})
            fig3.update_layout(yaxis_title='Frekuensi')
            st.plotly_chart(fig3, use_container_width=True)

        with c4:
            rel_cnt = df['relationship'].value_counts().reset_index()
            rel_cnt.columns = ['Status', 'Jumlah']
            fig4 = px.pie(rel_cnt, names='Status', values='Jumlah',
                          title='Status Hubungan',
                          template='plotly_white',
                          color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig4, use_container_width=True)

        # Depresi per demografi
        st.markdown("**Rata-rata Tingkat Depresi per Kelompok**")
        d1, d2 = st.columns(2)

        with d1:
            grp = df.groupby('gender_group')['depressed'].mean().reset_index()
            grp.columns = ['Gender', 'Rata-rata Depresi']
            fig5 = px.bar(grp, x='Gender', y='Rata-rata Depresi',
                          template='plotly_white', color='Rata-rata Depresi',
                          color_continuous_scale='RdYlGn_r',
                          text=grp['Rata-rata Depresi'].apply(lambda x: f'{x:.2f}'),
                          title='Depresi per Gender')
            fig5.update_traces(textposition='outside')
            fig5.update_layout(coloraxis_showscale=False, yaxis_range=[0, 5])
            st.plotly_chart(fig5, use_container_width=True)

        with d2:
            grp2 = df.groupby('occupation')['depressed'].mean().sort_values(ascending=False).reset_index()
            grp2.columns = ['Occupation', 'Rata-rata Depresi']
            fig6 = px.bar(grp2, x='Occupation', y='Rata-rata Depresi',
                          template='plotly_white', color='Rata-rata Depresi',
                          color_continuous_scale='RdYlGn_r',
                          text=grp2['Rata-rata Depresi'].apply(lambda x: f'{x:.2f}'),
                          title='Depresi per Pekerjaan')
            fig6.update_traces(textposition='outside')
            fig6.update_layout(coloraxis_showscale=False, yaxis_range=[0, 5],
                               xaxis_tickangle=-15)
            st.plotly_chart(fig6, use_container_width=True)

    # ── Tab 2: Penggunaan Sosmed ──────────────────────────────────────────
    with tab2:
        # Platform terpopuler
        platforms = []
        for row in df['sosmed_platform'].dropna():
            for p in str(row).split(','):
                platforms.append(p.strip())
        platform_cnt = pd.DataFrame(Counter(platforms).most_common(10),
                                    columns=['Platform', 'Jumlah'])
        fig = px.bar(platform_cnt, x='Jumlah', y='Platform', orientation='h',
                     title='Platform Media Sosial Terpopuler',
                     template='plotly_white',
                     color='Jumlah', color_continuous_scale='Blues',
                     text='Jumlah')
        fig.update_traces(textposition='outside')
        fig.update_layout(coloraxis_showscale=False, yaxis_title='')
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)

        with c1:
            # Waktu penggunaan
            time_cnt = df['avg_time_per_day'].value_counts().reindex(TIME_ORDER, fill_value=0).reset_index()
            time_cnt.columns = ['Durasi', 'Jumlah']
            fig2 = px.bar(time_cnt, x='Durasi', y='Jumlah',
                          title='Durasi Harian Penggunaan Sosmed',
                          template='plotly_white',
                          color='Jumlah', color_continuous_scale='Blues',
                          text='Jumlah')
            fig2.update_traces(textposition='outside')
            fig2.update_layout(coloraxis_showscale=False, xaxis_tickangle=-20)
            st.plotly_chart(fig2, use_container_width=True)

        with c2:
            # Waktu vs tingkat depresi
            time_dep = df.groupby('avg_time_per_day')['depressed'].mean().reindex(TIME_ORDER).reset_index()
            time_dep.columns = ['Durasi', 'Rata-rata Depresi']
            fig3 = px.bar(time_dep, x='Durasi', y='Rata-rata Depresi',
                          title='Durasi Sosmed vs Rata-rata Depresi',
                          template='plotly_white',
                          color='Rata-rata Depresi',
                          color_continuous_scale='RdYlGn_r',
                          text=time_dep['Rata-rata Depresi'].apply(lambda x: f'{x:.2f}'))
            fig3.update_traces(textposition='outside')
            fig3.update_layout(coloraxis_showscale=False, xaxis_tickangle=-20,
                               yaxis_range=[0, 5])
            st.plotly_chart(fig3, use_container_width=True)

        st.info("💡 Semakin lama penggunaan media sosial per hari, rata-rata tingkat depresi "
                "cenderung **lebih tinggi** — terutama pada pengguna >5 jam/hari.")

    # ── Tab 3: Fitur vs Depresi ───────────────────────────────────────────
    with tab3:
        feat_label = st.selectbox(
            "Pilih fitur",
            list(NUM_LABELS.keys()),
            format_func=lambda x: NUM_LABELS[x]
        )

        c1, c2 = st.columns(2)

        with c1:
            fig = px.box(df, x='depressed', y=feat_label,
                         title=f'{NUM_LABELS[feat_label]} per Level Depresi',
                         template='plotly_white',
                         color='depressed',
                         color_continuous_scale='RdYlGn_r',
                         labels={'depressed': 'Level Depresi', feat_label: NUM_LABELS[feat_label]})
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            grp = df.groupby('depressed')[feat_label].mean().reset_index()
            grp.columns = ['Level Depresi', 'Rata-rata']
            grp['Label'] = grp['Level Depresi'].map(DEPRESSION_LABEL)
            fig2 = px.bar(grp, x='Label', y='Rata-rata',
                          title=f'Rata-rata {NUM_LABELS[feat_label]} per Level',
                          template='plotly_white',
                          color='Rata-rata',
                          color_continuous_scale='RdYlGn_r',
                          text=grp['Rata-rata'].apply(lambda x: f'{x:.2f}'))
            fig2.update_traces(textposition='outside')
            fig2.update_layout(coloraxis_showscale=False,
                               xaxis_title='Level Depresi', yaxis_range=[0, 5])
            st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 4: Korelasi ───────────────────────────────────────────────────
    with tab4:
        num_cols = NUM_FEATURES + ['depressed']
        corr = df[num_cols].corr().round(3)

        fig = px.imshow(corr, text_auto=True, aspect='auto',
                        color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                        title='Heatmap Korelasi Fitur Numerik',
                        template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

        # Bar korelasi vs depressed
        corr_dep = corr['depressed'].drop('depressed').sort_values(ascending=False)
        labels   = [NUM_LABELS.get(f, f) for f in corr_dep.index]

        fig2 = px.bar(x=corr_dep.values, y=labels, orientation='h',
                      title='Korelasi Fitur terhadap Tingkat Depresi',
                      template='plotly_white',
                      color=corr_dep.values,
                      color_continuous_scale='RdBu_r',
                      text=[f'{v:.3f}' for v in corr_dep.values],
                      labels={'x': 'Korelasi', 'y': 'Fitur'})
        fig2.update_traces(textposition='outside')
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

        top = corr_dep.idxmax()
        st.info(f"💡 **{NUM_LABELS[top]}** memiliki korelasi tertinggi "
                f"({corr_dep[top]:.3f}) terhadap tingkat depresi.")

    # ── Tab 5: Distribusi Target ──────────────────────────────────────────
    with tab5:
        c1, c2 = st.columns(2)

        with c1:
            dep_cnt = df['depressed'].value_counts().sort_index().reset_index()
            dep_cnt.columns = ['Level', 'Jumlah']
            dep_cnt['Label'] = dep_cnt['Level'].map(DEPRESSION_LABEL)
            fig = px.bar(dep_cnt, x='Label', y='Jumlah',
                         title='Distribusi Level Depresi',
                         template='plotly_white',
                         color='Level',
                         color_continuous_scale='RdYlGn_r',
                         text='Jumlah')
            fig.update_traces(textposition='outside')
            fig.update_layout(coloraxis_showscale=False,
                              xaxis_title='Level Depresi')
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig2 = px.pie(dep_cnt, names='Label', values='Jumlah',
                          title='Proporsi Level Depresi',
                          template='plotly_white',
                          color_discrete_sequence=COLORS_DEP)
            st.plotly_chart(fig2, use_container_width=True)

        st.info("💡 Dataset **tidak seimbang sempurna** — level Moderate (3) dan High (4) "
                "mendominasi (~47% gabungan), sementara Very Low (1) hanya ~11%. "
                "Augmentasi data telah dilakukan untuk menyeimbangkan distribusi.")