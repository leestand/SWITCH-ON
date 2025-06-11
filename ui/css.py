
import streamlit as st

def load_custom_css():
    st.markdown(
        """
        <style>
        .reportview-container {
            background-color: #f4f4f4;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
