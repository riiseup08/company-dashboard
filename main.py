import streamlit as st

st.set_page_config(page_title="My App", layout="wide")

st.title("Welcome to Streamlit")

st.write("This is a simple Streamlit application.")

name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello, {name}!")

st.button("Click me!")