import streamlit as st
import pandas as pd


def show_csv_loader() -> None:
    """
    Shows the csv loader.
    """
    uploaded_file = st.file_uploader("Upload your own csv file:", type="csv", accept_multiple_files=False)
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.session_state.df = dataframe


def show_use_example_data_button() -> None:
    """
    Shows the use example data button.
    """
    if st.button("Use example data"):
        try:
            st.session_state.df = pd.read_csv("example_data/Hotel_Reservations.csv")
        except FileNotFoundError as error:
            st.error("Couldn't load the example data, but it can be downloaded here: https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset")