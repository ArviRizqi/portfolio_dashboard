# projects/_depression_detection/pages/model_app.py

import streamlit as st
import pandas as pd
import numpy as np
import os, sys, warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
from shared.utils import section_header

BASE       = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE, "../models/depression_model.h5")
PREP_PATH  = os.path.join(BASE, "../models/preprocessor.pkl")

DEPRESSION_LABEL = {
    0: ("Very Low",  "😊", "#22c55e"),
    1: ("Low",       "🙂", "#84cc16"),
    2: ("Moderate",  "😐", "#f59e0b"),
    3: ("High",      "😟", "#f97316"),
    4: ("Very High", "😞", "#ef4444"),
}

# Pilihan dropdown — persis dari app.py Gradio
GENDER_CHOICES       = ['Male', 'Female', 'other']
RELATIONSHIP_CHOICES = ["in a relationship", "Married", "Single", "Disvorced"]
OCCUPATION_CHOICES   = ["University Student", "Retired", "Salaries Worker", "School Student"]
AFFILIATE_CHOICES    = ["Company", "Goverment", "Private", "School", "University", "None"]
SOSMED_CHOICES       = ['Reddit', 'Pinterest', 'Facebook', 'Twitter',
                         'Snapchat', 'YouTube', 'Discord', 'TikTok', 'Instagram']
AVG_TIME_CHOICES     = [
    "Less than one hour", "Beetwen 1 and 2 hour", "Beetwen 2 and 3 hour",
    "Beetwen 3 and 4 hour", "Beetwen 4 and 5 hour", "More than 5 hour",
]


@st.cache_resource
def load_pipeline():
    import joblib
    import tensorflow as tf
    model       = tf.keras.models.load_model(MODEL_PATH)
    preprocessor = joblib.load(PREP_PATH)
    return model, preprocessor


def classify_prediction(pred_idx: int) -> tuple:
    return DEPRESSION_LABEL.get(pred_idx, ("Unknown", "❓", "#94a3b8"))


