import streamlit as st
from PIL import Image
from src.general_views.logo import show_logo
from src.general_views.pages_explanations_view import show_sample_page_explanation, show_explore_page_explanation, show_modify_and_model_page_explanation, show_assess_page_explanation
from src import config

st.set_page_config(page_title="AutoML", page_icon=config.APP_FAVICON, layout="wide")

show_logo()
st.title("🏠 Home")
st.write(f"Welcome to DartML! This app lets you build a Machine Learning model using :{config.SEMMA_COLOR}[**SEMMA**] methodology without writing a single line of code.")

st.subheader(config.SAMPLE_PAGE_TITLE_WITH_COLOR)
show_sample_page_explanation()

st.subheader(config.EXPLORE_PAGE_TITLE_WITH_COLOR)
show_explore_page_explanation()

st.subheader(config.MODIFY_AND_MODEL_PAGE_TITLE_WITH_COLOR)
show_modify_and_model_page_explanation()

st.subheader(config.ASSESS_PAGE_TITLE_WITH_COLOR)
show_assess_page_explanation()