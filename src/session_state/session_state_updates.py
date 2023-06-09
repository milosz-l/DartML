import streamlit as st
from src.config import RANDOM_STATE


def update_sampled_df(subset_rows_num: int) -> None:
    """
    Updates the sampled_df in the session_state.
    args:
        subset_rows_num: number of rows to take from `df` to `sampled_df`
    """
    st.session_state.sampled_df = st.session_state.df.sample(n=subset_rows_num, random_state=RANDOM_STATE)
