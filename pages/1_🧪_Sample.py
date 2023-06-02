import streamlit as st
from src.session_state.session_state_checks import df_in_session_state, sampled_df_in_session_state
from src.sample.csv_loader_view import show_csv_loader
from src.general_views.df_view import show_uploaded_df, show_sampled_df
from src.general_views.sidebars_view import show_info_sidebar
from src.sample.sliders_view import show_data_sample_slider, show_train_test_split_slider
from src.general_views.logo import show_logo


show_logo()
st.title("🧪 Sample")

show_csv_loader()

if df_in_session_state():
    show_uploaded_df(expanded=True)

    st.divider()
    show_data_sample_slider()
    if sampled_df_in_session_state():
        show_sampled_df()

    st.divider()
    st.session_state.validation_type = st.selectbox("Use simple train/test split or 5-fold cross validation?", ("split", "kfold"), help="Choosing split is a faster option.")
    show_train_test_split_slider(disabled=True if st.session_state.validation_type == "kfold" else False)

show_info_sidebar()
