import streamlit as st
from sections import about, project, AIML, Pivot #contact

st.set_page_config(page_title="Govind Rawat", layout="wide",initial_sidebar_state="expanded" )

# col1, col2, col3 = st.columns(3)

# with col1:
#     if st.button("About Me"):
#         about.show()

# with col2:
#     if st.button("Projects"):
#         project.show()

# with col3:
#     if st.button("Contact"):
#         contact.show()
selection = st.sidebar.radio("Navigate to", ["About Me", "Projects","ML/AI","Create Pivots"]) #, "Contact"])

# Conditional display based on sidebar selection
if selection == "About Me":
    about.show()
elif selection == "Projects":
    project.show()
elif selection == "ML/AI":
    AIML.show()
elif selection == "Create Pivots":
    try:
        Pivot.show()
    except Exception as e:
        st.error("⚠️ Something went wrong while loading the data. Please contact support.")
        st.error(e)
# Optional: log the actual error somewhere safe
        with open("error.log", "a") as f:
            f.write(str(e) + "\n")