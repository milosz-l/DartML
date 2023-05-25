import streamlit as st
from src.explore.PlotBuilder import PlotBuilder
from src.general_views.uploaded_df import show_uploaded_df
from src.general_views.sidebars import show_info_sidebar
from src.utils.session_state_checks import df_in_session_state
import time


st.title("🔍 Explore")

if not df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_uploaded_df(expanded=False)
    show_info_sidebar()

    # regenerate plots button
    st.write("You've just uploaded a new dataframe and the plots didn't change? Then click the following button:")
    if st.button("Regenerate plots"):
        if "heatmap" in st.session_state:
            del st.session_state.heatmap
        if "pairplot" in st.session_state:
            del st.session_state.pairplot

    # calculate correlation heatmap if not done yet
    start_time = time.time()
    if "heatmap" not in st.session_state:
        with st.spinner("Generating heatmap"):
            st.session_state.heatmap = PlotBuilder(st.session_state.df).get_corr_heatmap()
    st.write("Correlation heatmap:")
    st.image(st.session_state.heatmap, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")

    st.divider()

    # calculate pairplot if not done yet
    start_time = time.time()
    if "pairplot" not in st.session_state:
        with st.spinner("Generating pairplot"):
            st.session_state.pairplot = PlotBuilder(st.session_state.df).get_pairplot()
    st.write("Pairplot:")
    st.image(st.session_state.pairplot, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")

# TODO: add button that clears saved figs from st.session_state. Call it "Rebuild plots"
