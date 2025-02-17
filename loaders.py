import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import streamlit as st

def load_and_split_document(pdf_file):
    loader = PyPDFLoader(pdf_file)
    with st.spinner("Loading document..."):
        documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    with st.spinner("Splitting document..."):
        docs = text_splitter.split_documents(documents)
    return docs

def create_or_load_vectordb(docs, persist_dir, embedding_model):
    embeddings = OllamaEmbeddings(model=embedding_model)

    if not os.path.exists(persist_dir):
        with st.spinner("Processing embeddings and saving to ChromaDB (one-time only)..."):
            vectordb = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                persist_directory=persist_dir
            )
    else:
        with st.spinner("Loading vector database from storage..."):
            vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vectordb