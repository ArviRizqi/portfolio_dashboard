# 📊 Portfolio Dashboard

Multi-project Streamlit dashboard untuk Data Analytics & Machine Learning portfolio.

## 📁 Folder Structure

```
PORTFOLIO_DASHBOARD/
│
├── app.py                          ← Entry point utama (router)
├── requirements.txt
│
├── shared/
│   └── utils.py                   ← Fungsi bersama (metric_row, show_dataframe, dll)
│
└── projects/
    ├── _crop_recomendation/
    │   ├── data/                  ← Letakkan CSV di sini
    │   ├── models/                ← Letakkan .pkl model di sini
    │   └── pages/
    │       ├── data_overview.py
    │       ├── eda.py
    │       ├── model_performance.py
    │       └── feature_importance.py
    │
    └── _house_prediction/
        ├── data/
        ├── models/
        └── pages/
            ├── data_overview.py
            ├── eda.py
            ├── model_performance.py
            └── feature_importance.py
```

## 🚀 Cara Menjalankan

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ➕ Cara Menambahkan Project Baru

1. Buat folder `projects/_nama_project/` dengan subfolder `data/`, `models/`, `pages/`
2. Buat file `data_overview.py`, `eda.py`, `model_performance.py`, `feature_importance.py` di `pages/` — masing-masing dengan fungsi `render()`
3. Tambahkan pilihan di `app.py` pada bagian sidebar radio dan routing `if/elif`

## 🔌 Menghubungkan Data Asli

Di setiap file `pages/`, ganti bagian `_make_sample_df()` dengan:

```python
import pandas as pd
df = pd.read_csv("projects/_nama_project/data/your_file.csv")
```

Untuk model:
```python
import joblib
model = joblib.load("projects/_nama_project/models/model.pkl")
```