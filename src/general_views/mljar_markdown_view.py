import streamlit as st
import pandas as pd
from PIL import Image
import zipfile
import io
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
        img_bytes = archive.read(filename)
        if header:
            st.markdown(header)
        st.image(img_bytes, caption=caption)
    except KeyError:
        pass  # there is no such item in the archive


def show_csv_from_archive(archive, filename, header=""):
    try:
        csv_bytes = archive.read(filename)
        csv_io = io.BytesIO(csv_bytes)
        df = pd.read_csv(csv_io)
        if header:
            st.markdown(header)
        st.write(df)
    except KeyError:
        pass  # there is no such item in the archive


def show_tabs():
    pass  # TODO


def show_mljar_markdown():  # TODO: issue 1840 - use directory zipped into buffer from session_state
    if explain_zip_buffer_in_session_state():
        # get access to zipped archive saved in session_state
        archive = zipfile.ZipFile(st.session_state.explain_zip_buffer, "r")

        # show leaderboard
        show_csv_from_archive(archive, "leaderboard.csv", header="# AutoML Leaderboard")

        # show images
        show_image_from_archive(archive, "ldb_performance.png", header="### AutoML Performance")
        show_image_from_archive(archive, "ldb_performance_boxplot.png", header="### AutoML Performance Boxplot")
        show_image_from_archive(archive, "features_heatmap.png", header="### Features Importance")
        show_image_from_archive(archive, "correlation_heatmap.png", header="### Spearman Correlation of Models")

        show_tabs()
