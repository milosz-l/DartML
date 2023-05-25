import streamlit as st
from src.config import RANDOM_STATE


def update_sampled_df(subset_rows_num):
    st.session_state.sampled_df = st.session_state.df.sample(n=subset_rows_num, random_state=RANDOM_STATE)
