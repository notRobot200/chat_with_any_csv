from typing import TextIO
from langchain_experimental.agents import create_csv_agent
from langchain_groq import ChatGroq
from config import LLM_MODEL
import os
import streamlit as st

groq_api_key = st.secrets["GROQ_API_KEY"]

def get_answer_csv(file: TextIO, query: str) -> str:
    """
    Returns the answer to the given query by querying a CSV file.

    Args:
    - file (str): the file path to the CSV file to query.
    - query (str): the question to ask the agent.

    Returns:
    - answer (str): the answer to the query from the CSV file.
    """

    llm = ChatGroq(
        api_key=groq_api_key,
        model_name=LLM_MODEL,
        temperature = 0
    )

    # Create an agent using the LLM model and the CSV file
    agent = create_csv_agent(llm, file, verbose=True, allow_dangerous_code=True)

    #query = "whats the square root of the average age?"
    answer = agent.run(query)
    return answer