def render():
    section_header("🧠 Depression Detection — Model App",
                   "Isi kuesioner di bawah untuk mendapatkan estimasi tingkat depresi "
                   "berdasarkan pola penggunaan media sosial Anda.")

    model_ready = os.path.exists(MODEL_PATH) and os.path.exists(PREP_PATH)

    if not model_ready:
        st.warning("""
        ⚠️ **File model belum ditemukan.**
        Letakkan file berikut di `projects/_depression_detection/models/`:
        - `depression_model.h5`
        - `preprocessor.pkl`
        """)
        st.info("Form preview tersedia di bawah. Prediksi aktif setelah model diunggah.")
        st.markdown("---")

    # ═══════════════════════════════════════════════════
    # SECTION 1 — Informasi Pribadi (tidak dipakai model)
    # ═══════════════════════════════════════════════════
    st.markdown("#### 👤 Informasi Pribadi")
    st.caption("Informasi ini hanya untuk personalisasi hasil — tidak digunakan model.")

    c1, c2, c3 = st.columns(3)
    with c1:
        name   = st.text_input("Nama", value="Anonymous", key="dep_name")
    with c2:
        age    = st.number_input("Usia", min_value=10, max_value=100, value=21, key="dep_age")
    with c3:
        gender = st.selectbox("Gender", GENDER_CHOICES, key="dep_gender")

    c4, c5, c6 = st.columns(3)
    with c4:
        relationship = st.selectbox("Status Hubungan", RELATIONSHIP_CHOICES, key="dep_rel")
    with c5:
        occupation   = st.selectbox("Pekerjaan", OCCUPATION_CHOICES, key="dep_occ")
    with c6:
        affiliate    = st.multiselect("Affiliasi Organisasi", AFFILIATE_CHOICES,
                                      default=["None"], key="dep_aff")

    sosmed_used = st.multiselect("Platform Media Sosial yang Digunakan",
                                 SOSMED_CHOICES, default=["Instagram", "YouTube"],
                                 key="dep_sosmed")

    avg_time = st.selectbox("Rata-rata Waktu Penggunaan Sosmed per Hari",
                            AVG_TIME_CHOICES, index=2, key="dep_time")

    st.markdown("---")

    # ═══════════════════════════════════════════════════
    # SECTION 2 — Kuesioner (INPUT MODEL)
    # ═══════════════════════════════════════════════════
    st.markdown("#### 🎛️ Kuesioner Perilaku & Perasaan")
    st.caption("Nilai **1 = Tidak sama sekali**, **5 = Sangat sering/parah**")

    questions = {
        "without_purpose":    "Seberapa sering kamu menggunakan media sosial tanpa tujuan tertentu?",
        "distracted":         "Seberapa sering kamu terdistraksi media sosial saat sedang sibuk?",
        "restless":           "Apakah kamu merasa gelisah jika belum membuka media sosial?",
        "distracted_ease":    "Seberapa mudah kamu teralihkan perhatiannya?",
        "worries":            "Seberapa sering kamu diganggu oleh rasa khawatir?",
        "concentration":      "Apakah kamu merasa sulit berkonsentrasi?",
        "compare_to_others":  "Seberapa sering kamu membandingkan diri dengan orang lain di media sosial?",
        "validation":         "Seberapa sering kamu mencari validasi dari media sosial?",
        "daily_activity_flux":"Seberapa sering minat kamu terhadap aktivitas harian berfluktuasi?",
        "sleeping_issues":    "Seberapa sering kamu mengalami masalah tidur?",
    }

    inputs = {}
    cols_q = st.columns(2)
    for i, (key, question) in enumerate(questions.items()):
        with cols_q[i % 2]:
            inputs[key] = st.slider(
                label=question,
                min_value=1, max_value=5, value=3,
                key=f"dep_{key}"
            )

    st.markdown("---")

    # ── Tombol prediksi ───────────────────────────────────────────────────
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        predict_btn = st.button("🔍 Deteksi Level Depresi",
                                use_container_width=True, type="primary",
                                disabled=not model_ready)

    if predict_btn and model_ready:
        try:
            model, preprocessor = load_pipeline()

            # Buat DataFrame persis seperti pipeline Gradio
            input_df = pd.DataFrame({
                'relationship':         [relationship],
                'occupation':           [occupation],
                'affiliate_organization': [", ".join(affiliate)],
                'avg_time_per_day':     [avg_time],
                'without_purpose':      [inputs['without_purpose']],
                'distracted':           [inputs['distracted']],
                'restless':             [inputs['restless']],
                'distracted_ease':      [inputs['distracted_ease']],
                'worries':              [inputs['worries']],
                'concentration':        [inputs['concentration']],
                'compare_to_others':    [inputs['compare_to_others']],
                'validation':           [inputs['validation']],
                'daily_activity_flux':  [inputs['daily_activity_flux']],
                'sleeping_issues':      [inputs['sleeping_issues']],
            })

            processed = preprocessor.transform(input_df)
            probs     = model.predict(processed)
            pred_idx  = int(np.argmax(probs, axis=1)[0])

            label, emoji, color = classify_prediction(pred_idx)

            # ── Hasil utama ───────────────────────────────────────────────
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #0f172a, {color});
                border-radius: 14px; padding: 2rem;
                text-align: center; color: white;
                margin-bottom: 1.5rem;
            ">
                <div style="font-size:3.5rem;">{emoji}</div>
                <div style="font-size:0.9rem; opacity:0.75; margin-top:0.5rem;">
                    Hasil untuk <strong>{name}</strong> · {age} tahun · {gender}
                </div>
                <div style="font-size:0.85rem; opacity:0.65;">
                    Sosmed: {", ".join(sosmed_used) if sosmed_used else "-"} · {avg_time}
                </div>
                <div style="font-size:1rem; opacity:0.8; margin-top:1rem;">
                    Estimasi Level Depresi
                </div>
                <div style="font-size:2.75rem; font-weight:800;">
                    {label}
                </div>
                <div style="font-size:1rem; opacity:0.8;">
                    Level {pred_idx + 1} dari 5
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Probabilitas semua kelas ──────────────────────────────────
            st.markdown("##### 📊 Probabilitas per Level")
            labels_all = ["Very Low", "Low", "Moderate", "High", "Very High"]
            colors_all = ["#22c55e", "#84cc16", "#f59e0b", "#f97316", "#ef4444"]

            for i, (lbl, prob, col) in enumerate(zip(labels_all, probs[0], colors_all)):
                pct = float(prob) * 100
                active = "⭐ " if i == pred_idx else ""
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.5rem;">
                    <div style="width:110px; font-size:0.85rem;">
                        {active}<strong>{lbl}</strong>
                    </div>
                    <div style="flex:1; background:#e2e8f0; border-radius:999px; height:10px;">
                        <div style="width:{pct:.1f}%; background:{col};
                                    border-radius:999px; height:10px;"></div>
                    </div>
                    <div style="width:50px; font-size:0.82rem; text-align:right;">
                        {pct:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── Disclaimer ────────────────────────────────────────────────
            st.markdown("<br>", unsafe_allow_html=True)
            st.warning("""
            ⚠️ **Disclaimer:** Hasil ini bukan diagnosis medis. Model ini dibuat untuk 
            tujuan akademis dan eksplorasi data. Jika kamu merasa mengalami gejala depresi, 
            segera konsultasikan dengan profesional kesehatan mental.
            """)

            # ── Detail input ──────────────────────────────────────────────
            with st.expander("📋 Detail input yang digunakan model"):
                q_labels = {
                    'relationship': 'Status Hubungan',
                    'occupation': 'Pekerjaan',
                    'affiliate_organization': 'Affiliasi',
                    'avg_time_per_day': 'Waktu Sosmed/hari',
                    **{k: v[:50] for k, v in questions.items()}
                }
                detail_df = pd.DataFrame({
                    'Pertanyaan': list(q_labels.values()),
                    'Jawaban': [
                        relationship, occupation, ", ".join(affiliate), avg_time,
                        *[inputs[k] for k in questions.keys()]
                    ]
                })
                st.dataframe(detail_df, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"❌ Error saat prediksi: {e}")
            st.exception(e)