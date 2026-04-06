import streamlit as st

#=====
# Config
#=====

st.set_page_config(
    page_title="My Dashboard Portfolio",
    layout="wide",
)

#=====
# Header
#=====
st.title("My Dashboard Portfolio")
st.caption("Multi-Project Analytics Dashboard (Tabular Data Focus)")

st.markdown("---")

#=====
# Sidebar
#=====
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
        "EDA"
        "Model Performance",
        "Feature Importance",
    ]
)

#=====
#Breadcrumb
#=====
st.caption(f"home > {project} > {module}")

st.markdown("---")

#=====
#Routing Function
#=====
def load_project_module(project, module):
    if project == "Crop Prediction":
        if module == "Data Overview":
            st.subheader("Crop Prediction - Data Overview")
            st.write("This section provides an overview of the crop prediction dataset, including data sources, key features, and summary statistics.")
        elif module == "EDA":
            st.subheader("Crop Prediction - Exploratory Data Analysis")
            st.write("This section includes visualizations and analyses to explore the relationships between features and the target variable in the crop prediction dataset.")
        elif module == "Model Performance":
            st.subheader("Crop Prediction - Model Performance")
            st.write("This section evaluates the performance of various machine learning models used for crop prediction, including metrics and visualizations.")
        elif module == "Feature Importance":
            st.subheader("Crop Prediction - Feature Importance")
            st.write("This section identifies and visualizes the most important features contributing to crop prediction.")
    
    elif project == "House Price Prediction":
        if module == "Data Overview":
            st.subheader("House Price Prediction - Data Overview")
            st.write("This section provides an overview of the house price prediction dataset, including data sources, key features, and summary statistics.")
        elif module == "EDA":
            st.subheader("House Price Prediction - Exploratory Data Analysis")
            st.write("This section includes visualizations and analyses to explore the relationships between features and the target variable in the house price prediction dataset.")
        elif module == "Model Performance":
            st.subheader("House Price Prediction - Model Performance")
            st.write("This section evaluates the performance of various machine learning models used for house price prediction, including metrics and visualizations.")
        elif module == "Feature Importance":
            st.subheader("House Price Prediction - Feature Importance")
            st.write("This section identifies and visualizes the most important features contributing to house price prediction.")
    else:
        st.error("Project tidak ditemukan")
        return

    # run selected module
    run()

# ======================
# EXECUTE MODULE
# ======================
load_project_module(project, module)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("© 2026 - Data Analyst Portfolio")