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


def target_column_in_session_state():
    if "target_column_name" in st.session_state:
        return True
    return False


def explain_zip_buffer_in_session_state():
    if "explain_zip_buffer" in st.session_state:
        return True
    return False


def redirected_training_output_in_session_state():
    if "redirected_training_output" in st.session_state:
        return True
    return False


def split_type_in_session_state():
    if "split_type" in st.session_state:
        return True
    return False


def shuffle_in_session_state():
    if "shuffle" in st.session_state:
        return True
    return False


def stratify_in_session_state():
    if "stratify" in st.session_state:
        return True
    return False
