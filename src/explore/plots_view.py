import streamlit as st
import time
from src.explore.PlotBuilder import PlotBuilder
from src.explore.buttons_view import show_regenerate_heatmap_button, show_regenerate_pairplot_button
import altair as at
import numpy as np
import pandas as pd
from src import config


# matplotlib and seaborn
def show_heatmap():
    start_time = time.time()
    if "heatmap" not in st.session_state:
        with st.spinner("Generating heatmap"):
            st.session_state.heatmap = PlotBuilder(st.session_state.sampled_df).get_corr_heatmap()
    st.image(st.session_state.heatmap, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")


def show_pairplot():
    start_time = time.time()
    if "pairplot" not in st.session_state:
        with st.spinner("Generating pairplot"):
            st.session_state.pairplot = PlotBuilder(st.session_state.sampled_df).get_pairplot()
    st.image(st.session_state.pairplot, channels="RGB")
    end_time = time.time()
    st.write(f"Showing the above plot took {end_time - start_time:.2f}s")


def show_plots(expanded=False):
    with st.expander("Show correlation heatmap", expanded=expanded):
        show_regenerate_heatmap_button()
        if not st.session_state.sampled_df.empty:
            show_heatmap()

    with st.expander("Show pairplot", expanded=expanded):
        show_regenerate_pairplot_button()
        if not st.session_state.sampled_df.empty:
            show_pairplot()


# altair
def get_binned(df, columns_to_drop):
    def compute_2d_histogram(var1, var2, df, density=True):
        H, xedges, yedges = np.histogram2d(df[var1], df[var2], density=density)
        H[H == 0] = np.nan

        # Create a nice variable that shows the bin boundaries
        xedges = pd.Series(["{0:.4g}".format(num) for num in xedges])
        xedges = pd.DataFrame({"a": xedges.shift(), "b": xedges}).dropna().agg(" - ".join, axis=1)
        yedges = pd.Series(["{0:.4g}".format(num) for num in yedges])
        yedges = pd.DataFrame({"a": yedges.shift(), "b": yedges}).dropna().agg(" - ".join, axis=1)

        # Cast to long format using melt
        res = pd.DataFrame(H, index=yedges, columns=xedges).reset_index().melt(id_vars="index").rename(columns={"index": "value2", "value": "count", "variable": "value"})

        # Also add the raw left boundary of the bin as a column, will be used to sort the axis labels later
        res["raw_left_value"] = res["value"].str.split(" - ").map(lambda x: x[0]).astype(float)
        res["raw_left_value2"] = res["value2"].str.split(" - ").map(lambda x: x[0]).astype(float)
        res["variable"] = var1
        res["variable2"] = var2
        return res.dropna()  # Drop all combinations for which no values where found

    # Use the function for each combination of variables.
    value_columns = df.columns.drop(columns_to_drop)
    data_2dbinned = pd.concat([compute_2d_histogram(var1, var2, df) for var1 in value_columns for var2 in value_columns])
    return data_2dbinned


def get_corr_data(df):
    cor_data = (
        df.corr()
        .stack()
        .reset_index()  # The stacking results in an index on the correlation values, we need the index as normal columns for Altair
        .rename(columns={0: "correlation", "level_0": "variable", "level_1": "variable2"})
    )
    cor_data["correlation_label"] = cor_data["correlation"].map("{:.2f}".format)  # Round to 2 decimal
    return cor_data


def altair_interactive_corr_heatmap(df, data_2dbinned):
    # Define selector
    var_sel_cor = at.selection_single(fields=["variable", "variable2"], clear=False, init={"variable": "mock_col1", "variable2": "mock_col2"})

    cor_data = get_corr_data(df)
    # Define correlation heatmap
    base = at.Chart(cor_data).encode(x="variable2:O", y="variable:O")

    text = base.mark_text().encode(text="correlation_label", color=at.condition(at.datum.correlation > 0.5, at.value("white"), at.value("black")))

    cor_plot = base.mark_rect().encode(color=at.condition(var_sel_cor, at.value("pink"), "correlation:Q")).add_selection(var_sel_cor)

    # Define 2d binned histogram plot
    scat_plot = (
        at.Chart(data_2dbinned)
        .transform_filter(var_sel_cor)
        .mark_rect()
        .encode(
            at.X("value:N", sort=at.EncodingSortField(field="raw_left_value")),
            at.Y("value2:N", sort=at.EncodingSortField(field="raw_left_value2", order="descending")),
            at.Color("count:Q", scale=at.Scale(scheme="blues")),
        )
    )

    # Combine all plots. hconcat plots both side-by-side
    return at.vconcat(
        (cor_plot + text).properties(width=config.ALTAIR_PLOTS_SIZE, height=config.ALTAIR_PLOTS_SIZE), scat_plot.properties(width=config.ALTAIR_PLOTS_SIZE, height=config.ALTAIR_PLOTS_SIZE)
    ).resolve_scale(color="independent")


def generate_interactive_altair_corr_heatmap():
    def get_non_numeric_columns_names(df):
        non_numeric_cols = [col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])]
        return non_numeric_cols

    sampled_df_copy = st.session_state.sampled_df.copy()

    data_2dbinned = get_binned(sampled_df_copy, get_non_numeric_columns_names(sampled_df_copy))
    return altair_interactive_corr_heatmap(sampled_df_copy, data_2dbinned)


def show_altair_plots():
    st.altair_chart(generate_interactive_altair_corr_heatmap())
