import streamlit as st


def progress_sidebar(df_info):
    st.sidebar.header('DataFrame info')
    st.sidebar.write(f'{df_info["col_num"]} columns')
    st.sidebar.write(f'{df_info["row_num"]} rows')
