import streamlit as st

st.set_page_config(
    page_title="Homepage",
)

st.sidebar.success("Select a page above.")

st.title("Welcome to the Obesity Level Prediction App")
    
st.header("Overview")
st.write("""
    This app is designed to help you understand and predict obesity levels based on various health and lifestyle factors. 
    Navigate through the different sections to learn more about the dataset, explore descriptive statistics, and make predictions.
    """)

st.header("Navigation")
st.write("""
    - **Introduction**: Learn about the purpose and background of this app.
    - **Descriptive Analysis**: Explore detailed statistics and visualizations of the dataset.
    - **Prediction**: Input your data to predict the obesity level.
    """)
