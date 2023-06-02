import streamlit as st
from src.general_views.df_view import show_sampled_df
from src.general_views.sidebars_view import show_info_sidebar
from src.session_state.session_state_checks import sampled_df_in_session_state
from src.explore.plots_view import show_plots, show_altair_plots
from src.general_views.logo import show_logo


# use style.css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("src/explore/style.css")

show_logo()
st.title("🔍 Explore")

if not sampled_df_in_session_state():
    st.write("You need to upload some data first! Please go to Sample tab.")
else:
    show_info_sidebar()
    show_sampled_df()

    st.divider()

    sampled_df_before_plotting = st.session_state.sampled_df.copy()
    show_altair_plots()
    sampled_df_after_plotting = st.session_state.sampled_df.copy()
    is_same = sampled_df_before_plotting.equals(sampled_df_after_plotting)
    st.experimental_show(is_same)
    # show_plots(expanded=True)
