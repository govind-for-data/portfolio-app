import streamlit as st
from sections import about, project, contact

st.set_page_config(page_title="Govind Rawat", layout="wide")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("About Me"):
        about.show()

with col2:
    if st.button("Projects"):
        project.show()

with col3:
    if st.button("Contact"):
        contact.show()
