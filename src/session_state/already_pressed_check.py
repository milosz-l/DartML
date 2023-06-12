import time

import streamlit as st

from src import config


def already_pressed_based_on_session_state() -> bool:
    """
    Returns whether `Generate new report` button has been pressed within the time limit + overhead.
    """
    try:
        return already_pressed(
            current_time=time.time(),
            training_time_start=st.session_state.training_time_start,
            total_time_limit=st.session_state.automl_trainer.total_time_limit,
            overhead=config.ASSESS_REFRESH_OVERHEAD,
        )
    except AttributeError:
        return False


def already_pressed(
    current_time: int, training_time_start: int, total_time_limit: int, overhead: int
) -> bool:
    """
    Returns whether `Generate new report` button has been pressed within the time limit + overhead.
    """
    return current_time - training_time_start < total_time_limit + overhead
