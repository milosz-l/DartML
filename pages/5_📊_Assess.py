import streamlit as st
from src.general_views.df_view import show_sampled_df
from src.session_state.session_state_checks import sampled_df_in_session_state
from src.general_views.sidebars_view import show_info_sidebar
from src.general_views.mljar_explain_view import show_mljar_assess
from src.general_views.logo import show_logo
from src import config

st.set_page_config(page_title="AutoML", page_icon=config.APP_FAVICON, layout="wide")

show_logo()
st.title("📊 Assess")

if not sampled_df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar()
    show_sampled_df()
    show_mljar_assess()
