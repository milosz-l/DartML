import time

import streamlit as st

from src import config
from src.assess.assess_view import show_download_button, show_training_results
from src.general_views.df_view import show_sampled_df
from src.general_views.logo import show_logo
from src.general_views.pages_explanations_view import show_page_explanation_in_expander
from src.general_views.sidebars_view import show_info_sidebar
from src.session_state.already_pressed_check import (
    already_pressed_based_on_session_state,
)
from src.session_state.session_state_checks import (
    automl_trainer_in_session_state,
    sampled_df_in_session_state,
)

st.set_page_config(
    page_title=config.APP_TITLE, page_icon=config.APP_FAVICON, layout="wide"
)

show_logo()
st.title(config.ASSESS_PAGE_TITLE)
show_page_explanation_in_expander("assess")

if not sampled_df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar()
    show_sampled_df()

    # show training results in real time
    placeholder = st.empty()
    try:
        while already_pressed_based_on_session_state():
            with placeholder.container():
                show_training_results()
                time.sleep(config.ASSESS_REFRESH_INTERVAL)
        with placeholder.container():
            show_training_results()
            time.sleep(config.ASSESS_REFRESH_INTERVAL)
        if automl_trainer_in_session_state:
            show_download_button(
                st.session_state.automl_trainer.tempdir.name
            )  # show download button after training is finished
    except AttributeError:
        st.warning("First you need to start training in the **Modify & Model** tab.")
