import streamlit as st
from src.explore.df_visualizations import plot_corr_heatmap, plot_pairplot, plot_to_ndarray
import time

# Transform Data
st.title("Explore Data")


if "df" not in st.session_state:
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    # show uploaded df
    st.write("Uploaded DataFrame:")
    st.write(st.session_state.df)

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
            st.session_state.heatmap = plot_to_ndarray(plot_corr_heatmap(st.session_state.df))
            # st.session_state.heatmap = plot_corr_heatmap(st.session_state.df)
    st.write("Correlation heatmap:")
    st.image(st.session_state.heatmap, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")

    # calculate pairplot if not done yet
    start_time = time.time()
    if "pairplot" not in st.session_state:
        with st.spinner("Generating pairplot"):
            # st.session_state.pairplot = sns.pairplot(st.session_state.df)
            st.session_state.pairplot = plot_to_ndarray(plot_pairplot(st.session_state.df))
            # st.session_state.pairplot = plot_pairplot(st.session_state.df)
    st.write("Pairplot:")
    st.image(st.session_state.pairplot, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")

# TODO: add button that clears saved figs from st.session_state. Call it "Rebuild plots"
