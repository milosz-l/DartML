import streamlit as st
from src.utils.session_state_checks import df_in_session_state
from src.sample.csv_loader import show_csv_loader
from src.general_views.uploaded_df import show_uploaded_df
from src.general_views.sidebars import show_info_sidebar
from src.sample.sliders import show_data_sample_slider, show_train_test_split_slider


st.title("🧪 Sample")

show_csv_loader()

if df_in_session_state():
    show_uploaded_df(expanded=True)

    st.divider()
    show_data_sample_slider()
    st.divider()
    show_train_test_split_slider()

show_info_sidebar()
