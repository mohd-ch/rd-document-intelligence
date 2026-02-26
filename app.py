import streamlit as st
import pdfplumber
import docx
import string

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Prototype V1",
    page_icon="📊",
    layout="centered"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("System Info")
st.sidebar.write("Prototype: v1")
st.sidebar.write("Module: Document Intelligence")
st.sidebar.write("Status: AI-ready architecture")
st.sidebar.info("AI & OCR modules will be enabled in production environment.")

# ---------------- TITLE ----------------
st.title("R&D Document Intelligence Engine – Prototype v1")
st.caption("Modular document processing pipeline for requirement understanding and structured extraction.")
st.markdown("---")

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Client Document", type=["pdf","docx","txt"])

st.info("Note: Scanned/image PDFs will be supported in next version using OCR integration.")

# ---------------- EXTRACTION FUNCTIONS ----------------
def extract_pdf(file):
    text=""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text+=page.extract_text()+"\n"
    return text

def extract_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_txt(file):
    return file.read().decode("utf-8")

# ---------------- PROCESS ----------------
if uploaded_file:

    if uploaded_file.type == "application/pdf":
        text = extract_pdf(uploaded_file)
    elif "word" in uploaded_file.type:
        text = extract_docx(uploaded_file)
    else:
        text = extract_txt(uploaded_file)

    if text.strip()=="":
        st.error("No readable text detected in document.")
    else:
        st.success("Document processed successfully")

        # -------- METRICS --------
        words=len(text.split())
        chars=len(text)

        st.metric("Total Words", words)
        st.metric("Total Characters", chars)

        st.markdown("---")

        # -------- SECTION DETECTION --------
        lines=text.split("\n")
        headings=[l.strip() for l in lines if len(l)<60 and l.strip().isupper()]

        st.subheader("Detected Sections")
        if headings:
            for h in headings[:15]:
                st.write("•",h)
        else:
            st.write("No strong headings detected")

        st.markdown("---")

        # -------- KEY TECH TERMS --------
        stopwords=set([
            "the","and","for","with","this","that","from","have","are","was","were",
            "will","shall","into","your","our","their","there","here","about"
        ])

        clean=text.lower().translate(str.maketrans("","",string.punctuation))
        words_list=clean.split()

        freq={}
        for w in words_list:
            if w not in stopwords and len(w)>5:
                freq[w]=freq.get(w,0)+1

        sorted_words=sorted(freq.items(),key=lambda x:x[1],reverse=True)

        st.subheader("Key Technical Terms")
        for w,c in sorted_words[:15]:
            st.write(f"{w} ({c})")

        st.markdown("---")

        # -------- PREVIEW --------
        st.subheader("Raw Document Extraction (Pre-Processing View)")
        st.text_area("Content Snapshot", text[:2500], height=220)

        st.download_button("Download Extracted Text", text, "processed_text.txt")

# ---------------- FUTURE AI ----------------
st.markdown("---")
st.subheader("AI Intelligence Layer (Planned)")
st.write("""
Future production version will include:
- AI requirement summarization  
- Semantic keyword extraction  
- OCR for scanned documents  
- Client requirement detection  
- Structured data extraction  
""")