import streamlit as st
import pandas as pd
from PIL import Image
import zipfile
import io
from src.session_state.session_state_checks import explain_zip_buffer_in_session_state
from src.config import X_TEST_DF_FILENAME, Y_TEST_DF_FILENAME, TEST_PREDICTIONS_FILENAME
from src.utils.metrics import calculate_binary_classification_metrics, calculate_multiclass_classification_metrics, calculate_regression_metrics


def show_image_from_path(path, header="", caption=""):
    try:
        image = Image.open(path)
        if header:
            st.markdown(f"### {header}")
        st.image(image, caption=caption)
    except FileNotFoundError:
        pass


def show_image_from_archive(archive, filename, header="", caption=""):
    try:
        img_bytes = archive.read(filename)
        if header:
            st.markdown(header)
        st.image(img_bytes, caption=caption)
    except KeyError:
        pass  # there is no such item in the archive


def get_df_from_csv_in_archive(archive, filename):
    try:
        csv_bytes = archive.read(filename)
        csv_io = io.BytesIO(csv_bytes)
        df = pd.read_csv(csv_io)
        return df
    except KeyError:
        return None  # there is no such item in the archive


def show_csv_from_archive(archive, filename, header=""):
    try:
        df = get_df_from_csv_in_archive(archive, filename)
        if header:
            st.markdown(header)
        st.write(df)
    except KeyError:
        pass  # there is no such item in the archive


def show_tabs():
    pass  # TODO


# def test_data_results_exist(archive):
#     def file_exists(archive, file_name):
#         try:
#             archive.read(file_name)
#         except KeyError:
#             return False    # there is no such item in the archive
#         return True

#     file_names = [X_TEST_DF_FILENAME, Y_TEST_DF_FILENAME, TEST_PREDICTIONS_FILENAME]
#     for file_name in file_names:
#         if not file_exists(archive, file_name):
#             return False
#     return True


def show_test_data_results(archive, header=""):
    try:
        X_test = get_df_from_csv_in_archive(archive, X_TEST_DF_FILENAME)
        y_test = get_df_from_csv_in_archive(archive, Y_TEST_DF_FILENAME)
        predictions = get_df_from_csv_in_archive(archive, TEST_PREDICTIONS_FILENAME)
        combined_df = pd.concat([X_test, y_test, predictions], axis=1)

        # extract problem type from predictions column name
        ml_task = predictions.columns[0].split("-")[0]
        metrics_functions = {
            "binary_classification": calculate_binary_classification_metrics,
            "multiclass_classification": calculate_multiclass_classification_metrics,
            "regression": calculate_regression_metrics,
        }
        metrics_function = metrics_functions[ml_task]

        if header:
            st.markdown(header)
        try:
            st.write(metrics_function(y_test, predictions))
        except ValueError as error:
            st.warning("ValueError occured during generating test data results:")
            st.write(error)
        st.write(combined_df)
    except KeyError:
        pass  # there is no such item in the archive


def show_mljar_markdown():
    if explain_zip_buffer_in_session_state():
        # get access to zipped archive saved in session_state
        archive = zipfile.ZipFile(st.session_state.explain_zip_buffer, "r")

        # show leaderboard
        show_csv_from_archive(archive, "leaderboard.csv", header="# AutoML Leaderboard")

        # show images
        show_image_from_archive(archive, "ldb_performance.png", header="### AutoML Performance")
        show_image_from_archive(archive, "ldb_performance_boxplot.png", header="### AutoML Performance Boxplot")
        show_image_from_archive(archive, "features_heatmap.png", header="### Features Importance")
        show_image_from_archive(archive, "correlation_heatmap.png", header="### Spearman Correlation of Models")

        show_tabs()

        # show test data results
        show_test_data_results(archive, header="### Test data results")
