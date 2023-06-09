import io
import sys
from typing import Literal

import pandas as pd
import streamlit as st
from supervised.automl import AutoML

from src import config
from src.session_state.session_state_checks import (
    shuffle_in_session_state,
    stratify_in_session_state,
)


class OutputRedirector:
    """
    Class used to redirect the output of the training process to a string.
    """

    def __enter__(self):
        self.original_stdout = sys.stdout
        sys.stdout = self.output_string = io.StringIO()
        return self.output_string

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.original_stdout


def perform_X_y_split(df: pd.DataFrame, target_label: str):
    """
    Performs X y split on given dataframe.
    args:
        df: dataframe to split
        target_label: name of the target column
    """
    X = df.drop(columns=target_label)
    y = df[target_label]
    return X, y


def get_shuffle_and_stratify_settings() -> tuple[bool, bool]:
    """
    Returns shuffle and stratify settings from session state.
    """
    if shuffle_in_session_state() and stratify_in_session_state():
        return st.session_state.shuffle, st.session_state.stratify
    else:
        return True, True


def train_automl(
    target_col_name: str,
    tmpdirname: str,
    problem_type: Literal[
        "binary classification", "multiclass classification", "regression", "auto"
    ],
    eval_metric: str,
    algorithms: list[str],
    total_time_limit: int,
    mode: Literal["Explain", "Perform", "Compete"],
    redirect_logs: bool,
) -> None:
    """
    Trains AutoML model.
    args:
        target_col_name: name of the target column
        tmpdirname: path to the temporary directory, where all the results are saved
        problem_type: problem type
        eval_metric: evaluation metric
        algorithms: list of algorithms to train
        total_time_limit: total time limit for training in seconds
        mode: mode of training
        redirect_logs: whether to redirect logs to a string
    """
    X, y = perform_X_y_split(st.session_state.sampled_df, target_col_name)

    shuffle_setting, stratify_setting = get_shuffle_and_stratify_settings()

    if st.session_state.split_type == "split":
        configured_validation_strategy = {
            "validation_type": "split",
            "train_ratio": st.session_state.train_test_split_percentage,
            "shuffle": shuffle_setting,
            "stratify": stratify_setting,
            "random_seed": config.RANDOM_STATE,
        }
    else:  # validation type is kfold
        configured_validation_strategy = {
            "validation_type": "kfold",
            "k_folds": 5,
            "shuffle": shuffle_setting,
            "stratify": stratify_setting,
            "random_seed": config.RANDOM_STATE,
        }

    # create AutoML object
    if problem_type == "auto":
        automl = AutoML(
            results_path=tmpdirname,
            mode=mode,
            ml_task=problem_type,
            algorithms=algorithms,
            validation_strategy=configured_validation_strategy,
            total_time_limit=total_time_limit,
        )
    else:
        problem_type = problem_type.replace(" ", "_")
        automl = AutoML(
            results_path=tmpdirname,
            mode=mode,
            ml_task=problem_type,
            algorithms=algorithms,
            validation_strategy=configured_validation_strategy,
            total_time_limit=total_time_limit,
            eval_metric=eval_metric,
        )

    if redirect_logs:  # perform training with logs redirected to string
        with OutputRedirector() as output_string:
            automl.fit(X, y)
            st.session_state.redirected_training_output = output_string.getvalue()
    else:  # perform training without redirecting logs
        automl.fit(X, y)
        st.session_state.redirected_training_output = None
