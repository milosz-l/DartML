import time
from typing import Literal, Optional

import streamlit as st
from supervised.exceptions import AutoMLException

from src import config
from src.modify_and_model.AutoMLTrainer import AutoMLTrainer
from src.session_state.already_pressed_check import (
    already_pressed_based_on_session_state,
)
from src.session_state.session_state_checks import (
    automl_trainer_in_session_state,
    sampled_df_in_session_state,
    shuffle_in_session_state,
    split_type_in_session_state,
    stratify_in_session_state,
    train_test_split_percentage_in_session_state,
)


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

    total_time_limit = st.slider(
        "Total time limit (in seconds)",
        config.TRAINING_MIN,
        config.TRAINING_MAX,
        config.TRAINING_MIN,
        15,
    )
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
    return mode


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


def get_shuffle_and_stratify_settings() -> tuple[bool, bool]:
    """
    Returns shuffle and stratify settings from session state.
    """
    if shuffle_in_session_state() and stratify_in_session_state():
        return st.session_state.shuffle, st.session_state.stratify
    else:
        return True, True


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
        eval_metric = metric_selectbox(problem_type)
        st.divider()

        algorithms = algorithms_selectbox()
        st.divider()

        total_time_limit = total_time_limit_slider()
        st.divider()

        mode = mode_selectbox()
        st.divider()

        shuffle, stratify = get_shuffle_and_stratify_settings()

        if automl_trainer_in_session_state():
            st.warning(
                "⚠️ You have already clicked the **_Generate new report_** button. Clicking it again will override the report currently available in the 📊 **Assess** tab!"
            )

        if st.button(
            "Generate new report",
            disabled=already_pressed_based_on_session_state(),
            help="If the button is disabled, please wait until the previous training is finished.",
            type="primary",
        ):
            if not already_pressed_based_on_session_state():
                try:
                    with st.spinner(""):
                        # clicking the button creates new AutoMLTrainer object, which replaces the old one (if there was any)
                        st.session_state.automl_trainer = AutoMLTrainer(
                            st.session_state.sampled_df,
                            target_col_name,
                            problem_type,
                            eval_metric,
                            algorithms,
                            total_time_limit,
                            mode,
                            shuffle,
                            stratify,
                            st.session_state.split_type,
                            st.session_state.train_test_split_percentage,
                        )

                        # run automl training
                        st.session_state.training_time_start = time.time()
                        st.write(
                            "Training is in progress. Now go to the 📊 **Assess** tab to see the results in real time!"
                        )
                        st.session_state.automl_trainer.train()

                except AutoMLException as error:
                    st.warning(
                        "Something went wrong. 😔 Please check if sampled dataframe isn't too small or if train data percentage isn't too high or too low."
                    )
                    st.write(error)
