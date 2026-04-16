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
    page_title="Data Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# CUSTOM CSS
# ======================
st.markdown("""
<style>
/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    padding-top: 0 !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: #334155 !important; }

/* Profile card */
.profile-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.25rem 1rem;
    text-align: center;
    margin-bottom: 0.5rem;
}
.profile-avatar {
    width: 72px; height: 72px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0ea5e9, #0f766e);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; margin: 0 auto 0.75rem;
    border: 2px solid rgba(255,255,255,0.15);
}
.profile-name {
    font-size: 1rem; font-weight: 700;
    color: #f1f5f9 !important; margin-bottom: 0.25rem;
}
.profile-bio {
    font-size: 0.75rem; color: #94a3b8 !important;
    line-height: 1.4; margin-bottom: 0.75rem;
}
.profile-links { display: flex; gap: 0.5rem; justify-content: center; }
.profile-link {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 6px; padding: 0.3rem 0.6rem;
    font-size: 0.7rem; color: #94a3b8 !important;
    text-decoration: none !important;
}
.profile-link:hover { background: rgba(255,255,255,0.15); }

/* Skill chips */
.skills-wrap {
    display: flex; flex-wrap: wrap; gap: 0.35rem;
    justify-content: center; margin-top: 0.6rem;
}
.skill-chip {
    background: rgba(14,165,233,0.15);
    border: 1px solid rgba(14,165,233,0.3);
    border-radius: 999px; padding: 0.2rem 0.55rem;
    font-size: 0.65rem; color: #7dd3fc !important;
}

/* Project nav buttons */
.project-nav-label {
    font-size: 0.7rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.08em;
    color: #64748b !important; margin: 0.75rem 0 0.4rem;
    padding: 0 0.25rem;
}

/* Active project button */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    text-align: left;
    color: #cbd5e1 !important;
    font-size: 0.85rem;
    transition: all 0.15s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.07);
    border-color: rgba(255,255,255,0.1);
}

/* ── Main area ── */
.page-hero {
    background: linear-gradient(135deg, #0f172a 0%, #0f766e 100%);
    border-radius: 14px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.75rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.page-hero::before {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.page-hero h1 { margin: 0 0 0.35rem; font-size: 1.75rem; font-weight: 800; }
.page-hero p  { margin: 0; opacity: 0.75; font-size: 0.9rem; }
.page-hero .badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border-radius: 999px; padding: 0.2rem 0.65rem;
    font-size: 0.72rem; margin-top: 0.75rem; margin-right: 0.35rem;
}

/* Home project cards */
.proj-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.5rem;
    height: 100%;
    transition: box-shadow 0.2s;
    cursor: pointer;
}
.proj-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.proj-card-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.proj-card-title { font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-bottom: 0.4rem; }
.proj-card-desc  { font-size: 0.82rem; color: #64748b; line-height: 1.5; }
.proj-card-tags  { margin-top: 0.75rem; display: flex; flex-wrap: wrap; gap: 0.3rem; }
.proj-tag {
    background: #f1f5f9; border-radius: 999px;
    padding: 0.15rem 0.55rem; font-size: 0.68rem; color: #475569;
}
</style>
""", unsafe_allow_html=True)

# ======================
# PROFILE DATA (ganti sesuai profil asli)
# ======================
PROFILE = {
    "name":    "Arvi Rizqi Fadhila",
    "avatar":  "public/arvi.jpg",  # Bisa ganti dengan emoji atau inisial kalau mau
    "bio":     """  I'am Arvi - a fresh Informatics graduate from Universitas AMIKOM with a strong focus on
                    machine learning and computer vision.I'am just train models in notebooks — I architect complete pipelines, from data
                    preprocessing and model training to deployment via Streamlit and HuggingFace.
                    My frontend skills (React, Vue, Tailwind) let me build the interfaces that make my
                    models usable — turning experiments into real products anyone can interact with. 
                """,
    "github":  "https://www.linkedin.com/in/arvi-rizqi-fadhila",
    "linkedin":"https://github.com/ArviRizqi",
    "skills":  ["Python", "Pandas", "Scikit-learn", "Streamlit", "Plotly", "SQL", "Random Forest", "XGBoost"],
}

# ======================
# PROJECT REGISTRY
# ======================
PROJECTS = {
    "crop-recommendation": {
        "label":   "🌾 Crop Recommendation",
        "title":   "Crop Recommendation",
        "icon":    "🌾",
        "desc":    "Klasifikasi 22 jenis tanaman berdasarkan kondisi tanah & iklim "
                   "menggunakan Random Forest Pipeline.",
        "tags":    ["Classification", "Random Forest", "22 Classes", "2200 rows"],
        "module":  "projects._crop_recomendation.pages",
        "color":   "#0f766e",
    },
    "house-price-prediction": {
        "label":   "🏠 House Price Prediction",
        "title":   "House Price Prediction",
        "icon":    "🏠",
        "desc":    "Prediksi harga rumah King County WA menggunakan Gradient Boosting "
                   "dengan 7 fitur hasil feature engineering.",
        "tags":    ["Regression", "Gradient Boosting", "King County WA", "21K rows"],
        "module":  "projects._house_prediction.pages",
        "color":   "#1e3a5f",
    },
}

