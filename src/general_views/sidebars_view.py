import streamlit as st
from src.session_state.session_state_checks import sampled_df_in_session_state, df_in_session_state, sample_percentage_in_session_state, train_test_split_percentage_in_session_state


def df_info_sidebar(df_info):
    st.sidebar.subheader("Uploaded data info")
    st.sidebar.write(f'{df_info["col_num"]} columns')
    st.sidebar.write(f'{df_info["row_num"]} rows')


def sampled_df_info_sidebar(sampled_df_info):
    st.sidebar.subheader("Sampled data info")
    st.sidebar.progress(st.session_state.data_sample_percentage, text=f"{round(st.session_state.data_sample_percentage * 100)}% of uploaded data")
    st.sidebar.write(f'{sampled_df_info["col_num"]} columns')
    st.sidebar.write(f'{sampled_df_info["row_num"]} rows')


def train_test_split_info_sidebar():
    st.sidebar.subheader("Train/test split info")
    train_data_size = round(st.session_state.train_test_split_percentage * 100)
    test_data_size = 100 - train_data_size
    st.sidebar.progress(st.session_state.train_test_split_percentage, text=f"{train_data_size}%/{test_data_size}%")


def show_info_sidebar():
    # if df_in_session_state():
    #     df_info = {}
    #     df_info["row_num"] = len(st.session_state.df.index)
    #     df_info["col_num"] = len(st.session_state.df.columns)
    #     df_info_sidebar(df_info)

    if sample_percentage_in_session_state() and sampled_df_in_session_state():
        sampled_df_info = {}
        sampled_df_info["row_num"] = len(st.session_state.sampled_df.index)
        sampled_df_info["col_num"] = len(st.session_state.sampled_df.columns)
        sampled_df_info_sidebar(sampled_df_info)

        if train_test_split_percentage_in_session_state():
            train_test_split_info_sidebar()
