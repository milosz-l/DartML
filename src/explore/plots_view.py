import streamlit as st
import time
from src.explore.PlotBuilder import PlotBuilder


def show_heatmap():
    start_time = time.time()
    if "heatmap" not in st.session_state:
        with st.spinner("Generating heatmap"):
            st.session_state.heatmap = PlotBuilder(st.session_state.df).get_corr_heatmap()
    st.write("Correlation heatmap:")
    st.image(st.session_state.heatmap, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")


def show_pairplot():
    start_time = time.time()
    if "pairplot" not in st.session_state:
        with st.spinner("Generating pairplot"):
            st.session_state.pairplot = PlotBuilder(st.session_state.df).get_pairplot()
    st.write("Pairplot:")
    st.image(st.session_state.pairplot, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")
