from openai import OpenAI
import re
from datetime import datetime
import pandas as pd
import time

def jesus_reads_your_message(context, current_message):
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

    messages_for_model = [
        {"role": "system", "content": f"""
         Curate the list of the top 10 traits, interests and major life happenings of Timothy. Keep the list structure as is and change, add, alter the bullets in the list.
         The headers above your list should always stay "traits, interests and major life happenings". Dont change the structure of the list.
         
         Here is the current list, you can append adjust this:
         
         ###List###:
         
         {context}
         
         
         ###EndList###
         
        """},
        {"role": "user", "content": f"""
         Please return the adjusted list of top traits, interests and major life happenings of Timothy based on this provided text:
         
         {current_message}
         
         """}
    ]

    completion = client.chat.completions.create(
        model="local-model", # this field is currently unused but signifies a placeholder for the model to use
        messages=messages_for_model,
        temperature=0.1,
    )

    print(completion.usage.total_tokens)
    return completion.choices[0].message.content


# Function to read statements from the file, where 2 lines of space separate each statement
def read_statements_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()
    # Splitting based on two newlines to separate each statement
    statements = content.split('\n\n\n')
    return statements

def process_statements_and_save_findings(file_path):
    statements = read_statements_from_file(file_path)
    col_findings = []
    context = ""
    for current_message in statements:
        if context == "":
            context = """
            Traits:
            - Empty item
            - [...]
            
            Interests:
            - Empty item
            - [...]

            Major life happenings:
            - Empty item
            - [...]
            
            """
        response = jesus_reads_your_message(context, current_message)
        context = response
        print(context)
        
    # Save the findings to a text file
    findings_path = 'data/timothy_top_10_insights.txt'
    with open(findings_path, 'w', encoding='utf-8') as f:
        for finding in col_findings:
            f.write(f"{finding}\n\n")
    
    print(f"All statements processed. Findings have been saved to: {findings_path}")

# Specify the path to your file
file_path = 'data/col_findings.txt'
process_statements_and_save_findings(file_path)
