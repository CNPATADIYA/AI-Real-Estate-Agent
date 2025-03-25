import streamlit as st

pages = {
    "NAVIGATION": [
        st.Page("questionnaire.py", title="Questionnaire"),
        st.Page("advisor.py", title="RealEstate AI Advisor"),
    ]
}
pg = st.navigation(pages)
pg.run()