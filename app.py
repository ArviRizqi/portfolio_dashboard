import streamlit as st
import sys
import os
import importlib

# ======================
# PATH FIX
# ======================
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Portfolio Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# CUSTOM CSS
# ======================
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f766e 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { margin: 0; font-size: 2rem; }
    .main-header p  { margin: 0.5rem 0 0; opacity: 0.85; }
    .kpi-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        text-align: center;
    }
    .kpi-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
    }
    .breadcrumb {
        background: #f1f5f9;
        border-left: 4px solid #0ea5e9;
        padding: 0.5rem 1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        color: #475569;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# SIDEBAR NAVIGATION
# ======================
with st.sidebar:
    st.markdown("## 📊 Portfolio")
    st.markdown("---")

    st.markdown("### 📂 Project")
    project = st.radio(
        "project_select",
        ["🌾 Crop Recommendation", "🏠 House Price Prediction"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### 📋 Module")
    module = st.radio(
        "module_select",
        ["📋 Data Overview", "📈 EDA", "📝 Conclusion", "🤖 Model App"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.caption("© 2026 | Data Portfolio")

# ======================
# CLEAN NAMES
# ======================
project_name = project.split(" ", 1)[1]
module_name  = module.split(" ", 1)[1]

# ======================
# HEADER
# ======================
st.markdown("""
<div class="main-header">
    <h1>📊 Data Portfolio Dashboard</h1>
    <p>Interactive Analytics & Machine Learning Projects</p>
</div>
""", unsafe_allow_html=True)

# ======================
# KPI ROW
# ======================
k1, k2, k3, k4 = st.columns(4)
for col, label, value in zip(
    [k1, k2, k3, k4],
    ["Projects", "Models", "Tech Stack", "Focus"],
    ["2", "6+", "Python", "Tabular ML"]
):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ======================
# BREADCRUMB
# ======================
st.markdown(f"""
<div class="breadcrumb">
    📍 <strong>{project_name}</strong> &rsaquo; {module_name}
</div>
""", unsafe_allow_html=True)

# ======================
# ROUTING MAP
# ======================
PROJECT_MAP = {
    "Crop Recommendation":   "projects._crop_recomendation.pages",
    "House Price Prediction": "projects._house_prediction.pages",
}

MODULE_MAP = {
    "Data Overview": "data_overview",
    "EDA":           "eda",
    "Conclusion":    "conclusion",
    "Model App":     "model_app",
}

# ======================
# DYNAMIC IMPORT & RENDER
# ======================
module_path = f"{PROJECT_MAP[project_name]}.{MODULE_MAP[module_name]}"

try:
    page = importlib.import_module(module_path)
    importlib.reload(page)
    page.render()
except ModuleNotFoundError as e:
    st.error(f"❌ Module tidak ditemukan: `{module_path}`")
    st.code(str(e))
    st.info("Pastikan semua folder memiliki file `__init__.py` (boleh kosong).")
except Exception as e:
    st.error("❌ Terjadi error saat merender halaman.")
    st.exception(e)