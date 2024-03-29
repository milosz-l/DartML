import time

import altair as at
import numpy as np
import pandas as pd
import streamlit as st

from src import config
from src.explore.buttons_view import (
    show_regenerate_heatmap_button,
    show_regenerate_pairplot_button,
)
from src.explore.PlotBuilder import PlotBuilder


# matplotlib and seaborn
def show_heatmap() -> None:
    """
    Shows the correlation heatmap.
    """
    start_time = time.time()
    if "heatmap" not in st.session_state:
        with st.spinner("Generating heatmap"):
            st.session_state.heatmap = PlotBuilder(
                st.session_state.sampled_df
            ).get_corr_heatmap()
    st.image(st.session_state.heatmap, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")


def show_pairplot() -> None:
    """
    Shows the pairplot.
    """
    start_time = time.time()
    if "pairplot" not in st.session_state:
        with st.spinner("Generating pairplot"):
            st.session_state.pairplot = PlotBuilder(
                st.session_state.sampled_df
            ).get_pairplot()
    st.image(st.session_state.pairplot, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")


def show_plots(expanded: bool = False) -> None:
    """
    Shows the matplotlib and seaborn plots (correlation heatmap and pairplot).
    """
    with st.expander("Show correlation heatmap", expanded=expanded):
        show_regenerate_heatmap_button()
        if not st.session_state.sampled_df.empty:
            show_heatmap()

    with st.expander("Show pairplot", expanded=expanded):
        show_regenerate_pairplot_button()
        if not st.session_state.sampled_df.empty:
            show_pairplot()


# altair
## numerical columns visualizations
def compute_2d_binned_histogram(
    var1: str, var2: str, df: pd.DataFrame, density: bool = True
) -> pd.DataFrame:
    """
    Returns a dataframe with the 2d binned histogram for the given combination of the numerical columns.
    """
    # compute the 2d binned histogram of two given columns
    H, xedges, yedges = np.histogram2d(df[var1], df[var2], density=density)
    H[H == 0] = np.nan  # later it will allow to get rid of empty rows

    # generate bin boundaries
    xedges = pd.Series(["{0:.4g}".format(num) for num in xedges])
    xedges = (
        pd.DataFrame({"a": xedges.shift(), "b": xedges})
        .dropna()
        .agg(" - ".join, axis=1)
    )
    yedges = pd.Series(["{0:.4g}".format(num) for num in yedges])
    yedges = (
        pd.DataFrame({"a": yedges.shift(), "b": yedges})
        .dropna()
        .agg(" - ".join, axis=1)
    )

    # unpivot - cast from wide to long format using melt
    histogram = (
        pd.DataFrame(H, index=yedges, columns=xedges)
        .reset_index()
        .melt(id_vars="index")
        .rename(columns={"index": "value2", "value": "count", "variable": "value"})
    )

    # add the raw left boundary of the bin as a column, will be used to sort the axis labels later
    histogram["raw_left_value"] = (
        histogram["value"].str.split(" - ").map(lambda x: x[0]).astype(float)
    )
    histogram["raw_left_value2"] = (
        histogram["value2"].str.split(" - ").map(lambda x: x[0]).astype(float)
    )
    histogram["variable"] = var1
    histogram["variable2"] = var2
    return histogram.dropna()  # drop all combinations for which no values where found


def transform_df_to_2d_binned_histograms(
    df: pd.DataFrame, columns_to_drop: list[str]
) -> pd.DataFrame:
    """
    Returns a dataframe with the 2d binned histograms for all the combinations of the numerical columns.
    args:
        df: the dataframe with data (and all columns - both numerical and categorical)
        columns_to_drop: list of the columns to drop (categorical columns)
    """
    numerical_columns = df.columns.drop(columns_to_drop)
    df_as_2d_binned_histograms = pd.concat(
        [
            compute_2d_binned_histogram(var1, var2, df)
            for var1 in numerical_columns
            for var2 in numerical_columns
        ]
    )
    return df_as_2d_binned_histograms


def compute_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a dataframe with the correlations between all the numerical columns.
    args:
        df: the dataframe
    """
    correlations = (
        df.corr()
        .stack()
        .reset_index()
        .rename(
            columns={0: "correlation", "level_0": "variable", "level_1": "variable2"}
        )
    )
    correlations["correlation_label"] = correlations["correlation"].map("{:.2f}".format)
    return correlations


def altair_interactive_corr_heatmap(
    df: pd.DataFrame, df_as_2d_binned_histograms: pd.DataFrame
) -> None:
    """
    Returns an interactive correlation heatmap.
    args:
        df: the dataframe
        df_as_2d_binned_histograms: 2d binned histograms data
    """
    # based on https://towardsdatascience.com/altair-plot-deconstruction-visualizing-the-correlation-structure-of-weather-data-38fb5668c5b1

    # correlation heatmap
    correlations = compute_correlations(df)
    base = at.Chart(correlations).encode(x="variable2:O", y="variable:O")

    # labels for correlation heatmap
    text = base.mark_text().encode(
        text="correlation_label",
        color=at.condition(
            at.datum.correlation > 0.5, at.value("white"), at.value("black")
        ),
    )

    # selector
    var_sel_cor = at.selection_single(
        fields=["variable", "variable2"],
        clear=False,
        init={"variable": "mock_col1", "variable2": "mock_col2"},
    )

    # correlation heatmap with selector
    cor_plot = (
        base.mark_rect()
        .encode(color=at.condition(var_sel_cor, at.value("pink"), "correlation:Q"))
        .add_selection(var_sel_cor)
    )

    # 2d binned histogram plot
    scat_plot = (
        at.Chart(df_as_2d_binned_histograms)
        .transform_filter(var_sel_cor)
        .mark_rect()
        .encode(
            at.X("value:N", sort=at.EncodingSortField(field="raw_left_value")),
            at.Y(
                "value2:N",
                sort=at.EncodingSortField(field="raw_left_value2", order="descending"),
            ),
            at.Color("count:Q", scale=at.Scale(scheme="blues")),
        )
    )

    # combine all plots vertically
    return at.vconcat(
        (cor_plot + text).properties(
            width=config.ALTAIR_PLOTS_WIDTH, height=config.ALTAIR_PLOTS_HEIGHT
        ),
        scat_plot.properties(
            width=config.ALTAIR_PLOTS_WIDTH, height=config.ALTAIR_PLOTS_HEIGHT
        ),
    ).resolve_scale(color="independent")


@st.cache_data
def generate_interactive_altair_corr_heatmap(df: pd.DataFrame) -> at.Chart:
    """
    Generates the interactive altair plot.
    args:
        df: the dataframe to use
    """

    def get_non_numeric_columns_names(df):
        non_numeric_cols = [
            col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])
        ]
        return non_numeric_cols

    df_as_2d_binned_histograms = transform_df_to_2d_binned_histograms(
        df=df, columns_to_drop=get_non_numeric_columns_names(df)
    )
    return altair_interactive_corr_heatmap(df, df_as_2d_binned_histograms)


def show_numerical_columns_visualizations(show_time: bool = False) -> None:
    """
    Shows the interactive altair plot.
    args:
        show_time: whether to show the time it took to generate the plot
    """
    start_time = time.time()
    df = st.session_state.sampled_df
    st.altair_chart(
        generate_interactive_altair_corr_heatmap(df), use_container_width=False
    )
    end_time = time.time()
    if show_time:
        st.write(f"Showing the above plot took {end_time - start_time:.2f}s")


## categorical columns visualizations
@st.cache_data
def generate_categorical_columns_visualizations(df: pd.DataFrame) -> list[at.Chart]:
    """
    Generates bar charts for each categorical column in the dataframe.
    Returns a list of Altair charts.
    args:
        df: dataframe to generate the plots for
    """
    categorical_columns = df.select_dtypes(include=["object"]).columns

    charts = []

    # create bar charts for each categorical column
    for column in categorical_columns:
        # count the occurrences of each unique value
        value_counts = df[column].value_counts().reset_index()
        value_counts.columns = [column, "Count"]

        # create the bar chart using Altair
        chart = (
            at.Chart(value_counts)
            .mark_bar()
            .encode(x=column, y="Count")
            .properties(title=f"Bar Chart - {column}", width=config.ALTAIR_PLOTS_WIDTH)
        )

        # append created chart to the list of charts
        charts.append(chart)
    return charts


def show_categorical_columns_visualizations(show_time: bool = False) -> None:
    """
    Show bar charts for each categorical column in the dataframe.
    args:
        show_time: if True, show the time it took to generate the plots
    """
    start_time = time.time()
    df = st.session_state.sampled_df
    charts = generate_categorical_columns_visualizations(df)
    end_time = time.time()
    for chart in charts:
        st.altair_chart(chart, use_container_width=False)
    if show_time:
        st.write(f"Showing the above plots took {end_time - start_time:.2f}s")
