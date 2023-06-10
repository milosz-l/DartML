from datetime import datetime

import streamlit as st

from src.assess.report_view import show_report
from src.session_state.session_state_checks import (
    automl_trainer_in_session_state,
    explain_zip_buffer_in_session_state,
    redirected_training_output_in_session_state,
    sampled_df_in_session_state,
    train_test_split_percentage_in_session_state,
)


def show_training_results() -> None:
    """
    Shows training results saved in session_state.
    """
    if sampled_df_in_session_state() and train_test_split_percentage_in_session_state():
        # if explain_zip_buffer_in_session_state():
        #     show_report()
        #     show_logs()
        #     show_zip_download_button()
        
        if automl_trainer_in_session_state():
            show_automl_trainer_info()
            tempdirname = st.session_state.automl_trainer.tempdir.name
            show_report(tempdirname)
            # show_logs()   # TODO
            # show_download_button()    # TODO


def show_automl_trainer_info() -> None:
    """
    Shows AutoMLTrainer object info.
    """
    if automl_trainer_in_session_state():
        st.experimental_show(st.session_state.automl_trainer.__repr__())


def show_zip_download_button() -> None:
    """
    Shows button that allows to download zip file with whole report and all trained models.
    """
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%H_%M_%S-%d_%m_%Y")
    st.download_button(
        "Download data",
        st.session_state.explain_zip_buffer.getvalue(),
        f"automl_report-{formatted_datetime}.zip",
        help="Download data from last experiment (whole report and all trained models)",
    )


def show_logs() -> None:
    """
    Shows logs from training in expander.
    """
    with st.expander("Logs", expanded=False):
        if redirected_training_output_in_session_state():
            if st.session_state.redirected_training_output is not None:
                st.text(st.session_state.redirected_training_output)
