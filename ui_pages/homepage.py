import streamlit as st

st.set_page_config(
    page_title="Homepage",
    page_icon="🏠",
    layout="wide",
)

st.title("😤 I Hate PDF")

st.markdown(
    """
Un insieme di strumenti PDF che **nessuno ama usare**  
ma che **tutti prima o poi devono usare**.

Scegli un tool dal menu a sinistra per iniziare.
"""
)

st.divider()

st.subheader("🧰 Tool disponibili")

st.markdown(
    """
- 🔗 **Merge PDF**  
  Unisci più file PDF in un unico documento.

- ✂️ **Split PDF** *(coming soon)*  
  Dividi un PDF in più parti.

- 🗜️ **Compress PDF** *(coming soon)*  
  Riduci il peso dei tuoi PDF.
"""
)

st.divider()

st.caption(
    "I Hate PDF — built with Streamlit & PyMuPDF"
)
