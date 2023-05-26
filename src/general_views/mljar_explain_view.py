import streamlit as st
from supervised.automl import AutoML
from src.modify.target_select_view import show_target_column_selectbox
from src.session_state.session_state_checks import sampled_df_in_session_state, train_test_split_percentage_in_session_state
from sklearn.model_selection import train_test_split
import sys
import io


class OutputRedirector:
    def __enter__(self):
        self.original_stdout = sys.stdout
        sys.stdout = self.output_string = io.StringIO()
        return self.output_string

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.original_stdout


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
                    X_train, X_test, y_train, y_test = perform_train_test_split(st.session_state.sampled_df, target_col_name, st.session_state.train_test_split_percentage)
                    automl = AutoML(mode="Explain")  # TODO: custom filename

                    output_string = io.StringIO()
                    # with open("output.txt", "w") as sys.stdout:  # TODO: redirect output to buffer and print it
                    # with output_string as sys.stdout:
                    with OutputRedirector() as output_string:
                        st.text(output_string.getvalue())
                        automl.fit(X_train, y_train)

                        predictions = automl.predict(X_test)
                        st.write(predictions)
                st.success("Done!")
                with st.expander("Logs", expanded=False):
                    st.text(output_string.getvalue())
                # TODO: show results

    # TODO: choose target column
