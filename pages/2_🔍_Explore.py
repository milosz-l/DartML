import streamlit as st
from src.general_views.df_view import show_sampled_df
from src.general_views.sidebars_view import show_info_sidebar
from src.session_state.session_state_checks import sampled_df_in_session_state
from src.explore.plots_view import show_plots, show_altair_plot
from src.general_views.logo import show_logo
from src import config

st.set_page_config(page_title="AutoML", page_icon=config.APP_FAVICON, layout="wide")

show_logo()
st.title("🔍 Explore")

if not sampled_df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar()
    show_sampled_df()

    st.divider()

    show_altair_plot(show_time=True)

    # show_plots(expanded=True)
