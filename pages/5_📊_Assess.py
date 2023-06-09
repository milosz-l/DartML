import streamlit as st

from src import config
from src.assess.assess_view import show_training_results
from src.general_views.df_view import show_sampled_df
from src.general_views.logo import show_logo
from src.general_views.pages_explanations_view import show_page_explanation_in_expander
from src.general_views.sidebars_view import show_info_sidebar
from src.session_state.session_state_checks import sampled_df_in_session_state

st.set_page_config(
    page_title=config.APP_TITLE, page_icon=config.APP_FAVICON, layout="wide"
)

show_logo()
st.title(config.ASSESS_PAGE_TITLE)
show_page_explanation_in_expander("assess")

if not sampled_df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar()
    show_sampled_df()
    show_training_results()
