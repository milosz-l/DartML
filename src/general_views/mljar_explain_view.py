import streamlit as st
from supervised.automl import AutoML
from src.modify.target_select_view import show_target_column_selectbox
from src.session_state.session_state_checks import (
    sampled_df_in_session_state,
    train_test_split_percentage_in_session_state,
    explain_zip_buffer_in_session_state,
    redirected_training_output_in_session_state,
)
from sklearn.model_selection import train_test_split
import sys
import io
import tempfile
import os
import zipfile
from datetime import datetime
from src.general_views.mljar_markdown_view import show_mljar_markdown
from src.config import X_TEST_DF_FILENAME, Y_TEST_DF_FILENAME, TEST_PREDICTIONS_FILENAME
import pandas as pd


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
    if train_size < 1:
        return train_test_split(X, y, train_size=train_size)
    else:  # when train_size is 100%
        return X, None, y, None


def train_mljar_explain(target_col_name, tmpdirname, problem_type, eval_metric, algorithms):
    # split data into train and test
    X_train, X_test, y_train, y_test = perform_train_test_split(st.session_state.sampled_df, target_col_name, st.session_state.train_test_split_percentage)

    # create AutoML object
    if problem_type == "auto":
        automl = AutoML(results_path=tmpdirname, mode="Explain", ml_task=problem_type, algorithms=algorithms)
    else:
        problem_type = problem_type.replace(" ", "_")
        automl = AutoML(results_path=tmpdirname, mode="Explain", ml_task=problem_type, algorithms=algorithms, eval_metric=eval_metric)

    # perform training with redirected stdout
    with OutputRedirector() as output_string:
        # perform training
        automl.fit(X_train, y_train)

        # save predictions
        if X_test is not None:
            predictions = automl.predict(X_test)
            predictions_df = pd.DataFrame(predictions, columns=[f"{automl._ml_task}-predictions"])
            predictions_df.to_csv(f"{tmpdirname}/{TEST_PREDICTIONS_FILENAME}", index=False)

        # save redirected logs to session_state
        st.session_state.redirected_training_output = output_string.getvalue()

    return X_test, y_test


def save_test_data_to_dir(X_test, y_test, path):
    X_test.to_csv(f"{path}/{X_TEST_DF_FILENAME}", index=False)
    y_test.to_csv(f"{path}/{Y_TEST_DF_FILENAME}", index=False)


def show_mljar_model():
    if sampled_df_in_session_state() and train_test_split_percentage_in_session_state():
        target_col_name = simple_target_column_selectbox()
        problem_type = problem_type_selectbox()
        metric = metric_selectbox(problem_type)
        algorithms = algorithms_selectbox()
        if st.button("Generate new report"):
            with st.spinner("Generating report..."):
                with tempfile.TemporaryDirectory() as tmpdirname:
                    # run automl training
                    X_test, y_test = train_mljar_explain(target_col_name, tmpdirname, problem_type, metric, algorithms)

                    # save test predictions to directory with results
                    if X_test is not None and y_test is not None:
                        save_test_data_to_dir(X_test, y_test, tmpdirname)

                    # save dir with results as zip to session_state
                    st.session_state.explain_zip_buffer = io.BytesIO()
                    zip_directory_into_buffer(tmpdirname, st.session_state.explain_zip_buffer)

            st.success("Done! Now you can go to Assess tab to see the results!")


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
