import streamlit as st
import base64
st.set_page_config(page_title="Govind Rawat", layout="wide",initial_sidebar_state="expanded" )

def show():
    st.title("👋 Hi, I'm Govind Rawat")
    expand = st.expander("⚠️ *Disclaimer:*",expanded=True)
    expand.write("""  
    This interactive resume is crafted with love ❤️ (and a lot of coffee ☕) using the **Streamlit** library.  
    So if something breaks, let’s just agree it’s not a bug — it’s a feature. 😅""")
    st.write("#### Senior IT Service Analyst | Data Science Enthusiast | Aspiring Developer")
    col = st.columns([1,1.5,1.5],border=True,vertical_alignment= "center")
    with col[0]:
        st.image("assets/1756729896853.jpg", width=350, use_container_width=True)
    with col[1]:
        with open("assets/certificate1.pdf", "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        # Embed PDF in iframe
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="450" type="application/pdf"></iframe>'
        #with st.expander("📄 View report"):
            st.markdown(pdf_display, unsafe_allow_html=True, width="content",)
    with col[2]:
        with open("assets/certificate2.pdf", "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        # Embed PDF in iframe
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="450" type="application/pdf"></iframe>'
        #with st.expander("📄 View report"):
            st.markdown(pdf_display, unsafe_allow_html=True)        
    st.markdown("## Building Data Centric Applications")
    st.markdown("""
                    Once upon a time, I proudly printed my very first **`Hello, World!`** in Python and thought I had conquered programming itself. 😅  

                    Fast forward to today, I’ve leveled up from that humble one-liner to building **data-centric applications** that actually *solve* problems (and don’t just say hello). 🚀  
                """)
    st.markdown("""
    #### Summary
    - 10+ years in IT service management  
    - Proficient in Python, data science, Streamlit, SQL  
    - Engineering practical ML solutions using Python, SQL, and Streamlit with CI/CD.  
    """)
    st.markdown("""
    #### Work History
    - Ipsos Research Pvt. Ltd : Sr. IT Service Analyst (July 2024 - PRESENT)
    - Crownit : Sr. IT Administrator (August  2015 - July 2024)
    - Appin Technology Lab :  IT Administrator (June 2013 - March 2015)
    """)


