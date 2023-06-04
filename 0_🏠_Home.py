import streamlit as st
from PIL import Image
from src.general_views.logo import show_logo
from src.general_views.pages_explanations_view import show_page_explanation_in_expander
from src import config

st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_FAVICON, layout="centered")

show_logo()
st.title("🏠 Home")
st.markdown(f"Welcome to **DartML**! This app lets you build Machine Learning models using :{config.SEMMA_COLOR}[**SEMMA**] methodology **without writing a single line of code**!")
st.markdown("Below there are explanations of each tab's functionality. But don't worry! You don't have to read it now, as the same explanations are available at the top of each tab.")

st.subheader(config.SAMPLE_PAGE_TITLE_WITH_COLOR)
show_page_explanation_in_expander("sample", expanded=True)

st.subheader(config.EXPLORE_PAGE_TITLE_WITH_COLOR)
show_page_explanation_in_expander("explore", expanded=True)

st.subheader(config.MODIFY_AND_MODEL_PAGE_TITLE_WITH_COLOR)
show_page_explanation_in_expander("modify_and_model", expanded=True)

st.subheader(config.ASSESS_PAGE_TITLE_WITH_COLOR)
show_page_explanation_in_expander("assess", expanded=True)
