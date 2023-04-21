import streamlit as st
import pandas as pd
from src.views.sidebar import progress_sidebar


st.title("Upload Data")


# load uploaded file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", accept_multiple_files=False)
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.session_state.df = dataframe

# show uploaded df
if "df" in st.session_state:
    st.write("")
    st.write("Uploaded DataFrame:")
    st.write(st.session_state.df)

# TODO: issue described in kanban board (search for SIDEBAR)
if "df" in st.session_state:
    df_info = {}
    df_info["row_num"] = len(st.session_state.df.index)
    df_info["col_num"] = len(st.session_state.df.columns)
    progress_sidebar(df_info)
