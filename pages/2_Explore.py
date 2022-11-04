import streamlit as st

# Transform Data
st.title("Explore Data")

# show uploaded df
if 'df' in st.session_state:
    st.write('Uploaded DataFrame:')
    st.write(st.session_state['df'])

# Drop columns
