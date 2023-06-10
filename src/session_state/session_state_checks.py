import streamlit as st


def df_in_session_state() -> bool:
    """
    Returns whether `df` is in the session state.
    """
    if "df" in st.session_state:
        return True
    return False


def sampled_df_in_session_state() -> bool:
    """
    Returns whether `sampled_df` is in the session state.
    """
    if "sampled_df" in st.session_state:
        return True
    return False


def sample_percentage_in_session_state() -> bool:
    """
    Returns whether `sample_percentage` is in the session state.
    """
    if "data_sample_percentage" in st.session_state:
        return True
    return False


def train_test_split_percentage_in_session_state() -> bool:
    """
    Returns whether `train_test_split_percentage` is in the session state.
    """
    if "train_test_split_percentage" in st.session_state:
        return True
    return False


def target_column_in_session_state() -> bool:
    """
    Returns whether `target_column_name` is in the session state.
    """
    if "target_column_name" in st.session_state:
        return True
    return False


def explain_zip_buffer_in_session_state() -> bool:
    """
    Returns whether `explain_zip_buffer` is in the session state.
    """
    if "explain_zip_buffer" in st.session_state:
        return True
    return False


def redirected_training_output_in_session_state() -> bool:
    """
    Returns whether `redirected_training_output` is in the session state.
    """
    if "redirected_training_output" in st.session_state:
        return True
    return False


def split_type_in_session_state() -> bool:
    """
    Returns whether `split_type` is in the session state.
    """
    if "split_type" in st.session_state:
        return True
    return False


def shuffle_in_session_state() -> bool:
    """
    Returns whether `shuffle` is in the session state.
    """
    if "shuffle" in st.session_state:
        return True
    return False


def stratify_in_session_state() -> bool:
    """
    Returns whether `stratify` is in the session state.
    """
    if "stratify" in st.session_state:
        return True
    return False


def automl_trainer_in_session_state() -> bool:
    """
    Returns whether `automl_trainer` is in the session state.
    """
    if "automl_trainer" in st.session_state:
        return True
    return False
