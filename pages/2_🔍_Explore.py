import streamlit as st
from src.general_views.df_view import show_sampled_df
from src.general_views.sidebars_view import show_info_sidebar
from src.session_state.session_state_checks import sampled_df_in_session_state
from src.explore.plots_view import show_plots, show_altair_plots
from src.general_views.logo import show_logo


show_logo()
st.title("🔍 Explore")

if not sampled_df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar()
    show_sampled_df()

    st.divider()
    show_altair_plots()
    # show_plots(expanded=True)
