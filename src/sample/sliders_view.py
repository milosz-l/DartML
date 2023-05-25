import streamlit as st
from src.utils.session_state_checks import df_in_session_state, sample_percentage_in_session_state, train_test_split_percentage_in_session_state


def show_data_sample_slider():
    # TODO: default value in sliders must come back to already selected
    st.session_state.data_sample_percentage = st.slider("Sample data:", 1, 100, 100, help="Leave the slider at 100% if you want to use whole data.", disabled=not df_in_session_state()) / 100
    if df_in_session_state() and sample_percentage_in_session_state():
        all_rows_num = len(st.session_state.df.index)
        subset_rows_num = round(st.session_state.data_sample_percentage * all_rows_num)
        st.caption(f"You sampled {round(st.session_state.data_sample_percentage * 100)}% of data, which is {subset_rows_num} rows out of {all_rows_num} rows in the whole dataset.")


def show_train_test_split_slider():
    st.session_state.train_test_split_percentage = (
        st.slider("Choose train data size:", 1, 100, 80, help="Training data is usually 70-80% of the sampled data.", disabled=not df_in_session_state()) / 100
    )
    if df_in_session_state() and train_test_split_percentage_in_session_state():
        train_data_size = round(st.session_state.train_test_split_percentage * 100)
        test_data_size = 100 - train_data_size
        st.caption(f"Chosen train/test data split is {train_data_size}%/{test_data_size}%.")
