# theme.py
# ════════════════════════════════════════════════════════════
#  EDIT FILE INI untuk mengubah tampilan dashboard
#  Semua warna, ukuran, font, dan spacing ada di sini.
#  Tidak perlu menyentuh app.py sama sekali.
# ════════════════════════════════════════════════════════════


# ── WARNA UTAMA ───────────────────────────────────────────────
# Ganti nilai hex di sini untuk mengubah palet warna dashboard
COLOR = {
    # Sidebar
    "sidebar_bg_top":    "#0f172a",   # warna atas sidebar
    "sidebar_bg_bottom": "#1e293b",   # warna bawah sidebar
    "sidebar_border":    "#334155",   # garis pemisah di sidebar
    "sidebar_text":      "#e2e8f0",   # teks di sidebar
    "sidebar_text_muted":"#94a3b8",   # teks redup (bio, caption)
    "sidebar_hover":     "rgba(255,255,255,0.07)",  # hover tombol

    # Profile card
    "avatar_gradient_a": "#0ea5e9",   # warna kiri avatar default
    "avatar_gradient_b": "#0f766e",   # warna kanan avatar default
    "skill_chip_bg":     "rgba(14,165,233,0.15)",
    "skill_chip_border": "rgba(14,165,233,0.3)",
    "skill_chip_text":   "#7dd3fc",

    # Hero banner (halaman home)
    "hero_bg_left":      "#0f172a",   # kiri gradient hero
    "hero_bg_right":     "#0f766e",   # kanan gradient hero

    # Card project (halaman home)
    "card_bg":           "#f8fafc",
    "card_border":       "#e2e8f0",
    "card_title":        "#0f172a",
    "card_desc":         "#64748b",
    "card_tag_bg":       "#f1f5f9",
    "card_tag_text":     "#475569",

    # Meta chip (halaman project)
    "meta_chip_bg":      "#f1f5f9",
    "meta_chip_border":  "#e2e8f0",
    "meta_chip_text":    "#475569",
    "meta_chip_label":   "#0f172a",
}


# ── TIPOGRAFI ────────────────────────────────────────────────
# Ganti nama font sesuai Google Fonts atau font sistem
FONT = {
    "family":       "Inter, system-ui, sans-serif",   # font utama seluruh dashboard
    "size_base":    "0.875rem",   # ukuran teks normal
    "size_sm":      "0.75rem",    # teks kecil (caption, label)
    "size_xs":      "0.65rem",    # teks sangat kecil (chip, tag)
    "size_hero_h1": "1.75rem",    # judul hero banner
    "size_nav":     "0.85rem",    # tombol navigasi sidebar
    "weight_bold":  "700",
    "weight_semi":  "600",
}


# ── SPACING & SHAPE ───────────────────────────────────────────
SHAPE = {
    "radius_card":   "12px",    # border-radius kartu project
    "radius_chip":   "999px",   # border-radius chip/tag (pill)
    "radius_btn":    "8px",     # border-radius tombol
    "radius_hero":   "14px",    # border-radius hero banner
    "radius_avatar": "50%",     # bentuk avatar (50% = bulat)

    "avatar_size":   "72px",    # ukuran avatar profil
    "padding_card":  "1.5rem",  # padding dalam kartu project
    "padding_hero":  "2rem 2.5rem",  # padding hero banner
    "padding_btn":   "0.45rem 0.75rem",  # padding tombol sidebar
}


