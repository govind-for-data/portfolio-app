import streamlit as st
from sections import about, project, AIML, Pivot, Search #contact

st.set_page_config(page_title="Govind Rawat", layout="wide",initial_sidebar_state="expanded" )

selection = st.sidebar.radio("Navigate to", ["About Me", "Old School Projects","ML/AI","Pivot Builder","Data Explorer"]) #, "Contact"])
# Conditional display based on sidebar selection
if selection == "About Me":
    try:
        about.show()   
    except Exception as e:
        st.error("⚠️ Oops...Something went wrong while loading. We have logged the error. We'll fix it soon.")
        st.error(e)
# Optional: log the actual error somewhere safe
        with open("error.log", "a") as f:
            f.write(str(e) + "\n")
elif selection == "Old School Projects":
    try:
        project.show()
    except Exception as e:
        st.error("⚠️ Oops...Something went wrong while loading. We have logged the error. We'll fix it soon.")
        st.error(e)
# Optional: log the actual error somewhere safe
        with open("error.log", "a") as f:
            f.write(str(e) + "\n")
elif selection == "ML/AI":
    try:
        AIML.show()
    except Exception as e:
        st.error("⚠️ Oops...Something went wrong while loading. We have logged the error. We'll fix it soon.")
        st.error(e)
# Optional: log the actual error somewhere safe
        with open("error.log", "a") as f:
            f.write(str(e) + "\n")
elif selection == "Pivot Builder":
    try:
        Pivot.show()
    except Exception as e:
        st.error("⚠️ Oops...Something went wrong while loading. We have logged the error. We'll fix it soon.")
        st.error(e)
# Optional: log the actual error somewhere safe
        with open("error.log", "a") as f:
            f.write(str(e) + "\n")
elif selection == "Data Explorer":
    try:
        Search.show()
    except Exception as e:
        st.error("⚠️ Oops...Something went wrong while loading. We have logged the error. We'll fix it soon.")
        st.error(e)
# Optional: log the actual error somewhere safe
        with open("error.log", "a") as f:
            f.write(str(e) + "\n")

# ############## Tab style menu bar #####################
# tab = st.tabs(["About Me", "Projects","ML/AI","Create Pivots","Data Explorer"])
# with tab[0]:
#     try:
#         about.show()   
#     except Exception as e:
#         st.error("⚠️ Something went wrong while loading the data. Please contact support.")
#         st.error(e)
#     # Optional: log the actual error somewhere safe
#         with open("error.log", "a") as f:
#             f.write(str(e) + "\n")
# with tab[1]:
#     try:
#         project.show()
#     except Exception as e:
#         st.error("⚠️ Something went wrong while loading the data. Please contact support.")
#         st.error(e)
#     # Optional: log the actual error somewhere safe
#         with open("error.log", "a") as f:
#             f.write(str(e) + "\n")
# with tab[2]:
#     try:
#         AIML.show()
#     except Exception as e:
#         st.error("⚠️ Something went wrong while loading the data. Please contact support.")
#         st.error(e)
#  # Optional: log the actual error somewhere safe
#         with open("error.log", "a") as f:
#             f.write(str(e) + "\n")
# with tab[3]:
#     try:
#         Pivot.show()
#     except Exception as e:
#         st.error("⚠️ Something went wrong while loading the data. Please contact support.")
#         st.error(e)
#  # Optional: log the actual error somewhere safe
#         with open("error.log", "a") as f:
#             f.write(str(e) + "\n")
# with tab[2]:
#     try:
#         Search.show()
#     except Exception as e:
#         st.error("⚠️ Something went wrong while loading the data. Please contact support.")
#         st.error(e)
#  # Optional: log the actual error somewhere safe
#         with open("error.log", "a") as f:
#             f.write(str(e) + "\n")