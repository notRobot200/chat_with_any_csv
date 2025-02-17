import os
import streamlit as st
from config import PDF_FILE, CHROMA_PERSIST_DIR, EMBEDDING_MODEL, LLM_MODEL
from loaders import load_and_split_document, create_or_load_vectordb
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sqlite3

# Load environment variables
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY environment variable not set.")
    st.stop()

def main():
    st.title("E-Office Handbook Q&A Application")

    try:
        docs = load_and_split_document(PDF_FILE)
        vectordb = create_or_load_vectordb(docs, CHROMA_PERSIST_DIR, EMBEDDING_MODEL)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        query = st.text_input("Enter your question:", placeholder="Enter your question here...")

        if st.button("Answer"):
            if query:
                try:
                    llm = ChatGroq(api_key=groq_api_key, model=LLM_MODEL)
                    qa = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
                    )

                    with st.spinner("Searching for answer..."):
                        result = qa.invoke({"query": query})
                        answer = result['result']
                        st.write(f"Answer: {answer}")

                except Exception as e:
                    st.error(f"An error occurred: {e}")

            else:
                st.warning("Please enter your question.")

    except Exception as e:
        st.exception(f"An initialization error occurred: {e}")

if __name__ == "__main__":
    main()
