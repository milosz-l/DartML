import os

import pandas as pd
import streamlit as st
from PIL import Image, UnidentifiedImageError

from src import config


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
            st.markdown(header)
        st.image(image, caption=caption)
    except (FileNotFoundError, UnidentifiedImageError):
        pass  # there is no such file


def show_csv_from_path(path: str, header: str = "") -> None:
    """
    Shows csv from given path.
    If there is no file with given name in given path, does nothing.
    args:
        path: path to csv file
        header: header to be shown above csv (optional)
    """
    try:
        df = pd.read_csv(path)
        if header:
            st.markdown(header)
        st.write(df)
    except FileNotFoundError:
        pass  # there is no such file


def show_tabs() -> None:
    pass  # TODO


def show_report(path: str) -> None:
    """
    Shows portion of the report saved in temporary directory.
    args:
        path: path to temporary directory
    """
    with st.expander("Report", expanded=True):
        # show leaderboard
        show_csv_from_path(
            os.path.join(path, config.REPORT_DIRECTORY_NAME, "leaderboard.csv"),
            header="# AutoML Leaderboard",
        )

        # show images
        show_image_from_path(
            os.path.join(path, config.REPORT_DIRECTORY_NAME, "ldb_performance.png"),
            header="### AutoML Performance",
        )
        show_image_from_path(
            os.path.join(
                path, config.REPORT_DIRECTORY_NAME, "ldb_performance_boxplot.png"
            ),
            header="### AutoML Performance Boxplot",
        )
        show_image_from_path(
            os.path.join(path, config.REPORT_DIRECTORY_NAME, "features_heatmap.png"),
            header="### Features Importance",
        )
        show_image_from_path(
            os.path.join(path, config.REPORT_DIRECTORY_NAME, "correlation_heatmap.png"),
            header="### Spearman Correlation of Models",
        )

        show_tabs()
