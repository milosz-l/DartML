import os

import pandas as pd
from pandas.testing import assert_frame_equal

from src.explore.plots_view import (
    compute_2d_binned_histogram,
    compute_correlations,
    generate_interactive_altair_corr_heatmap,
    transform_df_to_2d_binned_histograms,
)

UNIT_TESTS_EXPECTED_DATA_PATH = os.path.join("tests", "unit_tests", "expected_data")


def test_df_after_generating_altair_plot_is_the_same():
    """
    Test if DataFrame is the same after generating altair plot
    """
    # create df with both numerical and categorical columns
    starting_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": ["a", "b", "c"]})
    expected_df = starting_df.copy()

    # generate altair plot
    generate_interactive_altair_corr_heatmap(starting_df)

    # check if df is the same
    assert starting_df.equals(expected_df)


def test_compute_2d_binned_histogram():
    """
    Test whether function compute_2d_binned_histogram works as expected on an example DataFrame.
    """
    example_df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4, 10, 10],
            "b": [1, 1, 1, 4, 4, 10],
        }
    )
    expected_df = pd.read_csv(
        os.path.join(
            UNIT_TESTS_EXPECTED_DATA_PATH,
            "expected_test_compute_2d_binned_histogram.csv",
        ),
        index_col=0,
    )
    actual_df = compute_2d_binned_histogram(
        var1="a", var2="b", df=example_df, density=True
    )
    assert_frame_equal(actual_df, expected_df)


def test_transform_df_to_2d_binned_histograms():
    """
    Test whether function transform_df_to_2d_binned_histograms works as expected on an example DataFrame.
    """
    example_df = pd.DataFrame(
        {
            "a": [1, 2],
            "b": [1, 1],
            "c": [2, 3],
            "text_col": ["text1", "text2"],
        }
    )
    expected_df = pd.read_csv(
        os.path.join(
            UNIT_TESTS_EXPECTED_DATA_PATH,
            "expected_test_transform_df_to_2d_binned_histograms.csv",
        ),
        index_col=0,
    )

    actual_df = transform_df_to_2d_binned_histograms(
        df=example_df, columns_to_drop=["text_col"]
    )
    assert_frame_equal(actual_df, expected_df)


def test_compute_correlations():
    """
    Test whether function compute_correlations works as expected on an example DataFrame.
    """
    example_df = pd.DataFrame(
        {
            "a": [1, 2, 5, 6, 7, 8],
            "b": [1, 1, 0, 0, 0, 0],
            "c": [2, 3, 4, 5, 6, 7],
            "d": [10, 9, 8, 7, 6, 5],
            "text_col": ["text1", "text2", "text3", "text4", "text5", "text6"],
        }
    )
    expected_df = pd.read_csv(
        os.path.join(
            UNIT_TESTS_EXPECTED_DATA_PATH, "expected_test_compute_correlations.csv"
        ),
        index_col=0,
    )
    actual_df = compute_correlations(df=example_df)
    actual_df["correlation_label"] = actual_df["correlation_label"].astype("float64")
    assert_frame_equal(actual_df, expected_df)
