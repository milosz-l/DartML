import io
import os
import zipfile

import streamlit as st

from src import config
from src.assess.report_view import show_report
from src.session_state.session_state_checks import (
    automl_trainer_in_session_state,
    sampled_df_in_session_state,
    train_test_split_percentage_in_session_state,
)
from src.session_state.already_pressed_check import (
    already_pressed_based_on_session_state,
)


def show_training_results() -> None:
    """
    Shows training results saved in session_state.
    """
    if sampled_df_in_session_state() and train_test_split_percentage_in_session_state():

        if automl_trainer_in_session_state():
            # show_automl_trainer_info()
            tempdirname = st.session_state.automl_trainer.tempdir.name
            show_report(tempdirname)
            show_logs(tempdirname)
            if not already_pressed_based_on_session_state():
                show_download_button(tempdirname)   # show download button after training is finished


def show_automl_trainer_info() -> None:
    """
    Shows AutoMLTrainer object info.
    """
    if automl_trainer_in_session_state():
        st.experimental_show(st.session_state.automl_trainer.__repr__())


def show_download_button(tempdirname: str) -> None:
    """
    Shows button that allows to download zip file with whole report and all trained models.
    """

    def zip_directory_into_buffer(directory_path: str,) -> None:
        """
        Returns directory zipped into buffer.
        args:
            directory_path: path to the directory to zip
        """
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Iterate over all the files and subdirectories in the directory
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add the file to the zip archive preserving the directory structure
                    zipf.write(file_path, os.path.relpath(file_path, directory_path))
        return buffer
    
    st.download_button(
        "Download data",
        zip_directory_into_buffer(tempdirname).getvalue(),
        f"automl_report_{tempdirname.split('/')[-1]}.zip",
        help="Download data from last experiment (whole report and all trained models)",
    )


def show_logs(tempdirname: str) -> None:
    """
    Shows logs from training in expander.
    args:
        tempdirname: name of temporary directory with training results
    """
    with st.expander("Logs", expanded=True):
        try:
            with open(f"{tempdirname}/{config.LOGS_FILENAME}", "r") as f:
                st.text(f.read())
        except FileNotFoundError:
            st.write("No logs to show")
