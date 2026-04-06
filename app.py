import streamlit as st

# ======================
# Config
# ======================
st.set_page_config(
    page_title="My Dashboard Portfolio",
    layout="wide",
)

# ======================
# Header
# ======================
st.title("My Dashboard Portfolio")
st.caption("Multi-Project Analytics Dashboard (Tabular Data Focus)")

st.markdown("---")

# ======================
# Sidebar
# ======================
st.sidebar.header("Navigation")

project = st.sidebar.selectbox(
    "Select a Project",
    [
        "Crop Prediction",
        "House Price Prediction",
    ]
)

module = st.sidebar.radio(
    "Select a Module",
    [
        "Data Overview",
        "EDA",
        "Model Performance",
        "Feature Importance",
    ]
)

# ======================
# Breadcrumb
# ======================
st.caption(f"home > {project} > {module}")
st.markdown("---")

# ======================
# Routing Function
# ======================
def load_project_module(project, module):
    if project == "Crop Prediction":
        if module == "Data Overview":
            st.subheader("Crop Prediction - Data Overview")
            st.write("Overview dataset crop prediction.")
        elif module == "EDA":
            st.subheader("Crop Prediction - EDA")
        elif module == "Model Performance":
            st.subheader("Crop Prediction - Model Performance")
        elif module == "Feature Importance":
            st.subheader("Crop Prediction - Feature Importance")

    elif project == "House Price Prediction":
        if module == "Data Overview":
            st.subheader("House Price - Data Overview")
        elif module == "EDA":
            st.subheader("House Price - EDA")
        elif module == "Model Performance":
            st.subheader("House Price - Model Performance")
        elif module == "Feature Importance":
            st.subheader("House Price - Feature Importance")

    else:
        st.error("Project tidak ditemukan")

# ======================
# EXECUTE
# ======================
load_project_module(project, module)

# ======================
# Footer
# ======================
st.markdown("---")
st.caption("© 2026 - Data Analyst Portfolio")