import streamlit as st

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)

st.title("Session State")
st.sidebar.success("Select a page above.")

if "my_input" not in st.session_state:  # we check if key is not already in a session_state
    st.session_state["my_input"] = ""

my_input = st.text_input("Input a text here", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    st.session_state["my_input"] = my_input
    st.write("You have entered: ", my_input)

try:    # if "my_input" in st.session_state.keys():
    st.write("You have entered", st.session_state["my_input"])
except KeyError:
    st.write("You have entered")


st.session_state
