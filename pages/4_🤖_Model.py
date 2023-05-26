import streamlit as st
from src.session_state.session_state_checks import sampled_df_in_session_state
from src.general_views.mljar_explain_view import show_mljar_explain
from src.general_views.sidebars_view import show_info_sidebar


# Train Model
st.title("🤖 Model")

if not sampled_df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar()
    show_mljar_explain()

    # st.write("## Scores")  # TODO: change to automatic
    # max_score = max(scores_dict.values())
    # for model_name, score in scores_dict.items():
    #     # st.write(f'{model_name}: {score}')
    #     st.metric(model_name, score, score - max_score)
