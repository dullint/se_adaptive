import streamlit as st
import webbrowser

st.title("Documentation")
# Option 2: Using a button with callback
if st.button("📚 Open Documentation"):
    webbrowser.open_new_tab("https://dullint.github.io/se_adaptive/")
    st.info("Documentation opened in a new tab!")
