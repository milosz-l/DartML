import streamlit as st
from src.session_state.session_state_checks import sampled_df_in_session_state, target_column_in_session_state


def target_column_selectbox():
    columns_list = st.session_state.sampled_df.columns.tolist()
    # if target_column_in_session_state():  # TODO: issue number 1289
    #     if st.session_state.target_column_name in columns_list:
    #         selectbox_default_index = columns_list.index(st.session_state.target_column_name)
    #     else:
    #         selectbox_default_index = 0
    #     # st.experimental_show(selectbox_default_index)
    # else:
    #     selectbox_default_index = 0
    selectbox_default_index = len(columns_list) - 1
    st.session_state.target_column_name = st.selectbox("Target column", columns_list, index=selectbox_default_index)


def show_target_column_selectbox():
    if sampled_df_in_session_state():
        target_column_selectbox()
