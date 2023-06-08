import streamlit as st
from src.general_views.df_view import show_sampled_df
from src.general_views.sidebars_view import show_info_sidebar
from src.session_state.session_state_checks import sampled_df_in_session_state
from src.explore.plots_view import show_plots, show_numerical_columns_visualizations, show_categorical_columns_visualizations
from src.general_views.logo import show_logo
from src import config
from src.general_views.pages_explanations_view import show_page_explanation_in_expander

st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_FAVICON, layout="wide")

show_logo()
st.title(config.EXPLORE_PAGE_TITLE)
show_page_explanation_in_expander("explore")

if not sampled_df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar()
    show_sampled_df()
    st.divider()

    st.markdown("### Numerical columns")
    show_numerical_columns_visualizations(show_time=False)

    # show_plots(expanded=True)

    st.markdown("### Categorical columns")
    show_categorical_columns_visualizations()
