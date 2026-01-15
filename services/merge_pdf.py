import fitz  # PyMuPDF


def merge_pdfs(uploaded_files) -> bytes:
    """
    Unisce una lista di UploadedFile Streamlit in un unico PDF.
    Restituisce i byte del PDF finale.
    """
    if not uploaded_files:
        raise ValueError("Nessun file PDF fornito")

    output_pdf = fitz.open()

    for uploaded_file in uploaded_files:
        pdf_bytes = uploaded_file.read()
        src_pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
        output_pdf.insert_pdf(src_pdf)
        src_pdf.close()

    merged_bytes = output_pdf.tobytes()
    output_pdf.close()

    return merged_bytes
