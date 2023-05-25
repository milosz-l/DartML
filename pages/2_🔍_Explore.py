import streamlit as st
from src.explore.PlotBuilder import PlotBuilder
from src.general_views.uploaded_df_view import show_uploaded_df
from src.general_views.sidebars_view import show_info_sidebar
from src.utils.session_state_checks import df_in_session_state
from src.explore.plots_view import show_heatmap, show_pairplot
import time


st.title("🔍 Explore")

if not df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_uploaded_df(expanded=False)
    show_info_sidebar()

    st.divider()
    # regenerate plots button
    if st.button("Regenerate plots", help="You've just uploaded a new dataframe and the plots didn't change? Then click this button!"):
        if "heatmap" in st.session_state:
            del st.session_state.heatmap
        if "pairplot" in st.session_state:
            del st.session_state.pairplot

    # calculate correlation heatmap if not done yet
    with st.expander("Show correlation heatmap", expanded=False):
        show_heatmap()

    # calculate pairplot if not done yet
    with st.expander("Show pairplot", expanded=False):
        show_pairplot()

# TODO: add button that clears saved figs from st.session_state. Call it "Rebuild plots"
