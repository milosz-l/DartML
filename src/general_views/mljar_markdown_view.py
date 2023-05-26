import streamlit as st
import pandas as pd
from PIL import Image


def show_image_from_path(path, caption=""):
    st.image(Image.open(path), caption=caption)


def show_mljar_markdown(tmpdirname):  # TODO: issue 1840 - use directory zipped into buffer from session_state
    st.markdown("# AutoML Leaderboard")

    # show leaderboard
    st.write(pd.read_csv(f"{tmpdirname}/leaderboard.csv"))

    # show images
    st.markdown("### AutoML Performance")
    show_image_from_path(f"{tmpdirname}/ldb_performance.png")

    st.markdown("### AutoML Performance Boxplot")
    show_image_from_path(f"{tmpdirname}/ldb_performance_boxplot.png")

    st.markdown("### Features Importance")
    show_image_from_path(f"{tmpdirname}/features_heatmap.png")

    st.markdown("### Spearman Correlation of Models")
    show_image_from_path(f"{tmpdirname}/correlation_heatmap.png")
