import streamlit as st
import pandas as pd
from io import StringIO

# Upload Data
st.title("Upload Data")

# load uploaded file
uploaded_file = st.file_uploader("Choose a CSV file", type='csv', accept_multiple_files=False)
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    dataframe = pd.read_csv(uploaded_file)
    st.session_state['df'] = dataframe

# show uploaded df
if 'df' in st.session_state:
    st.write('')
    st.write('Uploaded DataFrame:')
    st.write(st.session_state['df'])