MODULE_MAP = {
    "Data Overview": "data_overview",
    "EDA":           "eda",
    "Conclusion":    "conclusion",
    "Model App":     "model_app",
}

TAB_ICONS = {
    "Data Overview": "📋",
    "EDA":           "📈",
    "Conclusion":    "📝",
    "Model App":     "🤖",
}

# ======================
# QUERY PARAMS — routing
# ======================
params  = st.query_params
current = params.get("project", "home")

# Validasi — kalau project tidak dikenal, fallback ke home
if current not in PROJECTS and current != "home":
    current = "home"

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    # ── Profile card ────────────────────────────────────────────────────
    skills_html = "".join(f'<span class="skill-chip">{s}</span>' for s in PROFILE["skills"])
    st.markdown(f"""
    <div class="profile-card">
        <div class="profile-avatar">{PROFILE['avatar']}</div>
        <div class="profile-name">{PROFILE['name']}</div>
        <div class="profile-bio">{PROFILE['bio']}</div>
        <div class="profile-links">
            <a class="profile-link" href="{PROFILE['github']}"  target="_blank">⌥ GitHub</a>
            <a class="profile-link" href="{PROFILE['linkedin']}" target="_blank">in LinkedIn</a>
        </div>
        <div class="skills-wrap">{skills_html}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Home button ──────────────────────────────────────────────────────
    if st.button("🏠  Home", key="nav_home"):
        st.query_params["project"] = "home"
        st.rerun()

    # ── Project navigation ────────────────────────────────────────────────
    st.markdown('<div class="project-nav-label">📂 Projects</div>', unsafe_allow_html=True)

    for slug, proj in PROJECTS.items():
        is_active = (current == slug)
        btn_label = f"{'▶ ' if is_active else '   '}{proj['label']}"
        if st.button(btn_label, key=f"nav_{slug}"):
            st.query_params["project"] = slug
            st.rerun()

    st.markdown("---")
    st.caption("© 2026 | Data Portfolio")


# ======================
# MAIN CONTENT
# ======================

# ── HOME PAGE ────────────────────────────────────────────────────────────
if current == "home":
    st.markdown(f"""
    <div class="page-hero">
        <h1>📊 Data Portfolio Dashboard</h1>
        <p>Interactive Analytics & Machine Learning Projects</p>
        <span class="badge">Python</span>
        <span class="badge">Machine Learning</span>
        <span class="badge">Tabular Data</span>
        <span class="badge">Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    for col, label, value in zip(
        [k1, k2, k3, k4],
        ["Total Projects", "Models Built", "Tech Stack", "Focus"],
        [len(PROJECTS), "6+", "Python", "Tabular ML"]
    ):
        col.metric(label, value)

    st.markdown("---")
    st.markdown("### 🚀 Projects")

    cols = st.columns(len(PROJECTS))
    for col, (slug, proj) in zip(cols, PROJECTS.items()):
        with col:
            tags_html = "".join(f'<span class="proj-tag">{t}</span>' for t in proj["tags"])
            st.markdown(f"""
            <div class="proj-card">
                <div class="proj-card-icon">{proj['icon']}</div>
                <div class="proj-card-title">{proj['title']}</div>
                <div class="proj-card-desc">{proj['desc']}</div>
                <div class="proj-card-tags">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"Buka {proj['title']} →", key=f"open_{slug}", use_container_width=True):
                st.query_params["project"] = slug
                st.rerun()


# ── PROJECT PAGE ──────────────────────────────────────────────────────────
else:
    proj = PROJECTS[current]

    # Hero
    st.markdown(f"""
    <div class="page-hero" style="background: linear-gradient(135deg, #0f172a 0%, {proj['color']} 100%);">
        <h1>{proj['icon']} {proj['title']}</h1>
        <p>{proj['desc']}</p>
        {"".join(f'<span class="badge">{t}</span>' for t in proj['tags'])}
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────
    tab_labels = [f"{TAB_ICONS[m]} {m}" for m in MODULE_MAP.keys()]
    tabs = st.tabs(tab_labels)

    for tab, (module_name, module_file) in zip(tabs, MODULE_MAP.items()):
        with tab:
            module_path = f"{proj['module']}.{module_file}"
            try:
                page = importlib.import_module(module_path)
                importlib.reload(page)
                page.render()
            except ModuleNotFoundError as e:
                st.error(f"❌ Module tidak ditemukan: `{module_path}`")
                st.code(str(e))
            except Exception as e:
                st.error(f"❌ Error di tab **{module_name}**")
                st.exception(e)