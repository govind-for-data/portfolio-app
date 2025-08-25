import streamlit as st
import base64

def show():
  st.title("Projects")
  st.write("Data Analysis | Data Visualization | Machine Learning | SQL | PowerBI")
  expand = st.expander("ℹ️ Information")
  expand.write("""Inform about this short journy of transition""")
    # Insert containers separated into tabs:
  tab1, tab2,tab3, tab4 = st.tabs(["Data Analysis", "Data Visualization", "Machine Learning", "Application Deployment"])
    # You can also use "with" notation:
  with tab1:
    st.write("""
             ##### Techniques: 
            - Data cleaning, Exploratory Data Analysis, Descriptive statistics.
            """)
    st.markdown("---")
    st.markdown("### Cutomer Churn Predection")
    st.write("""
                 -  Developed a machine learning model that accurately predicts customer churn for an ecommerce company and recommended targeted retention strategies to reduce churn rate.
                 - Selected relevant features and engineered new features to enhance model performance
                 - Utilized various machine learning algorithms such as logistic regression, random forest, LDA, KNN and bagging classifier.
                 - Tuned hyperparameters to optimize model performance. Achieved an accuracy of 88% in predicting customer churn.
                    """)
    with open("assets/Customer_Churn.pdf", "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        # Embed PDF in iframe
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        with st.expander("📄 View report"):
          st.markdown(pdf_display, unsafe_allow_html=True)
#          st.download_button("📥 Download Resume (PDF)", f, "resume.pdf", "application/pdf")

    with open("assets/Customer_Churn.pdf", "rb") as f:
      st.download_button("📥 Download PDF", f, "Customer_Churn.pdf", "assets/Customer_Churn.pdf")
#      st.write("### Preview:")
    st.markdown("---")
      
    expand_1_2 = st.expander("User profiling")
    expand_1_2.write("""
                 -  Developed a machine learning model that accurately predicts customer churn for an ecommerce company and recommended targeted retention strategies to reduce churn rate.
                 - Selected relevant features and engineered new features to enhance model performance
                 - Utilized various machine learning algorithms such as logistic regression, random forest, LDA, KNN and bagging classifier.
                 - Tuned hyperparameters to optimize model performance. Achieved an accuracy of 88% in predicting customer churn.
                 """)
    expand_1_3 = st.expander("User Retentation")
    expand_1_3.write("""
                 -  Developed a machine learning model that accurately predicts customer churn for an ecommerce company and recommended targeted retention strategies to reduce churn rate.
                 - Selected relevant features and engineered new features to enhance model performance
                 - Utilized various machine learning algorithms such as logistic regression, random forest, LDA, KNN and bagging classifier.
                 - Tuned hyperparameters to optimize model performance. Achieved an accuracy of 88% in predicting customer churn.
                 """)
    st.markdown("""#### Summary""")
  with tab2:
    st.write("""
             ##### Techniques: 
            - Exploratory Data Analysis, Insights, PowerBI, SQL.
            """)
    expand_2_1 = st.expander("PowerBI Dashboard on IT Assets")
    expand_2_1.write("""
                 -  Developed a machine learning model that accurately predicts customer churn for an ecommerce company and recommended targeted retention strategies to reduce churn rate.
                 - Selected relevant features and engineered new features to enhance model performance
                 - Utilized various machine learning algorithms such as logistic regression, random forest, LDA, KNN and bagging classifier.
                 - Tuned hyperparameters to optimize model performance. Achieved an accuracy of 88% in predicting customer churn.
                 """)
    expand_2_2 = st.expander("Streamlit Application for Inventory")
    expand_2_2.write("""
                 -  Developed a machine learning model that accurately predicts customer churn for an ecommerce company and recommended targeted retention strategies to reduce churn rate.
                 - Selected relevant features and engineered new features to enhance model performance
                 - Utilized various machine learning algorithms such as logistic regression, random forest, LDA, KNN and bagging classifier.
                 - Tuned hyperparameters to optimize model performance. Achieved an accuracy of 88% in predicting customer churn.
                 """)
    st.markdown("""#### Summary""")
  with tab3:
    expand_3 = st.expander("Support Vector Machine")
    expand_3.write("""
                 -  Developed a machine learning model that accurately predicts customer churn for an ecommerce company and recommended targeted retention strategies to reduce churn rate.
                 - Selected relevant features and engineered new features to enhance model performance
                 - Utilized various machine learning algorithms such as logistic regression, random forest, LDA, KNN and bagging classifier.
                 - Tuned hyperparameters to optimize model performance. Achieved an accuracy of 88% in predicting customer churn.
                 """)
    st.write("""
             ##### Techniques: 
            - Data cleaning, Exploratory Data Analysis, Logistics regression, LDA, KNN, Decision tree, Random forest, ensemble techniques, SMOTE, Hyper-parameter tuning, cross-validation .
            """)
    st.markdown("""#### Summary""")
  with tab4:
    expand_3 = st.expander("Inventory Mannagement Application")
    expand_3.write("""
                 -  Developed a machine learning model that accurately predicts customer churn for an ecommerce company and recommended targeted retention strategies to reduce churn rate.
                 - Selected relevant features and engineered new features to enhance model performance
                 - Utilized various machine learning algorithms such as logistic regression, random forest, LDA, KNN and bagging classifier.
                 - Tuned hyperparameters to optimize model performance. Achieved an accuracy of 88% in predicting customer churn.
                 """)
    st.write("""
             ##### Techniques: 
            - Data cleaning, Exploratory Data Analysis, Logistics regression, LDA, KNN, Decision tree, Random forest, ensemble techniques, SMOTE, Hyper-parameter tuning, cross-validation .
            """)
    st.markdown("""#### Summary""")