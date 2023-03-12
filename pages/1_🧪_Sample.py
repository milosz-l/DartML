import streamlit as st
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns


# Upload Data
st.title("Upload Data")

# load uploaded file
uploaded_file = st.file_uploader("Choose a CSV file", type='csv', accept_multiple_files=False)
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    dataframe = pd.read_csv(uploaded_file)
    st.session_state['df'] = dataframe

    # TODO: comment/uncomment below and check whether it's faster
    # # calculate heatmap
    # st.session_state['heatmap_fig'] = plt.figure(figsize=(16, 16))
    # sns.heatmap(st.session_state['df'].corr(numeric_only=True), square=True, cmap='RdYlGn', annot=True, fmt=".2f", linewidth=0.5)

    # # calculate pairplot
    # st.session_state['pairplot_fig'] = sns.pairplot(st.session_state['df'])


# show uploaded df
if 'df' in st.session_state:
    st.write('')
    st.write('Uploaded DataFrame:')
    st.write(st.session_state['df'])
