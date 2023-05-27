import streamlit as st
import time
from src.explore.PlotBuilder import PlotBuilder
from src.explore.buttons_view import show_regenerate_heatmap_button, show_regenerate_pairplot_button


def show_heatmap():
    start_time = time.time()
    if "heatmap" not in st.session_state:
        with st.spinner("Generating heatmap"):
            st.session_state.heatmap = PlotBuilder(st.session_state.sampled_df).get_corr_heatmap()
    st.image(st.session_state.heatmap, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")


def show_pairplot():
    start_time = time.time()
    if "pairplot" not in st.session_state:
        with st.spinner("Generating pairplot"):
            st.session_state.pairplot = PlotBuilder(st.session_state.sampled_df).get_pairplot()
    st.image(st.session_state.pairplot, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")


def show_plots(expanded=False):
    with st.expander("Show correlation heatmap", expanded=expanded):
        show_regenerate_heatmap_button()
        if not st.session_state.sampled_df.empty:
            show_heatmap()

    with st.expander("Show pairplot", expanded=expanded):
        show_regenerate_pairplot_button()
        if not st.session_state.sampled_df.empty:
            show_pairplot()
