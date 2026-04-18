# projects/_house_prediction/pages/eda.py

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

DATA_PATH = str(CURRENT_DIR.parent / "data" / "kc_house_data.csv")

FEATURE_COLS = [
    'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
    'waterfront', 'view', 'condition', 'grade', 'sqft_above',
    'sqft_basement', 'sqft_living15', 'sqft_lot15', 'lat', 'long',
    'house_age', 'is_renovated', 'renovated_age', 'sqft_ratio',
    'total_rooms', 'basement_flag', 'sqft_living_log',
]

FEATURE_LABELS = {
    'bedrooms': 'Kamar Tidur', 'bathrooms': 'Kamar Mandi',
    'sqft_living': 'Luas Dalam (sqft)', 'sqft_lot': 'Luas Lahan (sqft)',
    'floors': 'Lantai', 'waterfront': 'Tepi Air', 'view': 'Skor View',
    'condition': 'Kondisi', 'grade': 'Grade', 'sqft_above': 'Luas Atas (sqft)',
    'sqft_basement': 'Luas Basement (sqft)', 'sqft_living15': 'Luas Tetangga (sqft)',
    'sqft_lot15': 'Lahan Tetangga (sqft)', 'lat': 'Latitude', 'long': 'Longitude',
    'house_age': 'Usia Rumah (th)', 'is_renovated': 'Pernah Renovasi',
    'renovated_age': 'Lama Sejak Renovasi (th)', 'sqft_ratio': 'Rasio Bangunan/Lahan',
    'total_rooms': 'Total Ruang', 'basement_flag': 'Ada Basement',
    'sqft_living_log': 'Log Luas Dalam',
}


# ── Loaders ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%dT%H%M%S', errors='coerce')

    # ── Cleaning persis dari pipeline ──────────────────────────────────
    df = df.drop(columns=['id'])
    df = df.dropna(subset=['price'])
    for col in ['bedrooms', 'bathrooms', 'sqft_living', 'condition', 'grade']:
        df[col] = df[col].fillna(df[col].median())
    df['waterfront'] = df['waterfront'].fillna(0)
    df['view']       = df['view'].fillna(0)
    df = df[df['bedrooms'] < 30]

    # ── Feature engineering persis dari pipeline ──────────────────────
    df['house_age']       = 2015 - df['yr_built']
    df['is_renovated']    = (df['yr_renovated'] > 0).astype(int)
    df['renovated_age']   = np.where(df['yr_renovated'] > 0, 2015 - df['yr_renovated'], 0)
    df['sqft_ratio']      = df['sqft_living'] / (df['sqft_lot'] + 1)
    df['total_rooms']     = df['bedrooms'] + df['bathrooms']
    df['basement_flag']   = (df['sqft_basement'] > 0).astype(int)
    df['sqft_living_log'] = np.log1p(df['sqft_living'])

    df['year_month']       = df['date'].dt.to_period('M').astype(str)
    df['waterfront_label'] = df['waterfront'].apply(lambda x: 'Waterfront' if x == 1 else 'Non-Waterfront')
    df['renovated_label']  = df['is_renovated'].apply(lambda x: 'Renovasi' if x == 1 else 'Tidak Renovasi')
    df['basement_label']   = df['basement_flag'].apply(lambda x: 'Ada Basement' if x == 1 else 'Tanpa Basement')

    return df


