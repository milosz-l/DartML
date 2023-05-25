import streamlit as st
from src.explore.PlotBuilder import PlotBuilder
from src.general_views.uploaded_df_view import show_uploaded_df
from src.general_views.sidebars_view import show_info_sidebar
from src.utils.session_state_checks import df_in_session_state
from src.explore.plots_view import show_heatmap, show_pairplot
from src.explore.buttons_view import show_regenerate_heatmap_button, show_regenerate_pairplot_button
import time


st.title("🔍 Explore")

if not df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_uploaded_df(expanded=False)
    show_info_sidebar()

    st.divider()

    with st.expander("Show correlation heatmap", expanded=False):
        show_regenerate_heatmap_button()
        show_heatmap()

    with st.expander("Show pairplot", expanded=False):
        show_regenerate_pairplot_button()
        show_pairplot()
