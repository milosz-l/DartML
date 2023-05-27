import streamlit as st
import pandas as pd
from PIL import Image
import zipfile
from src.session_state.session_state_checks import explain_zip_buffer_in_session_state


def show_image_from_path(path, header="", caption=""):  # TODO: issue number 4336
    try:
        image = Image.open(path)
        if header:
            st.markdown(f"### {header}")
        st.image(image, caption=caption)
    except FileNotFoundError:
        pass


def show_image_from_archive(archive, filename, header="", caption=""):
    try:
        img = archive.read(filename)
        if header:
            st.markdown(f"### {header}")
        st.image(img, caption=caption)
    except KeyError:
        pass  # there is no such item in the archive


def show_tabs(tmpdirname, leaderboard_df):
    pass  # TODO


def show_mljar_markdown(tmpdirname):  # TODO: issue 1840 - use directory zipped into buffer from session_state
    if explain_zip_buffer_in_session_state():
        archive = zipfile.ZipFile(st.session_state.explain_zip_buffer, "r")

        show_image_from_archive(archive, "Ensemble/predicted_vs_residuals.png", header="ytest")

        st.markdown("# AutoML Leaderboard")

        # show leaderboard
        leaderboard_df = pd.read_csv(f"{tmpdirname}/leaderboard.csv")
        st.write(leaderboard_df)

        # show images
        show_image_from_path(f"{tmpdirname}/ldb_performance.png", header="AutoML Performance")

        show_image_from_path(f"{tmpdirname}/ldb_performance_boxplot.png", header="AutoML Performance Boxplot")

        show_image_from_path(f"{tmpdirname}/features_heatmap.png", header="Features Importance")

        show_image_from_path(f"{tmpdirname}/correlation_heatmap.png", header="Spearman Correlation of Models")

        show_tabs(tmpdirname, leaderboard_df)
