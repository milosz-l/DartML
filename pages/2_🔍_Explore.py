import streamlit as st
from src.explore.PlotBuilder import PlotBuilder
from src.general_views.df_view import show_sampled_df
from src.general_views.sidebars_view import show_info_sidebar
from src.session_state.session_state_checks import df_in_session_state
from src.explore.plots_view import show_heatmap, show_pairplot
from src.explore.buttons_view import show_regenerate_heatmap_button, show_regenerate_pairplot_button
import time


st.title("🔍 Explore")

if not df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_sampled_df(expanded=False)
    show_info_sidebar()

    st.divider()

    with st.expander("Show correlation heatmap", expanded=False):
        show_regenerate_heatmap_button()
        if not st.session_state.sampled_df.empty:
            show_heatmap()

    with st.expander("Show pairplot", expanded=False):
        show_regenerate_pairplot_button()
        if not st.session_state.sampled_df.empty:
            show_pairplot()