# ── GENERATE CSS ─────────────────────────────────────────────
# Fungsi ini membuat string CSS dari variabel di atas.
# Tidak perlu diedit kecuali ingin menambah komponen baru.
def get_css() -> str:
    c = COLOR
    f = FONT
    s = SHAPE
    return f"""
<style>
/* ══ FONT ══════════════════════════════════════════════════ */
html, body, [class*="css"] {{
    font-family: {f['family']};
}}

/* ══ SIDEBAR ════════════════════════════════════════════════ */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {c['sidebar_bg_top']} 0%,
                                        {c['sidebar_bg_bottom']} 100%);
    padding-top: 0 !important;
}}
[data-testid="stSidebar"] * {{ color: {c['sidebar_text']} !important; }}
[data-testid="stSidebar"] hr {{ border-color: {c['sidebar_border']} !important; }}

/* ── Profile card ── */
.profile-card {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: {s['radius_card']};
    padding: 1.25rem 1rem;
    text-align: center;
    margin-bottom: 0.5rem;
}}
.profile-avatar {{
    width: {s['avatar_size']}; height: {s['avatar_size']};
    border-radius: {s['radius_avatar']};
    background: linear-gradient(135deg, {c['avatar_gradient_a']},
                                        {c['avatar_gradient_b']});
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; margin: 0 auto 0.75rem;
    border: 2px solid rgba(255,255,255,0.15);
}}
.profile-avatar img {{
    width: {s['avatar_size']}; height: {s['avatar_size']};
    border-radius: {s['radius_avatar']}; object-fit: cover;
}}
.profile-name {{
    font-size: {f['size_base']}; font-weight: {f['weight_bold']};
    color: #f1f5f9 !important; margin-bottom: 0.25rem;
}}
.profile-bio {{
    font-size: {f['size_sm']}; color: {c['sidebar_text_muted']} !important;
    line-height: 1.4; margin-bottom: 0.75rem;
}}
.profile-links {{ display: flex; gap: 0.5rem; justify-content: center; }}
.profile-link {{
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12);
    border-radius: 6px; padding: 0.3rem 0.6rem;
    font-size: {f['size_xs']}; color: {c['sidebar_text_muted']} !important;
    text-decoration: none !important;
}}

/* ── Skill chips ── */
.skills-wrap {{
    display: flex; flex-wrap: wrap; gap: 0.35rem;
    justify-content: center; margin-top: 0.6rem;
}}
.skill-chip {{
    background: {c['skill_chip_bg']}; border: 1px solid {c['skill_chip_border']};
    border-radius: {s['radius_chip']}; padding: 0.2rem 0.55rem;
    font-size: {f['size_xs']}; color: {c['skill_chip_text']} !important;
}}

/* ── Nav label ── */
.project-nav-label {{
    font-size: {f['size_xs']}; font-weight: {f['weight_semi']};
    text-transform: uppercase; letter-spacing: 0.08em;
    color: #64748b !important;
    margin: 0.75rem 0 0.4rem; padding: 0 0.25rem;
}}

/* ── Sidebar buttons ── */
[data-testid="stSidebar"] .stButton {{
    margin: 0 !important; padding: 0 !important;
}}
[data-testid="stSidebar"] .stButton > button {{
    width: 100%; background: transparent;
    border: none !important; border-radius: {s['radius_btn']};
    padding: {s['padding_btn']} !important; margin: 0 !important;
    text-align: left; color: {c['sidebar_text']} !important;
    font-size: {f['size_nav']}; transition: background 0.15s; line-height: 1.4;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: {c['sidebar_hover']} !important;
    border: none !important;
}}
[data-testid="stSidebar"] .stButton > button:focus {{
    box-shadow: none !important; border: none !important;
}}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {{
    gap: 0 !important;
}}

/* ══ HERO BANNER ════════════════════════════════════════════ */
.page-hero {{
    border-radius: {s['radius_hero']}; padding: {s['padding_hero']};
    margin-bottom: 1.75rem; color: white;
    position: relative; overflow: hidden;
}}
.page-hero::before {{
    content: ''; position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.04); border-radius: 50%;
}}
.page-hero h1 {{
    margin: 0 0 0.35rem; font-size: {f['size_hero_h1']};
    font-weight: {f['weight_bold']};
}}
.page-hero p {{ margin: 0; opacity: 0.75; font-size: {f['size_sm']}; }}
.page-hero .badge {{
    display: inline-block; background: rgba(255,255,255,0.12);
    border-radius: {s['radius_chip']}; padding: 0.2rem 0.65rem;
    font-size: {f['size_xs']}; margin-top: 0.75rem; margin-right: 0.35rem;
}}

/* ══ META CHIPS (halaman project) ═══════════════════════════ */
.meta-row {{ display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 1.25rem; }}
.meta-chip {{
    background: {c['meta_chip_bg']}; border: 1px solid {c['meta_chip_border']};
    border-radius: {s['radius_btn']}; padding: 0.3rem 0.75rem;
    font-size: {f['size_sm']}; color: {c['meta_chip_text']};
}}
.meta-chip strong {{ color: {c['meta_chip_label']}; }}

/* ══ PROJECT CARDS (halaman home) ═══════════════════════════ */
.proj-card {{
    background: {c['card_bg']}; border: 1px solid {c['card_border']};
    border-radius: {s['radius_card']}; padding: {s['padding_card']}; height: 100%;
}}
.proj-card-icon  {{ font-size: 2.5rem; margin-bottom: 0.75rem; }}
.proj-card-title {{
    font-size: 1.05rem; font-weight: {f['weight_bold']};
    color: {c['card_title']}; margin-bottom: 0.4rem;
}}
.proj-card-desc  {{ font-size: {f['size_sm']}; color: {c['card_desc']}; line-height: 1.5; }}
.proj-card-tags  {{ margin-top: 0.75rem; display: flex; flex-wrap: wrap; gap: 0.3rem; }}
.proj-tag {{
    background: {c['card_tag_bg']}; border-radius: {s['radius_chip']};
    padding: 0.15rem 0.55rem; font-size: {f['size_xs']}; color: {c['card_tag_text']};
}}
</style>
"""