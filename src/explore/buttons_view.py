import streamlit as st


def show_regenerate_heatmap_button() -> None:
    """
    Shows a button that allows to regenerate the heatmap.
    """
    if st.button(
        "Regenerate heatmap",
        help="You've just uploaded a new dataframe and the plot didn't change? Then click this button!",
    ):
        if "heatmap" in st.session_state:
            del st.session_state.heatmap


def show_regenerate_pairplot_button() -> None:
    """
    Shows a button that allows to regenerate the pairplot.
    """
    if st.button(
        "Regenerate pairplot",
        help="You've just uploaded a new dataframe and the plot didn't change? Then click this button!",
    ):
        if "pairplot" in st.session_state:
            del st.session_state.pairplot
