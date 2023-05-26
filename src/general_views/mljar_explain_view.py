import streamlit as st
from supervised.automl import AutoML
from src.modify.target_select_view import show_target_column_selectbox
from src.session_state.session_state_checks import sampled_df_in_session_state, train_test_split_percentage_in_session_state, explain_zip_buffer_in_session_state
from sklearn.model_selection import train_test_split
import sys
import io
import tempfile
import os
import zipfile


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


def perform_train_test_split(df, target_label, train_size):
    X = df.drop(columns=target_label)
    y = df[target_label]
    return train_test_split(X, y, train_size=train_size)


def show_mljar_explain():
    if sampled_df_in_session_state() and train_test_split_percentage_in_session_state():
        with st.form("EDA_form"):
            target_col_name = simple_target_column_selectbox()
            submitted = st.form_submit_button("Generate report")
            if submitted:
                with st.spinner("Generating report..."):
                    with tempfile.TemporaryDirectory() as tmpdirname:
                        X_train, X_test, y_train, y_test = perform_train_test_split(st.session_state.sampled_df, target_col_name, st.session_state.train_test_split_percentage)
                        automl = AutoML(results_path=tmpdirname, mode="Explain")

                        with OutputRedirector() as output_string:
                            automl.fit(X_train, y_train)

                            with st.expander("Report", expanded=True):
                                with open(f"{tmpdirname}/README.md", "r") as report_file:
                                    st.markdown(report_file.read())
                                    # TODO: issue number 4336

                            with st.expander("Logs", expanded=False):
                                st.text(output_string.getvalue())

                        with st.expander("Predictions for test data", expanded=False):
                            predictions = automl.predict(X_test)
                            st.write(predictions)

                        # save dir as zip to session_state
                        st.session_state.explain_zip_buffer = io.BytesIO()
                        zip_directory_into_buffer(tmpdirname, st.session_state.explain_zip_buffer)

        st.success("Done!")
        if explain_zip_buffer_in_session_state():
            st.download_button("Download report zip file", st.session_state.explain_zip_buffer.getvalue(), "automl_report.zip")
        # TODO: show results
