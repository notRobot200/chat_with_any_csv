# type: ignore
import streamlit as st
import os
from utils import get_answer_csv

st.set_page_config(
    page_title="Chat with your CSV",
    page_icon="📗"  
)

st.header("Chat with any CSV")

# Choose file input method
file_method = st.radio(
    "Select CSV file input method",
    ["Upload File", "Use Existing File"]
)

csv_file = None

if file_method == "Upload File":
    uploaded_file = st.file_uploader("Upload a csv file", type=["csv"])
    if uploaded_file is not None:
        csv_file = uploaded_file
else:
    # Path to existing CSV file
    path_csv = 'docs/csv/synthetic_transaction_data.csv'

    if os.path.exists(path_csv):
        csv_file = open(path_csv, 'rb')
        st.success(f"Using file: {path_csv}")
    else:
        st.error(f"File not found at path: {path_csv}")

if csv_file is not None:
    query = st.text_area("Ask any question related to the document")
    button = st.button("Submit")
    if button:
        st.write(get_answer_csv(csv_file, query))

        # Close file if using local file
        if file_method == "Use Existing File":
            csv_file.close()
