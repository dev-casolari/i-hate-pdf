import streamlit as st

homepage = st.Page("ui_pages/homepage.py", title="🏠 Homepage")
merge_pdf = st.Page("ui_pages/merge_pdf.py", title="🔗 Merge PDF")

pages = st.navigation([homepage, merge_pdf])
pages.run()
