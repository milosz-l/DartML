import streamlit as st


def show_uploaded_df(expanded=False):
    with st.expander("Uploaded data", expanded=expanded):
        st.write(st.session_state.df)
