import pandas as pd

from src.explore.plots_view import generate_interactive_altair_corr_heatmap


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
