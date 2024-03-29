import streamlit as st

from src.session_state.session_state_checks import (
    sample_percentage_in_session_state,
    sampled_df_in_session_state,
    shuffle_in_session_state,
    split_type_in_session_state,
    stratify_in_session_state,
    train_test_split_percentage_in_session_state,
)


def df_info_sidebar(df_info: dict) -> None:
    """
    Shows the DataFrame info in the sidebar (number of columns and rows).
    args:
        df_info: dictionary with the number of columns and rows of the df
    """
    st.sidebar.subheader("Uploaded data info")
    st.sidebar.write(f'{df_info["col_num"]} columns')
    st.sidebar.write(f'{df_info["row_num"]} rows')


def sampled_df_info_sidebar(sampled_df_info: dict) -> None:
    """
    Shows the sampled DataFrame info in the sidebar (number of columns and rows).
    args:
        sampled_df_info: dictionary with the number of columns and rows of the sampled DataFrame
    """
    st.sidebar.subheader("Sampled data info")
    st.sidebar.progress(
        st.session_state.data_sample_percentage,
        text=f"{round(st.session_state.data_sample_percentage * 100)}% of uploaded data",
    )
    st.sidebar.write(f'{sampled_df_info["col_num"]} columns')
    st.sidebar.write(f'{sampled_df_info["row_num"]} rows')


def train_test_split_info_sidebar() -> None:
    """
    Shows the train/test split info in the sidebar.
    """
    st.sidebar.subheader("Train/test split info")
    if split_type_in_session_state:
        if st.session_state.split_type == "split":
            train_data_size = round(st.session_state.train_test_split_percentage * 100)
            test_data_size = 100 - train_data_size
            st.sidebar.progress(
                st.session_state.train_test_split_percentage,
                text=f"{train_data_size}%/{test_data_size}%",
            )
        elif st.session_state.split_type == "kfold":
            st.sidebar.caption("5-fold cross validation chosen")


def target_column_selectbox_sidebar() -> None:
    """
    Shows the target column selectbox in the sidebar.
    """
    columns_list = st.session_state.sampled_df.columns.tolist()
    selectbox_default_index = len(columns_list) - 1
    st.session_state.target_column_name = st.sidebar.selectbox(
        "Target column", columns_list, index=selectbox_default_index
    )


def stratify_and_shuffle_info_sidebar() -> None:
    """
    Shows the stratify and shuffle info in the sidebar.
    """
    if st.session_state.shuffle:
        st.sidebar.subheader("Shuffle :green[on]")
    else:
        st.sidebar.subheader("Shuffle :red[off]")

    if st.session_state.stratify:
        st.sidebar.subheader("Stratify :green[on]")
    else:
        st.sidebar.subheader("Stratify :red[off]")


def show_info_sidebar(target_column_selection: bool = False) -> None:
    """
    Shows all the info in the sidebar.
    args:
        target_column_selection: boolean that indicates if the target column selection should be shown
    """

    if sample_percentage_in_session_state() and sampled_df_in_session_state():
        sampled_df_info = {}
        sampled_df_info["row_num"] = len(st.session_state.sampled_df.index)
        sampled_df_info["col_num"] = len(st.session_state.sampled_df.columns)
        sampled_df_info_sidebar(sampled_df_info)

        if train_test_split_percentage_in_session_state():
            st.sidebar.divider()
            train_test_split_info_sidebar()

        if shuffle_in_session_state() and stratify_in_session_state():
            st.sidebar.divider()
            stratify_and_shuffle_info_sidebar()

    if target_column_selection:
        if sampled_df_in_session_state():
            st.sidebar.divider()
            target_column_selectbox_sidebar()
