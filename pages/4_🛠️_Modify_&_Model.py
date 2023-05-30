import streamlit as st
from src.general_views.df_view import show_sampled_df

from src.session_state.session_state_checks import sampled_df_in_session_state
from src.general_views.mljar_explain_view import show_mljar_model
from src.general_views.sidebars_view import show_info_sidebar
from src.general_views.logo import show_logo


show_logo()
st.title("🛠️ Modify & Model")

if not sampled_df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar()
    show_sampled_df()
    show_mljar_model()
