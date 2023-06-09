import streamlit as st

from src import config
from src.general_views.logo import show_logo
from src.general_views.pages_explanations_view import (
    show_home_page_explanation,
    show_page_explanation_in_expander,
)

st.set_page_config(
    page_title=config.APP_TITLE, page_icon=config.APP_FAVICON, layout="centered"
)

show_logo()
st.title(config.HOME_PAGE_TITLE)
show_home_page_explanation()

st.subheader(config.SAMPLE_PAGE_TITLE_WITH_COLOR)
show_page_explanation_in_expander("sample", expanded=True)

st.subheader(config.EXPLORE_PAGE_TITLE_WITH_COLOR)
show_page_explanation_in_expander("explore", expanded=True)

st.subheader(config.MODIFY_AND_MODEL_PAGE_TITLE_WITH_COLOR)
show_page_explanation_in_expander("modify_and_model", expanded=True)

st.subheader(config.ASSESS_PAGE_TITLE_WITH_COLOR)
show_page_explanation_in_expander("assess", expanded=True)
