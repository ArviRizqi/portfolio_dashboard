# config.py
# ════════════════════════════════════════════════════════════
#  EDIT FILE INI untuk mengubah profil dan data project
#  tanpa perlu menyentuh app.py
# ════════════════════════════════════════════════════════════


# ── PROFIL ───────────────────────────────────────────────────
PROFILE = {
    "name":    "John Doe",
    "avatar":  "👨‍💻",          # emoji atau hapus jika pakai foto
    # "photo": "assets/photo.jpg",  # uncomment jika pakai foto file
    "bio":     "Data Analyst & ML Engineer. Passionate about turning data into actionable insights.",
    "github":  "https://github.com/johndoe",
    "linkedin":"https://linkedin.com/in/johndoe",
    "skills":  [
        "Python", "Pandas", "Scikit-learn",
        "Streamlit", "Plotly", "SQL",
        "Random Forest", "XGBoost",
    ],
}


# ── PROJECTS ─────────────────────────────────────────────────
# Untuk menambah project baru:
#   1. Tambah entry baru di dict ini
#   2. Buat folder projects/_nama_project/pages/ dengan 4 file:
#      data_overview.py, eda.py, conclusion.py, model_app.py
#   3. Tidak perlu ubah app.py sama sekali
# ─────────────────────────────────────────────────────────────
PROJECTS = {
    "crop-recommendation": {
        "label":  "🌾 Crop Recommendation",
        "title":  "Crop Recommendation",
        "icon":   "🌾",
        "desc":   (
            "Klasifikasi 22 jenis tanaman berdasarkan kondisi tanah & iklim "
            "menggunakan pipeline Random Forest dengan akurasi ~99%."
        ),
        "tags":   ["Classification", "Random Forest", "22 Classes", "2.200 rows"],
        "module": "projects._crop_recomendation.pages",
        "color":  "#0f766e",
        # Detail tambahan untuk halaman project
        "dataset":   "Crop_Recommendation.csv",
        "algorithm": "Random Forest Classifier",
        "accuracy":  "~99%",
        "task":      "Multi-class Classification",
    },

    "house-price-prediction": {
        "label":  "🏠 House Price Prediction",
        "title":  "House Price Prediction",
        "icon":   "🏠",
        "desc":   (
            "Prediksi harga rumah King County WA menggunakan Gradient Boosting "
            "dengan 7 fitur hasil feature engineering. R² = 0.90."
        ),
        "tags":   ["Regression", "Gradient Boosting", "King County WA", "21K rows"],
        "module": "projects._house_prediction.pages",
        "color":  "#1e3a5f",
        "dataset":   "kc_house_data.csv",
        "algorithm": "Gradient Boosting Regressor",
        "accuracy":  "R² = 0.90",
        "task":      "Regression",
    },

    "depression-detection": {
        "label":  "🧠 Depression Detection",
        "title":  "Depression Detection",
        "icon":   "🧠",
        "desc":   (
            "Deteksi tingkat depresi berdasarkan pola penggunaan media sosial "
            "menggunakan Multi-Layer Perceptron (MLP/Keras). "
            "Output: 5 level (Very Low – Very High)."
        ),
        "tags":   ["Classification", "Deep Learning", "MLP", "Mental Health", "2K rows"],
        "module": "projects._depression_detection.pages",
        "color":  "#4c1d95",
        "dataset":   "smmh_augmented__1_.csv",
        "algorithm": "XGBoost Classifier",
        "accuracy":  "~95%",
        "task":      "Multi-class Classification",
    },
}


# ── TABS PER PROJECT ─────────────────────────────────────────
# Urutan dan ikon tab yang muncul di setiap halaman project.
# Kunci harus sesuai dengan nama file di folder pages/
# (tanpa .py), contoh: "data_overview" → data_overview.py
TABS = {
    "Data Overview": {"icon": "📋", "file": "data_overview"},
    "EDA":           {"icon": "📈", "file": "eda"},
    "Conclusion":    {"icon": "📝", "file": "conclusion"},
    "Model App":     {"icon": "🤖", "file": "model_app"},
}


# ── DASHBOARD META ────────────────────────────────────────────
DASHBOARD = {
    "title":    "Data Portfolio Dashboard",
    "subtitle": "Interactive Analytics & Machine Learning Projects",
    "icon":     "📊",
    "footer":   "© 2026 | Data Portfolio",
    "badges":   ["Python", "Machine Learning", "Tabular Data", "Streamlit"],
}