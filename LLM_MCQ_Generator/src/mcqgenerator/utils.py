import os
import PyPDF2
import json
import traceback
import pandas as pd


def read_file(file):
    try:
        if file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        elif file.name.endswith(".txt"):
            # Your text file handling logic
            pass
        else:
            raise ValueError("Unsupported file format.")
    except PyPDF2.utils.PdfReadError as e:
        raise Exception(f"PyPDF2 error reading the PDF file: {e}")
    except Exception as e:
        raise Exception(f"General error reading the file: {e}")


def get_table_data(quiz_questions_str):
    try:
        # Convert the quiz from a string to a dictionary
        quiz_questions = json.loads(quiz_questions_str)
        
        # Normalize the JSON data into a flat table
        quiz_questions_df = pd.json_normalize(quiz_questions['questions'])
        
        # Convert options list to a newline-separated string
        quiz_questions_df['options'] = quiz_questions_df['options'].apply(lambda opts: '\n'.join(opts))

        return quiz_questions_df
    except Exception as e:
        # Print detailed traceback of the exception
        traceback.print_exception(type(e), e, e.__traceback__)
        return None  # Return None to indicate that the function did not complete successfully
    


