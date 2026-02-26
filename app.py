import streamlit as st
import pdfplumber
import docx
import string

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Document Extractor Prototype",
    page_icon="📄",
    layout="centered"
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("System Info")
    st.write("Version: Prototype v1")
    st.write("Processing: Local Python Modules")
    st.write("Supported Formats:")
    st.write("• PDF")
    st.write("• DOCX")
    st.write("• TXT")
    st.markdown("---")
    st.caption("No external APIs used")

# ---------------- TITLE ----------------
st.title("Document Extractor — Prototype v1")
st.caption("Lightweight document extraction and analysis tool")

st.markdown(" ")

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "docx", "txt"]
)
st.info(
    "⚠️ Current limitations: "
    "Scanned/image PDFs, OCR extraction, and complex multi-column layouts "
    "are not supported in Prototype v1."
)

# ---------------- EXTRACTION FUNCTIONS ----------------
def extract_pdf(file):
    text = ""
    pages = 0
    with pdfplumber.open(file) as pdf:
        pages = len(pdf.pages)
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text, pages


def extract_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs]), 1


def extract_txt(file):
    return file.read().decode("utf-8"), 1


# ---------------- PROCESS ----------------
if uploaded_file:

    with st.spinner("Extracting document..."):

        if uploaded_file.type == "application/pdf":
            text, pages = extract_pdf(uploaded_file)
        elif "word" in uploaded_file.type:
            text, pages = extract_docx(uploaded_file)
        else:
            text, pages = extract_txt(uploaded_file)

        if text.strip() == "":
            st.error("No readable text detected.")
        else:
            st.success("Document processed successfully")
        words = len(text.split())
        chars = len(text)
        read_time = max(1, round(words / 200))

        # ================= SUMMARY =================
        with st.container():
            if uploaded_file:
                file_name = uploaded_file.name
                file_type = uploaded_file.type
                file_size = round(uploaded_file.size / 1024, 2)
            st.subheader("📊 Document Summary")
            st.caption(f"File: {file_name} | Type: {file_type} | Size: {file_size} KB")

            col1, col2 = st.columns(2)
            col1.metric("Pages", pages)
            col2.metric("Words", words)

            col3, col4 = st.columns(2)
            col3.metric("Characters", chars)
            col4.metric("Read Time", f"{read_time} min")

        st.markdown(" ")

        # ================= TABS =================
        tab1, tab2, tab3 = st.tabs(
            ["🧩 Structure", "🔑 Keywords", "📑 Preview"]
        )

        # -------- STRUCTURE TAB --------
        with tab1:
            lines = text.split("\n")
            headings = [
                l.strip()
                for l in lines
                if len(l) < 60 and l.strip().isupper()
            ]

            if headings:
                st.write("Detected headings:")
                for h in headings[:20]:
                    st.write("•", h)
            else:
                st.write("No clear headings detected.")

        # -------- KEYWORDS TAB --------
        with tab2:

            stopwords = {
                "the","and","for","with","this","that","from","have","are",
                "was","were","will","shall","into","your","our","their",
                "there","here","about"
            }

            clean = text.lower().translate(
                str.maketrans("", "", string.punctuation)
            )

            words_list = clean.split()

            freq = {}
            for w in words_list:
                if w not in stopwords and len(w) > 5:
                    freq[w] = freq.get(w, 0) + 1

            sorted_words = sorted(
                freq.items(),
                key=lambda x: x[1],
                reverse=True
            )

            if sorted_words:
                st.write("Top keywords:")
                st.write(", ".join([w for w, _ in sorted_words[:20]]))
            else:
                st.write("No keywords detected.")

        # -------- PREVIEW TAB --------
        with tab3:
            st.text_area(
                "Extracted Text Preview",
                text[:3000],
                height=220
            )

        st.markdown(" ")

        # ================= DOWNLOAD =================
        st.download_button(
            "⬇️ Download Extracted Text",
            text,
            file_name="extracted_text.txt"
        )