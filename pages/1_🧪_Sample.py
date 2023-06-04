import streamlit as st
from src.session_state.session_state_checks import df_in_session_state, sampled_df_in_session_state
from src.sample.csv_loader_view import show_csv_loader, show_use_example_data_button
from src.general_views.df_view import show_uploaded_df, show_sampled_df
from src.general_views.sidebars_view import show_info_sidebar
from src.sample.sliders_view import show_data_sample_slider, show_train_test_split_slider
from src.general_views.logo import show_logo
from src import config
from src.general_views.pages_explanations_view import show_page_explanation_in_expander

st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_FAVICON, layout="wide")

show_logo()
st.title(config.SAMPLE_PAGE_TITLE)
show_page_explanation_in_expander("sample")


show_csv_loader()
st.markdown("OR")
show_use_example_data_button()
st.markdown("The example `Hotel Reservations` dataset comes from [here](https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset).")

if df_in_session_state():
    st.divider()
    show_uploaded_df(expanded=True)

    st.divider()
    show_data_sample_slider()
    if sampled_df_in_session_state():
        show_sampled_df()

    st.divider()
    st.session_state.validation_type = st.selectbox("Use simple train/test split or 5-fold cross validation?", ("split", "kfold"), help="Choosing split is a faster option.")
    col1, col2 = st.columns(2)
    st.session_state.shuffle = col1.checkbox(
        "Shuffle", value=True, help="Shuffle means splitting the data randomly. It's advised to leave it turned on. But you may want to turn it off e.g. for time series analysis problems."
    )
    st.session_state.stratify = col2.checkbox(
        "Stratify", value=True, help="Stratify ensures that both the train and test sets have the same proportion of examples in each class. It's advised to leave it on."
    )

    show_train_test_split_slider(disabled=True if st.session_state.validation_type == "kfold" else False)

show_info_sidebar()
