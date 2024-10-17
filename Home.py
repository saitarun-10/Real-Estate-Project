import streamlit as st
import os


st.set_page_config(
    page_title="Gurgaon Real Estate Analytics App",
    page_icon="👋🏻",
)

st.write("# Welcome to the Gurgaon Real Estate Analytics App! 👋🏻")
st.image("background.jpg", caption="Gurgaon Skyline", use_column_width=True)
# Description of the features
st.write("""
### Welcome to the Real Estate Insights Portal

Our platform is designed to empower users with advanced tools for navigating the real estate market. Explore our features below to enhance your property search and analysis:

- **Price Predictor**: Utilize our machine learning model to estimate property prices based on various parameters. Gain insights into potential investments and make informed decisions.

- **Analysis App**: Dive into comprehensive data analysis of real estate trends. Our app provides visualizations and insights that help you understand market dynamics and identify opportunities.

- **Recommend Apartments**: Discover your ideal living space with our personalized apartment recommendation system. Enter your preferred location and criteria, and receive tailored suggestions along with detailed information.

This app is designed for homebuyers and investors looking to explore Gurgaon’s real estate market using data-driven insights for informed decision-making. Leverage these powerful tools to optimize your real estate journey!
""")

# st.sidebar.success("Select a demo above.")
