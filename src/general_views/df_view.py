import streamlit as st

from src.session_state.session_state_checks import (
    df_in_session_state, sampled_df_in_session_state)


def show_uploaded_df(expanded: bool = False) -> None:
    """
    Shows the uploaded dataframe.
    args:
        expanded: whether the expander should initially be expanded or not
    """
    if df_in_session_state():
        with st.expander("Uploaded data", expanded=expanded):
            st.write(st.session_state.df)


def show_sampled_df(expanded: bool = False) -> None:
    """
    Shows the sampled dataframe.
    args:
        expanded: whether the expander should initially be expanded or not
    """
    if sampled_df_in_session_state():
        with st.expander("Sampled data", expanded=expanded):
            st.write(st.session_state.sampled_df)
