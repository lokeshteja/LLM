import os
import json
import pandas as pd
import traceback
import openai
import langchain 
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_openai.llms import OpenAI
from langchain_community.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from src.mcqgenerator.logger import logging 
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.MCQGenerator_app import final_chain


response_path = '/Users/loke/Library/CloudStorage/Dropbox/Project/LLM Projects/LLM_MCQ_Generator/Response.json'
with open(response_path,'r') as file:
    RESPONSE_JSON = json.load(file)


# Creating a title for the app
st.title("MCQs Generator Application with LangChain 🧠")

# Create a form using st.form
with st.form("user_inputs"):
    # File Upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    # Input Fields
    mcq_count = st.number_input("No. of MCQs", min_value=1, max_value=50)

    # Subject
    subject = st.text_input("Insert Subject", max_chars=20)

    # Quiz Tone
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    # Add Button
    button = st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Creating MCQ's"):
            try:
                # Read file and get text
                text = read_file(uploaded_file)
                
                # Count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response = final_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
                
                # Print the token usage and cost
                st.write(f"Total Tokens: {cb.total_tokens}")
                st.write(f"Prompt Tokens: {cb.prompt_tokens}")
                st.write(f"Completion Tokens: {cb.completion_tokens}")
                st.write(f"Total Cost: {cb.total_cost}")
                
                # Check if the response is a dictionary (successful response)
                if isinstance(response, dict):
                    # Extract the quiz data from the response
                    quiz = response.get("quiz_questions", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # Display the review in a text box
                            st.text_area(label="Review", value=response["quiz_review"])
                        else:
                            st.error("Error in the table data")
                    else:
                        st.error("Error: No quiz data found in the response.")
                else:
                    st.write(response)
                
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

