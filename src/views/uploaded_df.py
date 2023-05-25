import streamlit as st
from src.views.sidebars import show_info_sidebar


def show_uploaded_df(expanded=False):
    with st.expander("Show data", expanded=expanded):
        st.write(st.session_state.df)
