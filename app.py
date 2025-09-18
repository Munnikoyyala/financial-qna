import streamlit as st
import pandas as pd
import PyPDF2

st.title("📊 Financial Document Q&A Assistant")

# File upload
uploaded_file = st.file_uploader("Upload a financial document (PDF or Excel)", type=["pdf", "xlsx", "xls"])

data = None

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        st.subheader("Extracted Text from PDF")
        st.text_area("PDF Content", text, height=200)
        data = text

    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        df = pd.read_excel(uploaded_file)
        st.subheader("Excel Data Preview")
        st.dataframe(df.head())
        data = df

# Simple Q&A (Demo)
query = st.text_input("Ask a question about Revenue / Expenses / Profit:")

if query and data is not None:
    response = "Sorry, I can only show basic extraction in this demo."
    if isinstance(data, str):  # PDF text
        if "revenue" in query.lower():
            response = "Revenue details may be found in the extracted text above."
        elif "expense" in query.lower():
            response = "Expense details may be found in the extracted text above."
        elif "profit" in query.lower():
            response = "Profit details may be found in the extracted text above."
    else:  # Excel data
        if "revenue" in query.lower() and "Revenue" in data.columns:
            response = f"Total Revenue: {data['Revenue'].sum()}"
        elif "expense" in query.lower() and "Expenses" in data.columns:
            response = f"Total Expenses: {data['Expenses'].sum()}"
        elif "profit" in query.lower() and "Profit" in data.columns:
            response = f"Total Profit: {data['Profit'].sum()}"

    st.success(response)
