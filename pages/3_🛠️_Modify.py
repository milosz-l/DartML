import streamlit as st
from src.general_views.df_view import show_sampled_df
from src.general_views.sidebars_view import show_info_sidebar


st.title("🛠️ Modify")

if "df" not in st.session_state:
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar(target_column_selection=True)
    show_sampled_df(expanded=False)
