import streamlit as st
from src.session_state.session_state_checks import df_in_session_state, sampled_df_in_session_state


def show_uploaded_df(expanded=False):
    if df_in_session_state():
        with st.expander("Uploaded data", expanded=expanded):
            st.write(st.session_state.df)


def show_sampled_df(expanded=False):
    if sampled_df_in_session_state():
        with st.expander("Sampled data", expanded=expanded):
            st.write(st.session_state.sampled_df)
