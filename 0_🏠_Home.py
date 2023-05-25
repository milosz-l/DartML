import streamlit as st
from PIL import Image

# page config
st.set_page_config(page_title="AutoML", page_icon="💡", layout="wide")

st.title("🏠 Home")

st.write("Build a Machine Learning model using SEMMA methodology.")
st.image(Image.open("79b0e02b-20b7-4017-b56b-92cbd4993ba5.webp"))
st.write("You can return to some specific step any time you want!")
