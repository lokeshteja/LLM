import os
import json
import pandas as pd
import traceback
import openai
import langchain 
import PyPDF2
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_openai.llms import OpenAI
from langchain_community.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from src.mcqgenerator.logger import logging 
from src.mcqgenerator.utils import read_file,get_table_data



#Load environment variables 
load_dotenv()
#get the key stored in .env file 
KEY = os.getenv('OPENAI_API_KEY')

#get the model  that 
llm = ChatOpenAI(model_name = "gpt-3.5-turbo",api_key=KEY)

#Template for the input prompt 
TEMPLATE = """
Text: {text}

As an expert in MCQ generation, your task is to create a quiz consisting of {number} multiple-choice questions for students studying {subject}. The questions should be crafted in a {tone} manner and reflect the context provided. Each question must have one correct answer and three incorrect options.

Ensure your responses are structured as follows, using JSON format for clarity:
{response_json}
"""

#input prompt
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone",'response_json'],
    template=TEMPLATE
)


quiz_generator_chain = LLMChain(llm = llm, prompt = quiz_generation_prompt, output_key='quiz_questions', verbose=True)


#Now imporoving the response by evaluating it with another llm chain and improving the response further 

EVALUATION_TEMPLATE = """
As an expert in English grammar and writing, you have been presented with a Multiple Choice Quiz intended for {subject} students. Your task is to evaluate the complexity of the questions and provide a comprehensive analysis of the quiz. Offer concise feedback, limited to 50 words per question, addressing the cognitive and analytical demands posed by the quiz. If necessary, suggest modifications to the questions that will better align with the students' abilities.

Quiz MCQs:
{quiz_questions}

Based on your expertise as an English Writer, provide your critique and suggested enhancements for the quiz above:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz_questions"],
    template=EVALUATION_TEMPLATE
)
#creating LLM chain by combining both model and prompt 
quiz_review_chain = LLMChain(llm= llm, prompt=quiz_evaluation_prompt, verbose=True, output_key='quiz_review')


#Final chain combining bothe hte chains 
final_chain = SequentialChain(chains=[quiz_generator_chain,quiz_review_chain], input_variables=["text", "number", "subject", "tone",'response_json'],output_variables=['quiz_questions','quiz_review'],verbose=True)
