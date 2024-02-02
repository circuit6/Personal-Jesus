import re
import nltk
from nltk.corpus import stopwords
from nltk import FreqDist, bigrams
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from gpt_generic import summarize

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
key_word = "GPT"
summaries = display_matching_sections(key_word)
#summarize(summaries, key_word, 25)

'''
sections = process_text_file(file_path)  # Assuming this function is already defined as provided
most_common_nouns, common_bigrams = analyze_text(sections)
print("Most Common Nouns:", most_common_nouns)
print("Common Bigrams of Nouns:", common_bigrams)
'''