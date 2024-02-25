import re
import nltk
from nltk.corpus import stopwords
from nltk import FreqDist, bigrams
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from gpt_generic import summarize
from openai import OpenAI
import json
import random
import configparser

config = configparser.ConfigParser()
config.read('api_config.ini')
openai_key = config['DEFAULT']['OPENAI_API_KEY']

# Ensure you've downloaded the necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Updated analyze_text function to filter for nouns
def analyze_text(sections):
    # Concatenate sections into a single string
    full_text = ' '.join(sections)

    # Tokenize the text
    tokens = word_tokenize(full_text)
    
    # Perform POS tagging on the tokens
    tagged_tokens = pos_tag(tokens)
    
    # Filter for nouns only; NN (singular noun), NNS (plural noun), NNP (proper noun, singular), NNPS (proper noun, plural)
    nouns = [word.lower() for word, tag in tagged_tokens if tag in ('NN', 'NNS', 'NNP', 'NNPS')]

    # Load stop words
    stop_words = set(stopwords.words('english'))
    
    names = ["patrick", "andre", "dennis", "lisa", "david"]
    
    # Further filter nouns by removing stop words
    nouns = [noun for noun in nouns if noun not in stop_words and noun.isalpha()]
    nouns = [noun for noun in nouns if noun not in names]

    # Frequency distribution of nouns
    freq_dist = FreqDist(nouns)

    # Most common nouns
    most_common_nouns = freq_dist.most_common(100)

    # Bigrams (common noun pairs)
    common_bigrams = FreqDist(bigrams(nouns)).most_common(100)

    return most_common_nouns, common_bigrams

# Function to perform basic NLP analysis on the text
def perform_nlp_analysis(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Convert all tokens to lowercase
    tokens = [token.lower() for token in tokens if token.isalpha()]  # Remove punctuation
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Frequency distribution of words
    freq_dist = FreqDist(tokens)
    
    # Most common words
    most_common_words = freq_dist.most_common(100)
    
    # Bigrams (common word pairs)
    common_bigrams = FreqDist(bigrams(tokens)).most_common(100)
    
    return most_common_words, common_bigrams

# Function to clean individual sections
def clean_section(text):
    # Normalize whitespace by replacing sequences of whitespace characters with a single space
    text = re.sub(r'\s+', ' ', text)
    # Additional cleaning rules can go here (e.g., removing non-printable characters)
    return text.strip()

# Example modified function to process the file and return a single string for analysis
def process_text_file_for_analysis(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content)
    return content

# Enhanced function to read and process the file, including data cleaning
def process_text_file(file_path):
    sections = []  # Initialize an empty list to store sections
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Split the content based on two newlines, which indicates 2 lines of space
        raw_sections = content.split('\n\n\n')
        # Clean and store each section
        sections = [clean_section(section) for section in raw_sections]
    return sections

# Function to find sections containing the given keyword
def find_sections_with_keyword(sections, keyword):
    matching_sections = []
    for i, section in enumerate(sections, start=1):
        if keyword.lower() in section.lower():  # Case-insensitive search
            matching_sections.append((i, section))
    return matching_sections

# Example usage
file_path = 'data/col_findings.txt'
sections = process_text_file(file_path)  # Read and store sections from the file

# Function to display sections containing the keyword
def display_matching_sections(keyword):
    li = []
    matching_sections = find_sections_with_keyword(sections, keyword)
    if not matching_sections:
        print(f"No sections found containing the keyword '{keyword}'.")
    else:
        for section_num, section_text in matching_sections:
            print(f"Section {section_num} contains the keyword '{keyword}':\n{section_text}\n")
            li.append(section_text)
    return li

# Replace 'keyword' with the actual keyword you're searching for
key_word = "game"
summaries = display_matching_sections(key_word)
sections = process_text_file(file_path)  # Assuming this function is already defined as provided
most_common_nouns, common_bigrams = analyze_text(sections)
print("Most Common Nouns:", most_common_nouns)
#most_common_nouns = most_common_nouns.pop(0)

#### New section to generate ideas based on the most common nouns ####

######PERSONAL JESUS EXECUTION########
'''
def display_matching_sections_gpt(keyword):
    li = []
    matching_sections = find_sections_with_keyword(sections, keyword)
    if not matching_sections:
        print(f"No sections found containing the keyword '{keyword}'.")
    else:
        selected_sections = random.sample(matching_sections, min(len(matching_sections), 2))
        for section_num, section_text in selected_sections:
            #print(f"Randomly selected Section {section_num} contains the keyword '{keyword}':\n{section_text}\n")
            li.append(section_text)
    return li

tools = [
    {
    "type": "function",
    "function": {
        "name": "chose_three_topics",
        "parameters": {
            "type": "object",
            "properties": {
                "three_topics_from_nouns": {
                    "type": "array",
                    "description": "Select three nouns from the list. Dont choose 'Timothy'.",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": [
            "three_topics_from_nouns"
            ]
        },
        "description": "Choose three nouns from the list of most common nouns."
        }
    }
]

model = "gpt-4-0125-preview"

client = OpenAI(
  api_key=openai_key,
)

messages = [
    {"role": "system", "content": f"""
    """},
    {"role": "user", "content": f"""
    This is the list of common nouns. Please choose three nouns from the list to generate ideas for the next project:
    
    {most_common_nouns}
    
    """}
]

def chat_completion_request(messages, model=model, temperature=0.3):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=250,
        )
        response = completion.choices[0].message.content
        
        return response
    
    except Exception as e:
        print(f"Unable to generate ChatCompletion response: {e}")
        return None

def chat_completion_request_incl_function(messages, tools=None, model=model, tool_choice=None, temperature=0.1):
    try:    
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=temperature
        )
        response = completion.choices[0]
        #print(response)
        return response
    except Exception as e:
        print(f"Unable to generate ChatCompletion response: {e}")
        return None

response_func = chat_completion_request_incl_function(messages, tools=tools, tool_choice={"type": "function", "function": {"name": "chose_three_topics"}}, model=model)
json_output = json.loads(response_func.message.tool_calls[0].function.arguments)
three_nouns = json_output.get('three_topics_from_nouns')

print("three nouns: ", three_nouns)

jesus_input = []
for noun in three_nouns:
    summaries = display_matching_sections_gpt(noun)
    #print("summaries: ", summaries)
    for summa in summaries:
        #print("summa: ", summa)
        jesus_input.append(summa)

#print("jesus:     ", jesus_input)

prompt = f"""
You are provided with 6 sections of text. Each section contains information about a different topic. Your task is to generate ideas for the next project based on the information provided in the sections. 
You should combine the information from the sections to generate the ideas. 

Generate 1x idea  - be creative and innovative. Dont be boring! But the idea has to be realistic and feasible.
This one idea will be the next thing he does. One thing. Keep the answer short.

The six sections / topics are: 
#1: {jesus_input[0]}, 
#2: {jesus_input[1]}, 
#3: {jesus_input[2]},
#4: {jesus_input[3]},
#5: {jesus_input[4]},
#6: {jesus_input[5]}.

"""

messages=[
        {"role": "system", "content": "You are generating ideas for future projects based on the provided information by Timothy."},
        {"role": "user", "content": f"{prompt}"}
    ]

response = chat_completion_request(messages)

print("final Jesus response:    ", response)
'''