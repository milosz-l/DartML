import io
import os
import tempfile
import zipfile
from typing import Literal, Optional

import streamlit as st
from supervised.exceptions import AutoMLException

from src import config
from src.modify_and_model.train_automl import train_automl
from src.session_state.session_state_checks import (
    sampled_df_in_session_state, split_type_in_session_state,
    train_test_split_percentage_in_session_state)


def zip_directory_into_buffer(directory_path: str, buffer: io.BytesIO) -> None:
    """
    Zips the directory into given buffer.
    args:
        directory_path: path to the directory to zip
        buffer: buffer to zip the directory into
    """
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Iterate over all the files and subdirectories in the directory
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Add the file to the zip archive preserving the directory structure
                zipf.write(file_path, os.path.relpath(file_path, directory_path))


def simple_target_column_selectbox() -> str:
    """
    Shows a target column selectbox with the last column selected by default.
    Returns the selected target column.
    args: None"""
    columns_list = st.session_state.sampled_df.columns.tolist()
    selectbox_default_index = len(columns_list) - 1
    return st.selectbox(
        "Choose target column:", columns_list, index=selectbox_default_index
    )


def problem_type_selectbox() -> str:
    """
    Shows a problem type selectbox with auto selected by default.
    Returns the selected problem type.
    """
    problem_types = [
        "auto",
        "binary classification",
        "multiclass classification",
        "regression",
    ]
    chosen_problem_type = st.selectbox(
        "Choose problem type",
        problem_types,
        index=0,
        help="You can choose problem type manually or leave it at auto (then problem type will be guessed based on target values)",
    )
    return chosen_problem_type


def algorithms_selectbox() -> list[str]:
    """
    Shows a multiselectbox with first five algorithms selected by default.
    Returns list with selected algorithms.
    """
    algorithms = [
        "Baseline",
        "Linear",
        "Decision Tree",
        "Random Forest",
        "Xgboost",
        "Extra Trees",
        "LightGBM",
        "CatBoost",
        "Neural Network",
        "Nearest Neighbors",
    ]
    return st.multiselect("Choose algorithms to train", algorithms, algorithms[0:5])


def metric_selectbox(
    problem_type: Literal[
        "binary classification", "multiclass classification", "regression", "auto"
    ]
) -> Optional[str]:
    """
    If problem_type is not auto, shows a metric selectbox with the first metric selected by default.
    Returns the selected metric.
    """
    if problem_type == "binary classification":
        metrics = ["logloss", "auc", "f1", "average_precision", "accuracy"]
    elif problem_type == "multiclass classification":
        metrics = ["logloss", "f1", "accuracy"]
    elif problem_type == "regression":
        metrics = ["rmse", "mse", "mae", "r2", "mape", "spearman", "pearson"]
    else:  # problem type is auto
        metrics = []

    if metrics:
        return st.selectbox(
            "Choose metric", metrics, index=0, help="Choose evaluation metric."
        )
    return None


def total_time_limit_slider() -> int:
    """
    Shows the total time limit slider.
    Returns selected total time limit in seconds.
    """

    def get_minutes_and_seconds(seconds: int) -> tuple[int, int]:
        """
        Returns minutes and seconds from given seconds.
        args:
            seconds: seconds to convert
        """
        minutes = seconds // 60
        seconds = seconds % 60
        return minutes, seconds

    total_time_limit = st.slider("Total time limit (in seconds)", 60, 1800, 60, 15)
    minutes, seconds = get_minutes_and_seconds(total_time_limit)
    st.caption(
        f"The maximum training time will be {minutes} minutes and {seconds} seconds."
    )
    return total_time_limit


def mode_selectbox() -> str:
    """
    Shows the mode selectbox.
    Returns selected mode.
    """
    mode = st.selectbox(
        "Choose training mode",
        ["Compete", "Perform", "Explain"],
        help="Compete mode is dedicated for training best models. Explain mode is for generating visualizations (e.g. SHAP plots). Perform mode is something in between.",
    )
    if mode == "Explain" or mode == "Perform":
        st.caption(
            "Note: Visualizations generated for Explain and Perform modes may be incorrect if the app is under heavy load. If the app may be used by many users, is is advised to use the Compete mode."
        )
    return mode


def clean_up_directory_from_png_files(tmpdirname: str) -> None:
    """
    Removes all png files for given directory and its subdirectories.
    Used in Compete mode (png files are removed for multi-user purposes).
    args:
        tmpdirname: path to the directory to clean up
    """
    for root, dirs, files in os.walk(tmpdirname):
        for file in files:
            if file.endswith(".png"):
                os.remove(os.path.join(root, file))


def logs_visable_checkbox() -> bool:
    """
    Shows checkbox that determins whether logs after training should be shown.
    Returns True if logs should be shown, False otherwise.
    """
    logs_visable = st.checkbox(
        "Show training logs",
        value=False,
        help="Determin whether logs should be shown after training.",
    )
    if logs_visable:
        st.caption(
            "Note: Logs generated may be incorrect if the app is under heavy load. If the app may be used by many users, is is advised to leave it unchecked."
        )
    return logs_visable


def show_training_config() -> None:
    """
    Shows whole AutoML training configuration.
    """
    if (
        sampled_df_in_session_state()
        and train_test_split_percentage_in_session_state()
        and split_type_in_session_state()
    ):
        st.divider()
        target_col_name = simple_target_column_selectbox()
        st.divider()

        problem_type = problem_type_selectbox()
        metric = metric_selectbox(problem_type)
        st.divider()

        algorithms = algorithms_selectbox()
        st.divider()

        total_time_limit = total_time_limit_slider()
        st.divider()

        if config.SINGLE_USER_ADVANCED_APP_VERSION:
            mode = mode_selectbox()
            st.divider()
        else:
            mode = "Compete"

        if config.SINGLE_USER_ADVANCED_APP_VERSION:
            redirect_logs = logs_visable_checkbox()
            st.divider()
        else:
            redirect_logs = False

        if st.button("Generate new report"):
            try:
                with st.spinner("Generating report..."):
                    with tempfile.TemporaryDirectory() as tmpdirname:
                        # run automl training
                        train_automl(
                            target_col_name,
                            tmpdirname,
                            problem_type,
                            metric,
                            algorithms,
                            total_time_limit,
                            mode,
                            redirect_logs,
                        )

                        # clean up directory if the mode is Compete
                        if mode == "Compete":
                            clean_up_directory_from_png_files(tmpdirname)

                        # save dir with results as zip to session_state
                        st.session_state.explain_zip_buffer = io.BytesIO()
                        zip_directory_into_buffer(
                            tmpdirname, st.session_state.explain_zip_buffer
                        )
                st.success("Done! Now you can go to Assess tab to see the results!")
            except AutoMLException as error:
                st.warning(
                    "Something went wrong. 😔 Please check if sampled dataframe isn't too small or if train data percentage isn't too high or too low."
                )
                st.write(error)
