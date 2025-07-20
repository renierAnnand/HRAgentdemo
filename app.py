import streamlit as st
import fitz  # PyMuPDF for PDF reading
from docx import Document
import re

st.set_page_config(page_title="AI Agent Demo - HR New Hire", layout="centered")

st.title("🤖 AI Agent Demo for HR - New Hire Process")

st.markdown("""
Upload a **New Hire Form** (PDF or DOCX) and let the AI Agent extract the data and simulate ERP upload.
""")

uploaded_file = st.file_uploader("📎 Upload New Hire Form", type=["pdf", "docx"])

def extract_from_pdf(file):
    text = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

def extract_from_docx(file):
    text = ""
    doc = Document(file)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def parse_fields(text):
    fields = {}
    patterns = {
        "Name": r"Name:\s*(.*)",
        "Email": r"Email:\s*(.*)",
        "Department": r"Department:\s*(.*)",
        "Role": r"Role:\s*(.*)",
        "Start Date": r"Start Date:\s*(.*)",
        "Salary": r"Salary:\s*(.*)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[key] = match.group(1).strip()
        else:
            fields[key] = "❌ Not Found"
    return fields

def validate(fields):
    missing = [k for k, v in fields.items() if "Not Found" in v or v.strip() == ""]
    return missing

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        content = extract_from_pdf(uploaded_file)
    else:
        content = extract_from_docx(uploaded_file)

    st.subheader("📄 Extracted Data")
    extracted_fields = parse_fields(content)
    for k, v in extracted_fields.items():
        st.write(f"**{k}**: {v}")

    st.subheader("✅ Validation")
    missing = validate(extracted_fields)
    if missing:
        st.error(f"Missing required fields: {', '.join(missing)}")
    else:
        st.success("All required fields found.")

        with st.spinner("Simulating Oracle ERP upload..."):
            st.success("🎉 ERP updated successfully with new hire data!")
