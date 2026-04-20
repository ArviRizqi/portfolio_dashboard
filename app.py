"""
app.py — Entry point & router utama
════════════════════════════════════
File ini HANYA berisi logika routing dan rendering.

Untuk mengubah tampilan  → edit theme.py
Untuk mengubah konten    → edit config.py
Untuk menambah project   → tambah entry di config.py + buat folder pages/
"""

import streamlit as st
import sys
import os
import importlib

# ── Path fix ─────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Load config (reload agar perubahan langsung terdeteksi) ──────────────────
import app_config as _cfg
importlib.reload(_cfg)
PROFILE   = _cfg.PROFILE
PROJECTS  = _cfg.PROJECTS
TABS      = _cfg.TABS
DASHBOARD = _cfg.DASHBOARD

# ── Load theme ────────────────────────────────────────────────────────────────
import theme as _theme
importlib.reload(_theme)
COLOR = _theme.COLOR
FONT  = _theme.FONT
SHAPE = _theme.SHAPE

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=DASHBOARD["title"],
    page_icon=DASHBOARD["icon"],
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Inject CSS dari theme.py ──────────────────────────────────────────────────
st.markdown(_theme.get_css(), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def render_profile():
    """Render profile card di sidebar."""
    photo_path = PROFILE.get("photo", "")
    if photo_path and os.path.exists(os.path.join(ROOT, photo_path)):
        avatar_html = f'<img src="{photo_path}" alt="foto profil">'
    else:
        avatar_html = PROFILE.get("avatar", "👤")

    skills_html = "".join(
        f'<span class="skill-chip">{s}</span>'
        for s in PROFILE.get("skills", [])
    )
    links_html = ""
    if PROFILE.get("github"):
        links_html += (
            f'<a class="profile-link" href="{PROFILE["github"]}"'
            f' target="_blank">⌥ GitHub</a>'
        )
    if PROFILE.get("linkedin"):
        links_html += (
            f'<a class="profile-link" href="{PROFILE["linkedin"]}"'
            f' target="_blank">in LinkedIn</a>'
        )

    st.markdown(f"""
    <div class="profile-card">
        <div class="profile-avatar">{avatar_html}</div>
        <div class="profile-name">{PROFILE.get("name", "")}</div>
        <div class="profile-bio">{PROFILE.get("bio", "")}</div>
        <div class="profile-links">{links_html}</div>
        <div class="skills-wrap">{skills_html}</div>
    </div>
    """, unsafe_allow_html=True)


def render_project_meta(proj: dict):
    """Render chip metadata di bawah hero setiap project."""
    chips = {
        "📁 Dataset":   proj.get("dataset",   "-"),
        "🤖 Algorithm": proj.get("algorithm", "-"),
        "🎯 Task":      proj.get("task",      "-"),
        "📊 Score":     proj.get("accuracy",  "-"),
    }
    chips_html = "".join(
        f'<div class="meta-chip"><strong>{k}</strong>&nbsp;&nbsp;{v}</div>'
        for k, v in chips.items()
    )
    st.markdown(f'<div class="meta-row">{chips_html}</div>', unsafe_allow_html=True)


def render_page(module_path: str, tab_name: str):
    """Import & render satu halaman page dengan error handling."""
    try:
        if module_path in sys.modules:
            del sys.modules[module_path]
        page = importlib.import_module(module_path)
        page.render()
    except ModuleNotFoundError as e:
        missing = str(e)
        st.error(f"❌ Module tidak ditemukan: `{module_path}`")
        st.code(missing)
        if "No module named" in missing:
            pkg = missing.split("'")[1] if "'" in missing else missing
            st.warning(f"💡 Pastikan `{pkg}` ada di `requirements.txt`.")
    except ImportError as e:
        st.error("❌ Import error — library belum terinstall.")
        st.code(str(e))
        st.warning("💡 Cek `requirements.txt` dan deploy ulang.")
    except Exception as e:
        st.error(f"❌ Error di tab **{tab_name}**: {type(e).__name__}")
        st.exception(e)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTING — baca project aktif dari URL query param
# ══════════════════════════════════════════════════════════════════════════════
current = st.query_params.get("project", "home")
if current not in PROJECTS and current != "home":
    current = "home"


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    render_profile()
    st.markdown("---")

    # Tombol Home
    if st.button("🏠  Home", key="nav_home", use_container_width=True):
        st.query_params["project"] = "home"
        st.rerun()

    # Label section Projects
    st.markdown('<div class="project-nav-label">📂 Projects</div>',
                unsafe_allow_html=True)

    # Satu tombol per project — ▶ hanya untuk yang aktif
    for slug, proj in PROJECTS.items():
        prefix = "▶" if current == slug else " "
        label  = f"{prefix}  {proj['label']}"
        if st.button(label, key=f"nav_{slug}", use_container_width=True):
            st.query_params["project"] = slug
            st.rerun()

    st.markdown("---")
    st.caption(DASHBOARD["footer"])


# ══════════════════════════════════════════════════════════════════════════════
# HALAMAN HOME
# ══════════════════════════════════════════════════════════════════════════════
if current == "home":
    # Hero banner
    badges_html = "".join(
        f'<span class="badge">{b}</span>'
        for b in DASHBOARD.get("badges", [])
    )
    st.markdown(f"""
    <div class="page-hero"
         style="background: linear-gradient(135deg,
                {COLOR['hero_bg_left']} 0%,
                {COLOR['hero_bg_right']} 100%);">
        <h1>{DASHBOARD['icon']} {DASHBOARD['title']}</h1>
        <p>{DASHBOARD['subtitle']}</p>
        {badges_html}
    </div>
    """, unsafe_allow_html=True)

    # KPI metrics
    kpi_cols = st.columns(4)
    kpi_data = [
        ("Total Projects", len(PROJECTS)),
        ("Models Built",   "6+"),
        ("Tech Stack",     "Python"),
        ("Focus",          "Tabular ML"),
    ]
    for col, (label, value) in zip(kpi_cols, kpi_data):
        col.metric(label, value)

    st.markdown("---")
    st.markdown("### 🚀 Projects")

    # Project cards
    card_cols = st.columns(len(PROJECTS))
    for col, (slug, proj) in zip(card_cols, PROJECTS.items()):
        with col:
            tags_html = "".join(
                f'<span class="proj-tag">{t}</span>'
                for t in proj.get("tags", [])
            )
            st.markdown(f"""
            <div class="proj-card">
                <div class="proj-card-icon">{proj['icon']}</div>
                <div class="proj-card-title">{proj['title']}</div>
                <div class="proj-card-desc">{proj['desc']}</div>
                <div class="proj-card-tags">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"Buka {proj['title']} →",
                         key=f"open_{slug}", use_container_width=True):
                st.query_params["project"] = slug
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# HALAMAN PROJECT
# ══════════════════════════════════════════════════════════════════════════════
else:
    proj = PROJECTS[current]

    # Hero banner project
    badges_html = "".join(
        f'<span class="badge">{t}</span>'
        for t in proj.get("tags", [])
    )
    st.markdown(f"""
    <div class="page-hero"
         style="background: linear-gradient(135deg,
                {COLOR['hero_bg_left']} 0%,
                {proj['color']} 100%);">
        <h1>{proj['icon']} {proj['title']}</h1>
        <p>{proj['desc']}</p>
        {badges_html}
    </div>
    """, unsafe_allow_html=True)

    # Meta chips
    render_project_meta(proj)

    # Tabs — setiap tab render satu page module
    tab_labels = [f"{cfg['icon']} {name}" for name, cfg in TABS.items()]
    tabs       = st.tabs(tab_labels)

    for tab, (tab_name, tab_cfg) in zip(tabs, TABS.items()):
        with tab:
            module_path = f"{proj['module']}.{tab_cfg['file']}"
            render_page(module_path, tab_name)