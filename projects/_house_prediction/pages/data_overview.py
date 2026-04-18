# projects/_house_prediction/pages/data_overview.py

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

DATA_PATH = str(CURRENT_DIR.parent / "data" / "kc_house_data.csv")


@st.cache_data
def load_data():
    df_raw = pd.read_csv(DATA_PATH)
    df = df_raw.copy()
    df = df.drop(columns=['id', 'date'])
    df = df.dropna(subset=['price'])
    for col in ['bedrooms', 'bathrooms', 'sqft_living', 'condition', 'grade']:
        df[col] = df[col].fillna(df[col].median())
    df['waterfront'] = df['waterfront'].fillna(0)
    df['view']       = df['view'].fillna(0)
    df = df[df['bedrooms'] < 30]
    df['house_age']       = 2015 - df['yr_built']
    df['is_renovated']    = (df['yr_renovated'] > 0).astype(int)
    df['renovated_age']   = np.where(df['yr_renovated'] > 0, 2015 - df['yr_renovated'], 0)
    df['sqft_ratio']      = df['sqft_living'] / (df['sqft_lot'] + 1)
    df['total_rooms']     = df['bedrooms'] + df['bathrooms']
    df['basement_flag']   = (df['sqft_basement'] > 0).astype(int)
    df['sqft_living_log'] = np.log1p(df['sqft_living'])
    return df_raw, df


def render():
    section_header("🏠 House Price Prediction — Data Overview",
                   "Dataset King County WA — 21.613 transaksi properti 2014–2015. "
                   "Menampilkan kondisi sebelum dan sesudah cleaning + feature engineering pipeline.")

    df_raw, df = load_data()

    metric_row({
        "Raw Records":        f"{len(df_raw):,}",
        "Setelah Cleaning":   f"{len(df):,}",
        "Fitur (setelah FE)": df.shape[1],
        "Median Harga":       f"${df['price'].median():,.0f}",
    })

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Sample Data", "📊 Statistik", "🔧 Proses Cleaning", "🛠️ Feature Engineering"
    ])

    with tab1:
        st.markdown("**Data mentah (sebelum cleaning)**")
        show_dataframe(df_raw, max_rows=8)
        st.markdown("**Data setelah cleaning + feature engineering**")
        show_dataframe(df, max_rows=8)

    with tab2:
        num_df = df.select_dtypes(include='number')
        st.dataframe(num_df.describe().round(2), use_container_width=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Harga Min",    f"${df['price'].min():,.0f}")
        c2.metric("Median Harga", f"${df['price'].median():,.0f}")
        c3.metric("Mean Harga",   f"${df['price'].mean():,.0f}")
        c4.metric("Harga Max",    f"${df['price'].max():,.0f}")

    with tab3:
        steps = pd.DataFrame({
            'Langkah': [
                "Hapus kolom 'id' dan 'date'",
                "Hapus baris price kosong",
                "Imputasi median: bedrooms, bathrooms, sqft_living, condition, grade",
                "Imputasi 0: waterfront, view",
                "Hapus outlier bedrooms ≥ 30",
            ],
            'Detail': [
                "2 kolom dihapus",
                f"{df_raw['price'].isnull().sum()} baris dihapus",
                f"{df_raw[['bedrooms','bathrooms','sqft_living','condition','grade']].isnull().sum().sum()} nilai diimputasi",
                f"{df_raw[['waterfront','view']].isnull().sum().sum()} nilai diimputasi",
                f"{(df_raw['bedrooms'] >= 30).sum()} baris dihapus (data entry error)",
            ],
            'Alasan': [
                "Tidak relevan untuk prediksi harga",
                "Target kosong tidak bisa ditraining",
                "Median robust terhadap outlier",
                "Default: tidak ada waterfront/view",
                "33 kamar tidur dengan sqft_living ~1620 = input error",
            ]
        })
        st.dataframe(steps, use_container_width=True, hide_index=True)

        missing_raw = df_raw.isnull().sum()
        missing_cols = missing_raw[missing_raw > 0]
        if len(missing_cols):
            st.markdown("**Missing Values di Raw Data:**")
            m_df = missing_cols.reset_index()
            m_df.columns = ['Kolom', 'Jumlah Missing']
            m_df['% dari Total'] = (m_df['Jumlah Missing'] / len(df_raw) * 100).round(2)
            st.dataframe(m_df, use_container_width=True, hide_index=True)

    with tab4:
        fe_df = pd.DataFrame({
            'Fitur Baru':   ['house_age', 'is_renovated', 'renovated_age',
                             'sqft_ratio', 'total_rooms', 'basement_flag', 'sqft_living_log'],
            'Formula':      ['2015 − yr_built', 'yr_renovated > 0 → 1/0',
                             '2015 − yr_renovated (0 jika belum)',
                             'sqft_living / (sqft_lot + 1)',
                             'bedrooms + bathrooms',
                             'sqft_basement > 0 → 1/0',
                             'log(sqft_living + 1)'],
            'Tujuan':       ['Usia lebih interpretatif', 'Flag boolean renovasi',
                             'Seberapa baru renovasinya', 'Kepadatan bangunan/lahan',
                             'Proxy ukuran & fungsionalitas', 'Flag keberadaan basement',
                             'Normalisasi distribusi right-skewed'],
            'Statistik':    [
                f"Range: {df['house_age'].min()}–{df['house_age'].max()} tahun",
                f"{df['is_renovated'].sum():,} rumah renovasi ({df['is_renovated'].mean()*100:.1f}%)",
                f"Mean (jika renovasi): {df[df['renovated_age']>0]['renovated_age'].mean():.0f} tahun",
                f"Mean: {df['sqft_ratio'].mean():.3f}",
                f"Mean: {df['total_rooms'].mean():.1f} ruang",
                f"{df['basement_flag'].sum():,} rumah ({df['basement_flag'].mean()*100:.1f}%)",
                f"Range: {df['sqft_living_log'].min():.2f}–{df['sqft_living_log'].max():.2f}",
            ],
        })
        st.dataframe(fe_df, use_container_width=True, hide_index=True)