import streamlit as st
from supervised.automl import AutoML
from src.modify.target_select_view import show_target_column_selectbox
from src.session_state.session_state_checks import (
    sampled_df_in_session_state,
    train_test_split_percentage_in_session_state,
    explain_zip_buffer_in_session_state,
    redirected_training_output_in_session_state,
    validation_type_in_session_state,
    shuffle_in_session_state,
    stratify_in_session_state,
)
from sklearn.model_selection import train_test_split
import sys
import io
import tempfile
import os
import zipfile
from datetime import datetime
from src.general_views.mljar_markdown_view import show_mljar_markdown
from supervised.exceptions import AutoMLException
from src import config


class OutputRedirector:  # TODO: remove it in prod and lower the verbosity level of AutoML
    def __enter__(self):
        self.original_stdout = sys.stdout
        sys.stdout = self.output_string = io.StringIO()
        return self.output_string

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.original_stdout


def zip_directory_into_buffer(directory_path, buffer):
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Iterate over all the files and subdirectories in the directory
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Add the file to the zip archive preserving the directory structure
                zipf.write(file_path, os.path.relpath(file_path, directory_path))


def simple_target_column_selectbox():
    columns_list = st.session_state.sampled_df.columns.tolist()
    selectbox_default_index = len(columns_list) - 1
    return st.selectbox("Choose target column:", columns_list, index=selectbox_default_index)


def problem_type_selectbox():
    problem_types = ["auto", "binary classification", "multiclass classification", "regression"]
    chosen_problem_type = st.selectbox(
        "Choose problem type", problem_types, index=0, help="You can choose problem type manually or leave it at auto (then problem type will be guessed based on target values)"
    )
    return chosen_problem_type


def metric_selectbox(problem_type):
    if problem_type == "binary classification":
        metrics = ["logloss", "auc", "f1", "average_precision", "accuracy"]
    elif problem_type == "multiclass classification":
        metrics = ["logloss", "f1", "accuracy"]
    elif problem_type == "regression":
        metrics = ["rmse", "mse", "mae", "r2", "mape", "spearman", "pearson"]
    else:  # problem type is auto
        metrics = []

    if metrics:
        return st.selectbox("Choose metric", metrics, index=0, help="Choose evaluation metric.")
    return None


def algorithms_selectbox():
    algorithms = ["Baseline", "Linear", "Decision Tree", "Random Forest", "Xgboost", "Extra Trees", "LightGBM", "CatBoost", "Neural Network", "Nearest Neighbors"]
    return st.multiselect("Choose algorithms to train", algorithms, algorithms[0:5])


def perform_train_test_split(df, target_label, train_size):
    X = df.drop(columns=target_label)
    y = df[target_label]
    return train_test_split(X, y, train_size=train_size)


def perform_X_y_split(df, target_label):
    X = df.drop(columns=target_label)
    y = df[target_label]
    return X, y


def get_shuffle_and_stratify_settings():
    if shuffle_in_session_state() and stratify_in_session_state():
        return st.session_state.shuffle, st.session_state.stratify
    else:
        return True, True


def train_mljar_explain(target_col_name, tmpdirname, problem_type, eval_metric, algorithms, total_time_limit, mode):
    # X_train, X_test, y_train, y_test = perform_train_test_split(st.session_state.sampled_df, target_col_name, st.session_state.train_test_split_percentage)
    X, y = perform_X_y_split(st.session_state.sampled_df, target_col_name)

    shuffle_setting, stratify_setting = get_shuffle_and_stratify_settings()

    if st.session_state.validation_type == "split":
        configured_validation_strategy = {
            "validation_type": "split",
            "train_ratio": st.session_state.train_test_split_percentage,
            "shuffle": shuffle_setting,
            "stratify": stratify_setting,
            "random_seed": config.RANDOM_STATE,
        }
    else:  # validation type is kfold
        configured_validation_strategy = {"validation_type": "kfold", "k_folds": 5, "shuffle": shuffle_setting, "stratify": stratify_setting, "random_seed": config.RANDOM_STATE}

    # create AutoML object
    if problem_type == "auto":
        automl = AutoML(results_path=tmpdirname, mode=mode, ml_task=problem_type, algorithms=algorithms, validation_strategy=configured_validation_strategy, total_time_limit=total_time_limit)
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

    # perform training with redirected stdout
    with OutputRedirector() as output_string:
        automl.fit(X, y)
        st.session_state.redirected_training_output = output_string.getvalue()


def total_time_limit_slider():
    def get_minutes_and_seconds(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return minutes, seconds

    total_time_limit = st.slider("Total time limit (in seconds)", 60, 1800, 150, 15)
    minutes, seconds = get_minutes_and_seconds(total_time_limit)
    st.caption(f"The maximum training time will be {minutes} minutes and {seconds} seconds.")
    return total_time_limit


def mode_selectbox():
    mode = st.selectbox(
        "Choose training mode",
        ["Compete", "Perform", "Explain"],
        help="Compete mode is dedicated for training best models. Explain mode is for generating visualizations (e.g. SHAP plots). Perform mode is something in between.",
    )
    if mode == "Explain" or mode == "Perform":
        st.caption(
            "Note: Visualizations generated for Explain and Perform modes may break if the app is under heavy load. If the app may be used by many users, is is advised to use the Compete mode."
        )
    return mode


def clean_up_directory_from_png_files(tmpdirname):
    """
    Remove all png files for given directory and its subdirectories.
    """
    for root, dirs, files in os.walk(tmpdirname):
        for file in files:
            if file.endswith(".png"):
                os.remove(os.path.join(root, file))


def show_mljar_model():
    if sampled_df_in_session_state() and train_test_split_percentage_in_session_state() and validation_type_in_session_state():
        target_col_name = simple_target_column_selectbox()
        problem_type = problem_type_selectbox()
        metric = metric_selectbox(problem_type)
        algorithms = algorithms_selectbox()
        total_time_limit = total_time_limit_slider()
        mode = mode_selectbox()
        if st.button("Generate new report"):
            try:
                with st.spinner("Generating report..."):
                    with tempfile.TemporaryDirectory() as tmpdirname:
                        # run automl training
                        train_mljar_explain(target_col_name, tmpdirname, problem_type, metric, algorithms, total_time_limit, mode)

                        # clean up directory if the mode is Compete
                        if mode == "Compete":
                            clean_up_directory_from_png_files(tmpdirname)

                        # save dir with results as zip to session_state
                        st.session_state.explain_zip_buffer = io.BytesIO()
                        zip_directory_into_buffer(tmpdirname, st.session_state.explain_zip_buffer)
                st.success("Done! Now you can go to Assess tab to see the results!")
            except AutoMLException as error:
                st.warning("Something went wrong. 😔 Please check if sampled dataframe isn't too small or if train data percentage isn't too high or too low.")
                st.write(error)


def show_mljar_assess():
    if sampled_df_in_session_state() and train_test_split_percentage_in_session_state():
        if explain_zip_buffer_in_session_state():
            # show report
            with st.expander("Report", expanded=True):
                show_mljar_markdown()

            # show logs
            with st.expander("Logs", expanded=False):
                if redirected_training_output_in_session_state():
                    st.text(st.session_state.redirected_training_output)

            # show zip download button
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%H_%M_%S-%d_%m_%Y")
            st.download_button(
                "Download data",
                st.session_state.explain_zip_buffer.getvalue(),
                f"automl_report-{formatted_datetime}.zip",
                help="Download data from last experiment (whole report and all trained models)",
            )
