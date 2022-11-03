import streamlit as st


st.title("Get Data")

try:    # if "my_input" in st.session_state.keys():
    st.write("You have entered", st.session_state["my_input"])
except KeyError:
    st.write("You have entered")
