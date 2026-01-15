import streamlit as st
from streamlit_sortables import sort_items

from services.merge_pdf import merge_pdfs


# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Merge PDF",
    page_icon="🔗",
    layout="wide",
)

st.title("🔗 Merge PDF")
st.write("Carica uno o più PDF e trascinali per scegliere l’ordine.")
st.caption("📌 Limiti: minimo 2 PDF · massimo 20 PDF")
st.divider()


# --------------------------------------------------
# Session state
# --------------------------------------------------
if "pdf_files" not in st.session_state:
    st.session_state.pdf_files = []

if "merged_pdf" not in st.session_state:
    st.session_state.merged_pdf = None

if "has_merged" not in st.session_state:
    st.session_state.has_merged = False


# --------------------------------------------------
# File uploader (inizializzazione)
# --------------------------------------------------
cols = st.columns([0.4, 0.1, 0.4, 0.1])
with cols[0]:
    uploaded_files = st.file_uploader(
        "Carica i PDF",
        type=["pdf"],
        accept_multiple_files=True,
    )

# inizializza SOLO se non ho ancora file
if uploaded_files and not st.session_state.pdf_files:
    st.session_state.pdf_files = uploaded_files.copy()
    st.session_state.merged_pdf = None
    st.session_state.has_merged = False

# --------------------------------------------------
# Guardrails
# --------------------------------------------------
pdf_count = len(st.session_state.pdf_files)
can_merge = True

if pdf_count == 1:
    st.error("⚠️ Devi caricare **almeno 2 PDF** per poterli unire.")
    can_merge = False
elif pdf_count > 20:
    st.error("⚠️ Puoi unire **al massimo 20 PDF** alla volta.")
    can_merge = False

# --------------------------------------------------
# PDF list (sempre visibile)
# --------------------------------------------------
if st.session_state.pdf_files:
    with cols[2]:
        st.caption("Trascina per riordinare")

        file_names = [f.name for f in st.session_state.pdf_files]

        # drag & drop ATTIVO solo prima del merge
        if not st.session_state.has_merged:
            sorted_names = sort_items(
                file_names,
                direction="vertical",
                key="pdf_sorter",
            )

            name_to_file = {f.name: f for f in st.session_state.pdf_files}
            st.session_state.pdf_files = [name_to_file[name] for name in sorted_names]

        # dopo il merge: lista statica
        else:
            for i, name in enumerate(file_names, start=1):
                st.write(f"{i}. {name}")

# --------------------------------------------------
# MERGE BUTTON
# --------------------------------------------------
if st.session_state.pdf_files and not st.session_state.has_merged:
    if st.button("Unisci PDF", disabled=not can_merge):
        st.session_state.merged_pdf = merge_pdfs(st.session_state.pdf_files)
        st.session_state.has_merged = True
        st.rerun()

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------
if st.session_state.has_merged and st.session_state.merged_pdf:
    st.download_button(
        "⬇️ Scarica il PDF",
        data=st.session_state.merged_pdf,
        file_name="i-hate-merged.pdf",
        mime="application/pdf",
    )
