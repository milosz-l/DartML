import streamlit as st
from src.general_views.df_view import show_sampled_df
from src.general_views.sidebars_view import show_info_sidebar
from src.modify.target_select_view import show_target_column_selectbox
from src.general_views.mljar_explain_view import show_mljar_explain


st.title("🛠️ Modify")

if "df" not in st.session_state:
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar(target_column_selection=False)
    show_sampled_df(expanded=False)

    # show_target_column_selectbox()

    show_mljar_explain()
