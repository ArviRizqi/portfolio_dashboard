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
# LOAD CONFIG
# ======================
import config as _cfg
importlib.reload(_cfg)
PROFILE   = _cfg.PROFILE
PROJECTS  = _cfg.PROJECTS
TABS      = _cfg.TABS
DASHBOARD = _cfg.DASHBOARD

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title=DASHBOARD["title"],
    page_icon=DASHBOARD["icon"],
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

.profile-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.25rem 1rem;
    text-align: center;
    margin-bottom: 0.5rem;
}
.profile-avatar {
    width: 72px; height: 72px; border-radius: 50%;
    background: linear-gradient(135deg, #0ea5e9, #0f766e);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; margin: 0 auto 0.75rem;
    border: 2px solid rgba(255,255,255,0.15);
}
.profile-avatar img {
    width: 72px; height: 72px; border-radius: 50%;
    object-fit: cover;
}
.profile-name  { font-size: 1rem; font-weight: 700; color: #f1f5f9 !important; margin-bottom: 0.25rem; }
.profile-bio   { font-size: 0.75rem; color: #94a3b8 !important; line-height: 1.4; margin-bottom: 0.75rem; }
.profile-links { display: flex; gap: 0.5rem; justify-content: center; }
.profile-link  {
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12);
    border-radius: 6px; padding: 0.3rem 0.6rem;
    font-size: 0.7rem; color: #94a3b8 !important; text-decoration: none !important;
}
.skills-wrap { display: flex; flex-wrap: wrap; gap: 0.35rem; justify-content: center; margin-top: 0.6rem; }
.skill-chip  {
    background: rgba(14,165,233,0.15); border: 1px solid rgba(14,165,233,0.3);
    border-radius: 999px; padding: 0.2rem 0.55rem;
    font-size: 0.65rem; color: #7dd3fc !important;
}
.project-nav-label {
    font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.08em; color: #64748b !important;
    margin: 0.75rem 0 0.4rem; padding: 0 0.25rem;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%; background: transparent; border: 1px solid transparent;
    border-radius: 8px; padding: 0.5rem 0.75rem; text-align: left;
    color: #cbd5e1 !important; font-size: 0.85rem; transition: all 0.15s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.07); border-color: rgba(255,255,255,0.1);
}

/* ── Main area ── */
.page-hero {
    border-radius: 14px; padding: 2rem 2.5rem;
    margin-bottom: 1.75rem; color: white;
    position: relative; overflow: hidden;
}
.page-hero::before {
    content: ''; position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.04); border-radius: 50%;
}
.page-hero h1 { margin: 0 0 0.35rem; font-size: 1.75rem; font-weight: 800; }
.page-hero p  { margin: 0; opacity: 0.75; font-size: 0.9rem; }
.page-hero .badge {
    display: inline-block; background: rgba(255,255,255,0.12);
    border-radius: 999px; padding: 0.2rem 0.65rem;
    font-size: 0.72rem; margin-top: 0.75rem; margin-right: 0.35rem;
}

/* Project meta chips */
.meta-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 1.25rem; }
.meta-chip {
    background: #f1f5f9; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 0.3rem 0.75rem;
    font-size: 0.78rem; color: #475569;
}
.meta-chip strong { color: #0f172a; }

/* Home project cards */
.proj-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 1.5rem; height: 100%;
}
.proj-card-icon  { font-size: 2.5rem; margin-bottom: 0.75rem; }
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
# HELPERS
# ======================
def render_profile():
    # Avatar — foto atau emoji
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
        links_html += f'<a class="profile-link" href="{PROFILE["github"]}" target="_blank">⌥ GitHub</a>'
    if PROFILE.get("linkedin"):
        links_html += f'<a class="profile-link" href="{PROFILE["linkedin"]}" target="_blank">in LinkedIn</a>'

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
    """Tampilkan chip meta info project di bawah hero."""
    chips = {
        "📁 Dataset":    proj.get("dataset", "-"),
        "🤖 Algorithm":  proj.get("algorithm", "-"),
        "🎯 Task":       proj.get("task", "-"),
        "📊 Score":      proj.get("accuracy", "-"),
    }
    chips_html = "".join(
        f'<div class="meta-chip"><strong>{k}</strong>&nbsp;&nbsp;{v}</div>'
        for k, v in chips.items()
    )
    st.markdown(f'<div class="meta-row">{chips_html}</div>', unsafe_allow_html=True)


# ======================
# QUERY PARAMS — routing
# ======================
params  = st.query_params
current = params.get("project", "home")
if current not in PROJECTS and current != "home":
    current = "home"

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    render_profile()
    st.markdown("---")

    if st.button("🏠  Home", key="nav_home"):
        st.query_params["project"] = "home"
        st.rerun()

    st.markdown(
        f'<div class="project-nav-label">📂 Projects</div>',
        unsafe_allow_html=True
    )
    for slug, proj in PROJECTS.items():
        is_active = (current == slug)
        label     = f"{'▶  ' if is_active else '    '}{proj['label']}"
        if st.button(label, key=f"nav_{slug}"):
            st.query_params["project"] = slug
            st.rerun()

    st.markdown("---")
    st.caption(DASHBOARD["footer"])


# ======================
# HOME PAGE
# ======================
if current == "home":
    badges_html = "".join(
        f'<span class="badge">{b}</span>'
        for b in DASHBOARD.get("badges", [])
    )
    st.markdown(f"""
    <div class="page-hero" style="background: linear-gradient(135deg, #0f172a 0%, #0f766e 100%);">
        <h1>{DASHBOARD['icon']} {DASHBOARD['title']}</h1>
        <p>{DASHBOARD['subtitle']}</p>
        {badges_html}
    </div>
    """, unsafe_allow_html=True)

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
            if st.button(f"Buka {proj['title']} →", key=f"open_{slug}",
                         use_container_width=True):
                st.query_params["project"] = slug
                st.rerun()


# ======================
# PROJECT PAGE
# ======================
else:
    proj = PROJECTS[current]

    badges_html = "".join(
        f'<span class="badge">{t}</span>'
        for t in proj.get("tags", [])
    )
    st.markdown(f"""
    <div class="page-hero"
         style="background: linear-gradient(135deg, #0f172a 0%, {proj['color']} 100%);">
        <h1>{proj['icon']} {proj['title']}</h1>
        <p>{proj['desc']}</p>
        {badges_html}
    </div>
    """, unsafe_allow_html=True)

    render_project_meta(proj)

    # ── Tabs ──────────────────────────────────────────────────────────
    tab_labels = [f"{cfg['icon']} {name}" for name, cfg in TABS.items()]
    tabs       = st.tabs(tab_labels)

    for tab, (tab_name, tab_cfg) in zip(tabs, TABS.items()):
        with tab:
            module_path = f"{proj['module']}.{tab_cfg['file']}"
            try:
                page = importlib.import_module(module_path)
                importlib.reload(page)
                page.render()
            except ModuleNotFoundError as e:
                st.error(f"❌ Module tidak ditemukan: `{module_path}`")
                st.code(str(e))
            except Exception as e:
                st.error(f"❌ Error di tab **{tab_name}**")
                st.exception(e)