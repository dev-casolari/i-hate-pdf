import streamlit as st
from services.merge_pdf import merge_pdfs


# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Merge PDF",
    page_icon="🔗",
    layout="centered",
)

st.title("🔗 Merge PDF")
st.write("Carica uno o più PDF e scegli l’ordine prima di unirli.")

st.divider()


# --------------------------------------------------
# Session state initialization
# --------------------------------------------------
if "pdf_files" not in st.session_state:
    st.session_state.pdf_files = []

if "merged_pdf" not in st.session_state:
    st.session_state.merged_pdf = None


# --------------------------------------------------
# File uploader
# --------------------------------------------------
uploaded_files = st.file_uploader(
    "Carica i PDF",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:
    existing_names = [f.name for f in st.session_state.pdf_files]
    for f in uploaded_files:
        if f.name not in existing_names:
            st.session_state.pdf_files.append(f)

    # se carico nuovi file, invalido il merge precedente
    st.session_state.merged_pdf = None


# --------------------------------------------------
# Order UI
# --------------------------------------------------
if st.session_state.pdf_files:
    st.subheader("Ordine dei PDF")

    for index, pdf in enumerate(st.session_state.pdf_files):
        col_name, col_up, col_down = st.columns([6, 1, 1])

        col_name.write(f"{index + 1}. {pdf.name}")

        if col_up.button("⬆️", key=f"up_{index}") and index > 0:
            st.session_state.pdf_files[index - 1], st.session_state.pdf_files[index] = (
                st.session_state.pdf_files[index],
                st.session_state.pdf_files[index - 1],
            )
            st.session_state.merged_pdf = None
            st.rerun()

        if col_down.button("⬇️", key=f"down_{index}") and index < len(st.session_state.pdf_files) - 1:
            st.session_state.pdf_files[index + 1], st.session_state.pdf_files[index] = (
                st.session_state.pdf_files[index],
                st.session_state.pdf_files[index + 1],
            )
            st.session_state.merged_pdf = None
            st.rerun()

    st.divider()


# --------------------------------------------------
# Output filename
# --------------------------------------------------
output_name = st.text_input(
    "Nome file di output",
    value="merged.pdf",
)


# --------------------------------------------------
# Merge action
# --------------------------------------------------
if st.button("Unisci PDF", type="primary", disabled=not st.session_state.pdf_files):
    try:
        st.session_state.merged_pdf = merge_pdfs(st.session_state.pdf_files)
        st.success("PDF uniti correttamente ✅")
    except Exception as e:
        st.error("Errore durante l’unione dei PDF 😵")
        st.exception(e)


# --------------------------------------------------
# Download button (PERSISTENTE)
# --------------------------------------------------
if st.session_state.merged_pdf:
    st.download_button(
        label="⬇️ Scarica il PDF",
        data=st.session_state.merged_pdf,
        file_name=output_name if output_name.lower().endswith(".pdf") else f"{output_name}.pdf",
        mime="application/pdf",
    )


# --------------------------------------------------
# Reset
# --------------------------------------------------
if st.session_state.pdf_files:
    if st.button("Reset lista"):
        st.session_state.pdf_files = []
        st.session_state.merged_pdf = None
        st.rerun()
