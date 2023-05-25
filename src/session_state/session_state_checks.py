import streamlit as st


def df_in_session_state():
    if "df" in st.session_state:
        return True
    return False


def sampled_df_in_session_state():
    if "sampled_df" in st.session_state:
        return True
    return False


def sample_percentage_in_session_state():
    if "data_sample_percentage" in st.session_state:
        return True
    return False


def train_test_split_percentage_in_session_state():
    if "train_test_split_percentage" in st.session_state:
        return True
    return False
