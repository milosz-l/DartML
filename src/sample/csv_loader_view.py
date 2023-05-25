import streamlit as st
import pandas as pd


def show_csv_loader():
    uploaded_file = st.file_uploader("Upload a csv file:", type="csv", accept_multiple_files=False)
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.session_state.df = dataframe
