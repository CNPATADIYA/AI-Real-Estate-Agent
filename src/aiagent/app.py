import streamlit as st

pages = {
    "NAVIGATION": [
        st.Page("main.py", title="User Preference"),
        st.Page("chatbot.py", title="RealEstate AI Advisor"),
    ]
}
pg = st.navigation(pages)
pg.run()