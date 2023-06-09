import io
import zipfile

import pandas as pd
import streamlit as st
from PIL import Image

from src.session_state.session_state_checks import explain_zip_buffer_in_session_state


def show_image_from_path(path: str, header: str = "", caption: str = "") -> None:
    """
    Shows image from given path.
    If there is no image in given path, does nothing.
    args:
        path: path to image
        header: header to be shown above image (optional)
        caption: caption to be shown below image (optional)
    """
    try:
        image = Image.open(path)
        if header:
            st.markdown(f"### {header}")
        st.image(image, caption=caption)
    except FileNotFoundError:
        pass


def show_image_from_archive(
    archive: zipfile.ZipFile, filename: str, header: str = "", caption: str = ""
) -> None:
    """
    Shows image from given archive.
    If there is no file with given name in given archive, does nothing.
    args:
        archive: archive with training results
        filename: name of file with image to be shown
        header: header to be shown above image (optional)
        caption: caption to be shown below image (optional)
    """
    try:
        img_bytes = archive.read(filename)
        if header:
            st.markdown(header)
        st.image(img_bytes, caption=caption)
    except KeyError:
        pass  # there is no such item in the archive


def show_csv_from_archive(
    archive: zipfile.ZipFile, filename: str, header: str = ""
) -> None:
    """
    Shows csv from given archive.
    If there is no file with given name in given archive, does nothing.
    args:
        archive: archive with training results
        filename: name of the csv file to be shown
        header: header to be shown above csv (optional)
    """
    try:
        csv_bytes = archive.read(filename)
        csv_io = io.BytesIO(csv_bytes)
        df = pd.read_csv(csv_io)
        if header:
            st.markdown(header)
        st.write(df)
    except KeyError:
        pass  # there is no such item in the archive


def show_tabs() -> None:
    pass  # TODO


def show_report() -> None:
    """
    Shows portion of the report saved in session_state as zipped archive.
    """
    if explain_zip_buffer_in_session_state():
        with st.expander("Report", expanded=True):
            # get access to zipped archive saved in session_state
            archive = zipfile.ZipFile(st.session_state.explain_zip_buffer, "r")

            # show leaderboard
            show_csv_from_archive(
                archive, "leaderboard.csv", header="# AutoML Leaderboard"
            )

            # show images
            show_image_from_archive(
                archive, "ldb_performance.png", header="### AutoML Performance"
            )
            show_image_from_archive(
                archive,
                "ldb_performance_boxplot.png",
                header="### AutoML Performance Boxplot",
            )
            show_image_from_archive(
                archive, "features_heatmap.png", header="### Features Importance"
            )
            show_image_from_archive(
                archive,
                "correlation_heatmap.png",
                header="### Spearman Correlation of Models",
            )

            show_tabs()
