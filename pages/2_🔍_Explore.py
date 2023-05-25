import streamlit as st
from src.explore.PlotBuilder import PlotBuilder
from src.general_views.df_view import show_sampled_df
from src.general_views.sidebars_view import show_info_sidebar
from src.session_state.session_state_checks import df_in_session_state
from src.explore.plots_view import show_plots
import time


st.title("🔍 Explore")

if not df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar()
    show_sampled_df(expanded=False)

    st.divider()
    show_plots()
