# projects/_house_prediction/pages/conclusion.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os, sys, warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header

BASE      = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE, "../data/kc_house_data.csv")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.drop(columns=['id'])
    df = df.dropna(subset=['price'])
    for col in ['bedrooms', 'bathrooms', 'sqft_living', 'condition', 'grade']:
        df[col] = df[col].fillna(df[col].median())
    df['waterfront'] = df['waterfront'].fillna(0)
    df['view']       = df['view'].fillna(0)
    df = df[df['bedrooms'] < 30]
    df['house_age']       = 2015 - df['yr_built']
    df['is_renovated']    = (df['yr_renovated'] > 0).astype(int)
    df['sqft_living_log'] = np.log1p(df['sqft_living'])
    df['total_rooms']     = df['bedrooms'] + df['bathrooms']
    df['basement_flag']   = (df['sqft_basement'] > 0).astype(int)
    return df


def render():
    section_header("🏠 House Price Prediction — Conclusion",
                   "Ringkasan pipeline, temuan EDA, perbandingan model, dan rekomendasi.")

    df = load_data()

    # ── 1. Ringkasan Dataset ──────────────────────────────────────────────
    st.markdown("### 📦 Ringkasan Dataset")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Transaksi",    f"{len(df):,}")
    c2.metric("Fitur (setelah FE)", "22")
    c3.metric("Median Harga",       f"${df['price'].median():,.0f}")
    c4.metric("Range Harga",        "$75K – $7.7M")

    st.markdown("""
    Dataset **King County House Sales** (WA, USA) berisi 21.602 transaksi properti
    periode **Mei 2014 – Mei 2015**. Setelah cleaning (hapus outlier 33 kamar, imputasi median),
    pipeline menambahkan **7 fitur baru** melalui feature engineering untuk meningkatkan
    kemampuan prediksi model.
    """)

    st.markdown("---")

    # ── 2. Temuan Utama EDA ───────────────────────────────────────────────
    st.markdown("### 🔍 Temuan Utama EDA")

    col_left, col_right = st.columns(2)

    with col_left:
        # Korelasi top 8 vs price
        feature_cols = ['sqft_living', 'grade', 'sqft_living_log', 'bathrooms',
                        'total_rooms', 'view', 'is_renovated', 'house_age']
        labels = ['Luas Dalam', 'Grade', 'Log Luas Dalam', 'Kamar Mandi',
                  'Total Ruang', 'View', 'Pernah Renovasi', 'Usia Rumah']
        corr_vals = df[feature_cols + ['price']].corr()['price'].drop('price')

        fig = px.bar(x=corr_vals.values, y=labels, orientation='h',
                     title='Top Korelasi Fitur → Price',
                     template='plotly_white',
                     color=corr_vals.values,
                     color_continuous_scale='RdBu_r',
                     text=[f'{v:.3f}' for v in corr_vals.values])
        fig.update_traces(textposition='outside')
        fig.update_layout(coloraxis_showscale=False, height=320,
                          margin=dict(t=40, b=10, l=10, r=60))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Median price per grade
        grade_grp = df.groupby('grade')['price'].median().reset_index()
        grade_grp.columns = ['Grade', 'Median Price']
        fig2 = px.bar(grade_grp, x='Grade', y='Median Price',
                      title='Median Harga per Grade Konstruksi',
                      template='plotly_white',
                      color='Median Price', color_continuous_scale='Blues',
                      text=grade_grp['Median Price'].apply(lambda x: f'${x/1000:.0f}K'))
        fig2.update_traces(textposition='outside')
        fig2.update_layout(coloraxis_showscale=False, height=320,
                           yaxis_tickformat='$,.0f',
                           margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    | Temuan | Detail |
    |--------|--------|
    | 🏗️ **Grade** faktor kualitas utama | Korelasi 0.667 — grade 13 median $2.98M vs grade 5 hanya $229K |
    | 📐 **sqft_living** faktor fisik terkuat | Korelasi 0.702 — luas bangunan sangat menentukan harga |
    | 🌊 **Waterfront** premium besar | Median $1.4M vs $450K — 3× lebih mahal |
    | 🔨 **Renovasi** menaikkan harga | Median $600K vs $448K — selisih 34% |
    | 📍 **Lokasi (lat)** berpengaruh | Korelasi 0.307 — area utara King County lebih premium |
    | 📉 **house_age** negatif | −0.054 — rumah tua sedikit lebih murah, namun lemah |
    """)

    st.markdown("---")

    # ── 3. Perbandingan Model ─────────────────────────────────────────────
    st.markdown("### 🤖 Perbandingan Model (dari Pipeline)")
    st.caption("Hasil evaluasi pada test set (20% data, 80/20 split, random_state=42).")

    model_df = pd.DataFrame({
        'Model':            ['Gradient Boosting ★', 'Random Forest',
                             'Ridge Regression', 'Lasso Regression', 'Linear Regression'],
        'R²':               [0.9004, 0.8780, 0.7010, 0.6980, 0.7005],
        'MAE':              ['$67,600', '$80,200', '$120,400', '$121,000', '$120,500'],
        'RMSE':             ['$116,000', '$128,500', '$201,800', '$202,300', '$201,900'],
        'MAPE':             ['12.9%', '15.1%', '22.3%', '22.4%', '22.3%'],
        'Keterangan':       ['✅ Model terbaik', 'Alternatif kuat',
                             'Baseline regularized', 'Feature selection otomatis',
                             'Baseline sederhana'],
    })
    st.dataframe(model_df, use_container_width=True, hide_index=True)

    st.markdown("""
    Pipeline menggunakan **Gradient Boosting** sebagai model final dengan konfigurasi:
    - `n_estimators=200`, `learning_rate=0.08`, `max_depth=5`, `subsample=0.8`
    - Preprocessing: **RobustScaler** (tahan outlier) untuk model linear
    - Tree models (RF, GB) tidak memerlukan scaling
    - Cross-validation 5-fold: R² mean = **~0.90**, std kecil → model stabil
    """)

    st.markdown("---")

    # ── 4. 3 Faktor Utama ────────────────────────────────────────────────
    st.markdown("### 💡 3 Faktor Utama Penentu Harga")

    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
        <div style="background:#f0fdf4;border-left:4px solid #16a34a;
                    padding:1rem;border-radius:0 8px 8px 0">
            <div style="font-size:1.5rem">🏗️</div>
            <strong>Grade Konstruksi</strong><br>
            <small>Korelasi terkuat. Grade 7→13 bisa menaikkan harga 7×.</small>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div style="background:#eff6ff;border-left:4px solid #2563eb;
                    padding:1rem;border-radius:0 8px 8px 0">
            <div style="font-size:1.5rem">📐</div>
            <strong>Luas Bangunan (sqft_living)</strong><br>
            <small>Korelasi r=0.70. Setiap +1.000 sqft ≈ +$80K–$120K.</small>
        </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
        <div style="background:#fefce8;border-left:4px solid #ca8a04;
                    padding:1rem;border-radius:0 8px 8px 0">
            <div style="font-size:1.5rem">📍</div>
            <strong>Lokasi Geografis (lat/long)</strong><br>
            <small>Area utara KC (Bellevue, Mercer Island) jauh lebih premium.</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.success("""
    **Rekomendasi pengembangan:**
    - Tambah data zipcode/neighborhood sebagai categorical feature
    - Coba XGBoost atau LightGBM untuk perbandingan dengan GB
    - Tambah fitur jarak ke pusat kota Seattle (haversine dari lat/long)
    - Pertimbangkan prediksi log(price) lalu di-exponentiate untuk kurangi efek outlier
    """)

    st.markdown("---")
    st.caption("Pipeline: `gb_model.pkl` | Scaler: `scaler_house.pkl` | "
               "Data: `kc_house_data.csv` | King County, WA 2014–2015")