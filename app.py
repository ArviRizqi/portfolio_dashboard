import streamlit as st

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Portfolio Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================
# HEADER / HERO
# ======================
st.markdown("""
# 📊 Data Portfolio Dashboard
### Interactive Analytics & Machine Learning Projects
""")

st.markdown("""
Explore multiple real-world analytics projects built on tabular data,
including EDA, clustering, forecasting, and model evaluation.
""")

st.markdown("---")

# ======================
# PROJECT SELECTOR (MAIN CONTROL)
# ======================
col1, col2 = st.columns([2, 1])

with col1:
    project = st.selectbox(
        "📂 Select Project",
        [
            "Crop Prediction",
            "House Price Prediction",
        ]
    )

with col2:
    module = st.selectbox(
        "📊 Select Module",
        [
            "Data Overview",
            "EDA",
            "Model Performance",
            "Feature Importance",
        ]
    )

# ======================
# KPI SECTION (GLOBAL)
# ======================
st.markdown("### 📈 Portfolio Highlights")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Projects", "2")
col2.metric("Models", "6+")
col3.metric("Tech Stack", "Python")
col4.metric("Focus", "Tabular ML")

st.markdown("---")

# ======================
# MODULE NAVIGATION CARDS
# ======================
st.markdown("### 🚀 Explore Modules")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Data Overview"):
        module = "Data Overview"

with col2:
    if st.button("📈 EDA"):
        module = "EDA"

with col3:
    if st.button("🤖 Model"):
        module = "Model Performance"

with col4:
    if st.button("⭐ Feature"):
        module = "Feature Importance"

st.markdown("---")

# ======================
# BREADCRUMB
# ======================
st.caption(f"📍 {project} / {module}")

st.markdown("---")

# ======================
# CONTENT RENDERING
# ======================
def render_content(project, module):

    if project == "Crop Recommendation":

        if module == "Data Overview":
            st.subheader("🌾 Crop Recommendation - Data Overview")
            st.info("Overview of dataset, features, and structure.")

        elif module == "EDA":
            st.subheader("📊 Crop Recommendation - EDA")
            st.info("Interactive exploratory data analysis.")

        elif module == "Model Performance":
            st.subheader("🤖 Crop Recommendation - Model Performance")
            st.info("Model comparison and evaluation.")

        elif module == "Feature Importance":
            st.subheader("⭐ Crop Recommendation - Feature Importance")
            st.info("Key feature contribution analysis.")

    elif project == "House Price Prediction":

        if module == "Data Overview":
            st.subheader("🏠 House Price - Data Overview")

        elif module == "EDA":
            st.subheader("📊 House Price - EDA")

        elif module == "Model Performance":
            st.subheader("🤖 House Price - Model Performance")

        elif module == "Feature Importance":
            st.subheader("⭐ House Price - Feature Importance")

# ======================
# EXECUTE
# ======================
render_content(project, module)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("© 2026 | Data Analyst Portfolio")