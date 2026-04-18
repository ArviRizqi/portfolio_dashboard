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

from shared.utils import section_header

# ── Paths ────────────────────────────────────────────────────────────────────
MODEL_DIR  = CURRENT_DIR.parent / "models"
MODEL_PATH = str(MODEL_DIR / "best_model.pkl")
PREP_PATH  = str(MODEL_DIR / "preprocessor.pkl")

# Emoji per label
DEPRESSION_EMOJI = {
    "Very Low": "😇",
    "Low": "🙂",
    "Moderate": "😐",
    "High": "😟",
    "Very High": "🆘"
}

# Choices
GENDER_CHOICES = ['Male', 'Female', 'other']
REL_CHOICES    = ["in a relationship", "Married", "Single", 'Disvorced']
OCCUP_CHOICES  = ["University Student", "Retired", "Salaries Worker", 'School Student']
AFFIL_CHOICES  = ["Company", "Goverment", "Private", "School", "University", "None"]
SOSMED_CHOICES = ['Reddit', 'Pinterest', 'Facebook','Twitter', 'Snapchat', 'YouTube', 'Discord', 'TikTok', 'Instagram']
TIME_CHOICES   = ["Beetwen 1 and 2 hour", "Beetwen 2 and 3 hour", "Beetwen 3 and 4 hour", "Beetwen 4 and 5 hour", "Less than one hour", "More than 5 hour"]

@st.cache_resource
def load_pipeline():
    try:
        import joblib
        model = joblib.load(MODEL_PATH)
        preprocessor = joblib.load(PREP_PATH)
        return model, preprocessor, None
    except Exception as e:
        import traceback
        return None, None, traceback.format_exc()



def classify_prediction(prob):
    return ["Very Low", "Low", "Moderate", "High", "Very High"][prob]

def render():
    section_header("🧠 Depression Detection — Model App",
                   "Isi formulir survei singkat berikut untuk memprediksi tingkat depresi. "
                   "Aplikasi ini didukung penuh oleh algoritma XGBoost Classifier.")

    model, preprocessor, error_msg = load_pipeline()
    
    if model is None or preprocessor is None:
        st.warning("""
        Pastikan struktur model berikut tersedia di `projects/_depression_detection/models/`:
        - `best_model.pkl`
        - `preprocessor.pkl`
        
        Sistem tidak dapat memuat model karena pesan error berikut:
        """)
        st.code(error_msg, language="bash")
        
        st.info("💡 Pastikan `tensorflow` terinstall di backend environment Anda. Preview form di bawah ini. Hasil prediksi aktif saat model berhasil di-load.")
        st.markdown("---")



    st.markdown("#### 📋 Formulir Survei Sosial Media")
    
    with st.form("depression_form"):
        st.markdown("**A. Profil Singkat**")
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("Name", placeholder="Your name")
        with c2:
            age = st.text_input("Age", placeholder="e.g. 24")
        with c3:
            gender = st.selectbox("Gender", GENDER_CHOICES)
            
        c4, c5 = st.columns(2)
        with c4:
            relationship = st.selectbox("Relationship Status", REL_CHOICES)
        with c5:
            occupation = st.selectbox("Occupation", OCCUP_CHOICES)
            
        st.markdown("**B. Kebiasaan Sosial Media**")
        affiliate = st.multiselect("Affiliate Organization", AFFIL_CHOICES)
        sosmed = st.multiselect("Social Media Platforms", SOSMED_CHOICES)
        avg_time = st.selectbox("Average Time Per Day", TIME_CHOICES)

        st.markdown("**C. Psikologi & Perilaku (1 = Sangat Jarang, 5 = Sangat Sering)**")
        sc1, sc2 = st.columns(2)
        with sc1:
            without_purpose = st.slider("Using Sosmed Without Purpose", 1, 5, 3)
            distracted = st.slider("Distracted by Sosmed when busy", 1, 5, 3)
            restless = st.slider("Restless if haven't used Sosmed", 1, 5, 3)
            distracted_ease = st.slider("Ease of Distraction", 1, 5, 3)
            worries = st.slider("Bothered by Worries", 1, 5, 3)
        with sc2:
            concentration = st.slider("Difficult to Concentrate", 1, 5, 3)
            compare = st.slider("Compare to Others on Sosmed", 1, 5, 3)
            validation = st.slider("Seek Validation from Sosmed", 1, 5, 3)
            activity_flux = st.slider("Daily Activity Fluctuate", 1, 5, 3)
            sleeping = st.slider("Facing Sleeping Issues", 1, 5, 3)

        submitted = st.form_submit_button("Analisis Tingkat Depresi", use_container_width=True, type="primary")

        if submitted:
            if not model:
                st.error("Model tidak tersedia untuk prediksi.")
            elif not name or not age:
                st.error("Nama dan umur wajib diisi.")
            else:
                input_data = pd.DataFrame({
                    'relationship': [relationship],
                    'occupation': [occupation],
                    'affiliate_organization': [", ".join(affiliate) if affiliate else "None"],
                    'avg_time_per_day': [avg_time],
                    'without_purpose': [without_purpose],
                    'distracted': [distracted],
                    'restless': [restless],
                    'distracted_ease': [distracted_ease],
                    'worries': [worries],
                    'concentration': [concentration],
                    'compare_to_others': [compare],
                    'validation': [validation],
                    'daily_activity_flux': [activity_flux],
                    'sleeping_issues': [sleeping]
                })

                with st.spinner("Processing Model..."):
                    try:
                        processed = preprocessor.transform(input_data)
                        predictions = model.predict(processed)
                        pred_index = int(predictions[0])
                        label = classify_prediction(pred_index)
                        
                        # UI Result
                        st.markdown("---")
                        emoji = DEPRESSION_EMOJI.get(label, "🧠")
                        
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #1e293b, #0f172a);
                            border: 1px solid rgba(255,255,255,0.1);
                            border-radius: 14px;
                            padding: 2rem;
                            text-align: center;
                            color: white;
                            margin-bottom: 1.5rem;
                        ">
                            <div style="font-size: 4rem; margin-bottom: 0.5rem;">{emoji}</div>
                            <div style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 0.25rem;">
                                Hi <strong>{name}</strong>, skor prediksi Anda adalah
                            </div>
                            <div style="font-size: 2.5rem; font-weight: 800; color: #38bdf8;">
                                {label}
                            </div>
                            <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.7;">
                                Level {pred_index + 1} of 5
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat memproses prediksi: {e}")