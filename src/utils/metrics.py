from sklearn.metrics import log_loss, roc_auc_score, f1_score, average_precision_score, accuracy_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
from sklearn.preprocessing import OrdinalEncoder


import streamlit as st


def perform_label_encoding(y_test, predictions):
    ordinal_encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1, encoded_missing_value=-1)

    target_column_name = y_test.columns[0]
    y_test = y_test.to_numpy()
    # y_test[0] = "nyan"
    predictions = predictions.to_numpy()
    st.experimental_show(y_test)
    st.experimental_show(type(y_test))
    st.experimental_show(predictions)
    st.experimental_show(type(predictions))

    # fit ordinal encoder on uploaded data
    ordinal_encoder.fit(st.session_state.df[target_column_name].to_numpy().reshape(-1, 1))

    y_test_encoded = ordinal_encoder.transform(y_test)
    predictions_encoded = ordinal_encoder.transform(predictions)

    return y_test_encoded, predictions_encoded


def calculate_binary_classification_metrics(y_test, predictions):
    y_test_encoded, predictions_encoded = perform_label_encoding(y_test, predictions)

    metrics = {}
    metrics["logloss"] = log_loss(y_test_encoded, predictions_encoded)
    metrics["auc"] = roc_auc_score(y_test_encoded, predictions_encoded)
    metrics["f1"] = f1_score(y_test_encoded, predictions_encoded)
    metrics["average_precision"] = average_precision_score(y_test_encoded, predictions_encoded)
    metrics["accuracy"] = accuracy_score(y_test_encoded, predictions_encoded)

    return metrics


def calculate_multiclass_classification_metrics(y_test, predictions):
    y_test_encoded, predictions_encoded = perform_label_encoding(y_test, predictions)

    metrics = {}
    metrics["logloss"] = log_loss(y_test_encoded, predictions_encoded)
    metrics["f1"] = f1_score(y_test_encoded, predictions_encoded, average="weighted")
    metrics["accuracy"] = accuracy_score(y_test_encoded, predictions_encoded)

    return metrics


def calculate_regression_metrics(y_test, predictions):
    y_test_np = y_test.to_numpy()
    predictions_np = predictions.to_numpy()

    metrics = {}
    metrics["rmse"] = np.sqrt(mean_squared_error(y_test_np, predictions_np))
    metrics["mse"] = mean_squared_error(y_test_np, predictions_np)
    metrics["mae"] = mean_absolute_error(y_test_np, predictions_np)
    metrics["r2"] = r2_score(y_test_np, predictions_np)
    metrics["mape"] = np.mean(np.abs((y_test_np - predictions_np) / y_test_np)) * 100

    return metrics
