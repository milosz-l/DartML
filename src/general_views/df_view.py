import streamlit as st


def show_uploaded_df(expanded=False):
    with st.expander("Uploaded data", expanded=expanded):
        st.write(st.session_state.df)


def show_sampled_df(expanded=False):
    with st.expander("Sampled data", expanded=expanded):
        st.write(st.session_state.sampled_df)