# ── Render ───────────────────────────────────────────────────────────────────
def render():
    section_header("🏠 House Price Prediction — EDA",
                   "Eksplorasi data King County WA dengan feature engineering dari pipeline: "
                   "house_age, is_renovated, sqft_ratio, total_rooms, basement_flag, sqft_living_log.")

    df = load_data()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💰 Distribusi Harga",
        "🔗 Korelasi",
        "📐 Fitur vs Harga",
        "🏗️ Feature Engineering",
        "🗓️ Tren Waktu",
        "⭐ Feature Importance",
    ])

    # ── Tab 1: Distribusi harga ───────────────────────────────────────────
    with tab1:
        c1, c2 = st.columns(2)

        with c1:
            fig = px.histogram(df, x='price', nbins=80,
                               title='Distribusi Harga (Raw)',
                               template='plotly_white',
                               color_discrete_sequence=['#0ea5e9'],
                               labels={'price': 'Harga (USD)'})
            fig.update_layout(xaxis_tickformat='$,.0f', yaxis_title='Frekuensi')
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig2 = px.histogram(df, x=np.log1p(df['price']), nbins=60,
                                title='Distribusi Harga (Log Scale — lebih normal)',
                                template='plotly_white',
                                color_discrete_sequence=['#0f766e'],
                                labels={'x': 'log(Harga + 1)'})
            fig2.update_layout(yaxis_title='Frekuensi')
            st.plotly_chart(fig2, use_container_width=True)

        st.info("💡 Distribusi harga **right-skewed** — mayoritas rumah bernilai "
                "$322K–$645K, namun ada outlier hingga $7.7M. "
                "Log transform membantu model regresi linear bekerja lebih baik.")

        # Stats cards
        c1, c2, c3, c4 = st.columns(4)
        c1.metric('Minimum',  f"${df['price'].min():,.0f}")
        c2.metric('Median',   f"${df['price'].median():,.0f}")
        c3.metric('Mean',     f"${df['price'].mean():,.0f}")
        c4.metric('Maximum',  f"${df['price'].max():,.0f}")

    # ── Tab 2: Korelasi ───────────────────────────────────────────────────
    with tab2:
        st.markdown("##### Korelasi semua fitur (termasuk engineered features) terhadap Price")
        st.caption("Feature engineering dari pipeline menambah 7 fitur baru.")

        corr_all = df[FEATURE_COLS + ['price']].corr().round(3)

        # Heatmap subset fitur paling relevan
        top_feats = corr_all['price'].drop('price').abs().sort_values(ascending=False).head(12).index.tolist()
        corr_sub  = df[top_feats + ['price']].corr().round(3)

        fig = px.imshow(corr_sub, text_auto=True, aspect='auto',
                        color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                        title='Heatmap Korelasi — Top 12 Fitur + Price',
                        template='plotly_white')
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

        # Bar korelasi vs price
        corr_price = corr_all['price'].drop('price').sort_values(ascending=False)
        labels     = [FEATURE_LABELS.get(f, f) for f in corr_price.index]

        fig2 = px.bar(x=corr_price.values, y=labels, orientation='h',
                      title='Korelasi Seluruh Fitur terhadap Price',
                      template='plotly_white',
                      color=corr_price.values,
                      color_continuous_scale='RdBu_r',
                      text=[f'{v:.3f}' for v in corr_price.values],
                      labels={'x': 'Korelasi', 'y': 'Fitur'})
        fig2.update_traces(textposition='outside')
        fig2.update_layout(coloraxis_showscale=False, height=550,
                           xaxis_range=[-0.2, 0.85])
        st.plotly_chart(fig2, use_container_width=True)

        st.info("💡 **sqft_living** (r=0.70) dan **grade** (r=0.67) adalah dua fitur "
                "dengan korelasi tertinggi. Fitur engineered **sqft_living_log** (r=0.61) "
                "mengungguli beberapa fitur asli.")

    # ── Tab 3: Fitur vs Harga ─────────────────────────────────────────────
    with tab3:
        feat_options = {FEATURE_LABELS.get(f, f): f for f in FEATURE_COLS
                        if f not in ['waterfront', 'is_renovated', 'basement_flag',
                                     'lat', 'long', 'sqft_living_log']}
        feat_label = st.selectbox('Pilih fitur', list(feat_options.keys()))
        feat       = feat_options[feat_label]

        sample = df.sample(min(3000, len(df)), random_state=42)
        fig = px.scatter(sample, x=feat, y='price',
                         color='grade', trendline='ols',
                         title=f'{feat_label} vs Harga (sample 3.000, warna = grade)',
                         template='plotly_white', opacity=0.55,
                         labels={feat: feat_label, 'price': 'Harga (USD)'})
        fig.update_layout(yaxis_tickformat='$,.0f')
        st.plotly_chart(fig, use_container_width=True)

        # Box per grade
        fig2 = px.box(df, x='grade', y='price',
                      title='Distribusi Harga per Grade Konstruksi',
                      template='plotly_white',
                      color='grade')
        fig2.update_layout(showlegend=False, yaxis_tickformat='$,.0f',
                           xaxis_title='Grade', yaxis_title='Harga (USD)')
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 4: Feature Engineering ────────────────────────────────────────
    with tab4:
        st.markdown("##### 7 Fitur Baru dari Pipeline")
        st.caption("Fitur-fitur ini dibuat di Step 3 pipeline untuk meningkatkan performa model.")

        eng_info = pd.DataFrame({
            'Fitur Baru':   ['house_age', 'is_renovated', 'renovated_age',
                             'sqft_ratio', 'total_rooms', 'basement_flag', 'sqft_living_log'],
            'Formula':      ['2015 - yr_built', 'yr_renovated > 0 → 1/0',
                             '2015 - yr_renovated (0 jika belum)', 'sqft_living / sqft_lot',
                             'bedrooms + bathrooms', 'sqft_basement > 0 → 1/0',
                             'log(sqft_living + 1)'],
            'Tujuan':       ['Usia rumah lebih interpretatif', 'Flag renovasi',
                             'Berapa lama sejak renovasi terakhir',
                             'Rasio kepadatan bangunan terhadap lahan',
                             'Proxy ukuran & fungsionalitas rumah',
                             'Flag keberadaan basement',
                             'Kurangi right-skew distribusi luas'],
            'Korelasi ke Price': ['−0.054', '0.126', '0.069', '0.123',
                                  '0.470', '0.180', '0.611'],
        })
        st.dataframe(eng_info, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Visualisasi fitur engineering
        c1, c2 = st.columns(2)

        with c1:
            fig = px.box(df, x='waterfront_label', y='price',
                         title='Harga: Waterfront vs Non-Waterfront',
                         template='plotly_white',
                         color='waterfront_label',
                         color_discrete_map={'Waterfront': '#0ea5e9',
                                             'Non-Waterfront': '#94a3b8'})
            fig.update_layout(showlegend=False, yaxis_tickformat='$,.0f',
                              xaxis_title='', yaxis_title='Harga (USD)')
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Waterfront: median $1.4M vs $450K — 3× lebih mahal")

        with c2:
            fig2 = px.box(df, x='renovated_label', y='price',
                          title='Harga: Renovasi vs Tidak',
                          template='plotly_white',
                          color='renovated_label',
                          color_discrete_map={'Renovasi': '#0f766e',
                                              'Tidak Renovasi': '#94a3b8'})
            fig2.update_layout(showlegend=False, yaxis_tickformat='$,.0f',
                               xaxis_title='', yaxis_title='Harga (USD)')
            st.plotly_chart(fig2, use_container_width=True)
            st.caption("Renovasi: median $600K vs $448K — 34% lebih tinggi")

        c3, c4 = st.columns(2)
        with c3:
            fig3 = px.histogram(df, x='house_age', color='basement_label',
                                nbins=40, barmode='overlay', opacity=0.7,
                                title='Distribusi Usia Rumah (dengan/tanpa Basement)',
                                template='plotly_white',
                                color_discrete_map={'Ada Basement': '#0ea5e9',
                                                    'Tanpa Basement': '#f59e0b'},
                                labels={'house_age': 'Usia Rumah (tahun)'})
            st.plotly_chart(fig3, use_container_width=True)

        with c4:
            fig4 = px.scatter(df.sample(2000, random_state=1), x='sqft_ratio', y='price',
                              title='Rasio Bangunan/Lahan vs Harga',
                              template='plotly_white', opacity=0.5,
                              color_discrete_sequence=['#0ea5e9'],
                              labels={'sqft_ratio': 'sqft_ratio', 'price': 'Harga (USD)'})
            fig4.update_layout(yaxis_tickformat='$,.0f', xaxis_range=[0, 1])
            st.plotly_chart(fig4, use_container_width=True)

    # ── Tab 5: Tren Waktu ─────────────────────────────────────────────────
    with tab5:
        monthly = df.groupby('year_month').agg(
            median_price=('price', 'median'),
            count=('price', 'count')
        ).reset_index()

        fig = px.line(monthly, x='year_month', y='median_price',
                      title='Tren Median Harga per Bulan (Mei 2014 – Mei 2015)',
                      template='plotly_white', markers=True,
                      labels={'year_month': 'Bulan', 'median_price': 'Median Harga (USD)'})
        fig.update_layout(yaxis_tickformat='$,.0f')
        fig.update_traces(line_color='#0ea5e9', marker_color='#0f766e')
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(monthly, x='year_month', y='count',
                      title='Volume Transaksi per Bulan',
                      template='plotly_white',
                      color='count', color_continuous_scale='Blues',
                      labels={'year_month': 'Bulan', 'count': 'Jumlah Transaksi'})
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

        st.info("💡 Harga tertinggi di **April–Mei** (musim semi) dan terendah di "
                "**Februari** — pola musiman pasar properti AS yang umum.")

    # ── Tab 6: Feature Importance ─────────────────────────────────────────
    with tab6:
        st.caption("⏳ Feature importance akan ditampilkan setelah file model pipeline "
                   "(`gb_model.pkl`) diunggah ke `projects/_house_prediction/models/`.")

        # Sementara — tampilkan korelasi sebagai proxy importance
        st.markdown("##### Proxy: Korelasi Absolut terhadap Price")
        st.caption("Akan diganti dengan feature importance dari Gradient Boosting pipeline "
                   "setelah model diunggah.")

        corr_abs = df[FEATURE_COLS + ['price']].corr()['price'] \
                     .drop('price').abs().sort_values(ascending=True)
        labels_abs = [FEATURE_LABELS.get(f, f) for f in corr_abs.index]

        fig = px.bar(x=corr_abs.values, y=labels_abs, orientation='h',
                     title='|Korelasi| Fitur terhadap Price (proxy importance)',
                     template='plotly_white',
                     color=corr_abs.values, color_continuous_scale='Blues',
                     text=[f'{v:.3f}' for v in corr_abs.values],
                     labels={'x': '|Korelasi|', 'y': 'Fitur'})
        fig.update_traces(textposition='outside')
        fig.update_layout(coloraxis_showscale=False, height=550)
        st.plotly_chart(fig, use_container_width=True)

        st.info("🔄 **Setelah model diunggah**, tab ini akan menampilkan "
                "feature importance langsung dari `gb_model.pkl` "
                "(Gradient Boosting — model terbaik di pipeline).")