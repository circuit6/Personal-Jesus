from openai import OpenAI
import re
from datetime import datetime
import pandas as pd
import time

def jesus_reads_your_message(text):
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

    completion = client.chat.completions.create(
    model="local-model", # this field is currently unused
    messages=[
        {"role": "system", "content": f"""
         You are analyzing the ideas, dreams, wishes and life-experiences of Timothy. Summarize any noteworthy facts on the basis of the provided batch of messages.
        """},
        {"role": "user", "content": f"""
         This is the next batch of messages:
         
         {text}.
         
         """}
    ],
    temperature=0.5,
    )
    print(completion.usage.total_tokens)
    return completion.choices[0].message.content

# Function to parse chat data from a given file
def parse_chat_data_from_file(file_path):
    messages = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r'\[(\d{2}\.\d{2}\.\d{2}), (\d{2}:\d{2}:\d{2})\] (\w+): (.*)', line)
            if match:
                date_str, time_str, author, message = match.groups()
                datetime_str = f"20{date_str} {time_str}"  # Assuming the year is 20xx
                datetime_obj = datetime.strptime(datetime_str, '%Y.%m.%d %H:%M:%S')
                messages.append({
                    'datetime': datetime_obj,
                    'author': author,
                    'message': message
                })
    return messages

def format_messages_for_model(df, batch_size):
    # List to hold the formatted strings for each batch
    batched_messages = []
    
    # Calculate the total number of batches
    total_batches = len(df) // batch_size + (1 if len(df) % batch_size else 0)
    
    for i in range(total_batches):
        # Extract a batch of messages
        batch_df = df.iloc[i*batch_size:(i+1)*batch_size]
        
        # Format each message in the batch
        formatted_messages = []
        for _, row in batch_df.iterrows():
            # Format: "Author: Message"
            formatted_message = f"{row['author']}: {row['message']}"
            formatted_messages.append(formatted_message)
        
        # Join all formatted messages in the batch into a single string
        # Each message is separated by a newline for clarity
        batch_str = "\n".join(formatted_messages)
        
        # Append the batch string to the list
        batched_messages.append(batch_str)
    
    return batched_messages

def process_messages_and_save_findings(df, batch_size):
    col_findings = []
    
    # Use the updated format_messages_for_model function
    batched_messages = format_messages_for_model(df, batch_size=batch_size)
    
    total_batches = len(batched_messages)
    start_time = time.time()  # Start timing
    
    for i, batch_str in enumerate(batched_messages, 1):
        # Call the hypothetical function and collect its response
        print("len of batch ", len(batch_str))
        response = jesus_reads_your_message(batch_str)
        col_findings.append(response)
        
        # Print progress and estimate time remaining
        elapsed_time = time.time() - start_time
        avg_time_per_batch = elapsed_time / i
        estimated_total_time = avg_time_per_batch * total_batches
        estimated_remaining_time = estimated_total_time - elapsed_time
        
        print(f"Processed batch {i}/{total_batches}. Estimated time remaining: {estimated_remaining_time:.2f} seconds.")
    
    # Save the findings to a text file
    findings_path = 'data/col_findings.txt'
    with open(findings_path, 'w', encoding='utf-8') as f:
        for finding in col_findings:
            f.write(f"{finding}\n\n")
    
    print(f"All batches processed. Findings have been saved to: {findings_path}")
    return findings_path

file_path = 'data/concatenated_files.txt'

# Parse the data from the file
messages = parse_chat_data_from_file(file_path)

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(messages)

# Calculate word count for each message
df['word_count'] = df['message'].apply(lambda x: len(x.split()))

# Calculate character count for each message (excluding spaces)
df['character_count'] = df['message'].apply(lambda x: len(x.replace(" ", "")))

# Summarize word count by author
word_count_by_author = df.groupby('author')['word_count'].sum().reset_index()
word_count_by_author = word_count_by_author.rename(columns={'word_count': 'total_word_count'})

# Summarize character count by author
character_count_by_author = df.groupby('author')['character_count'].sum().reset_index()
character_count_by_author = character_count_by_author.rename(columns={'character_count': 'total_character_count'})

# Display the summaries
print("Word Count by Author:")
print(word_count_by_author)

print("\nCharacter Count by Author:")
print(character_count_by_author)

# Calculate word count for each message
df['word_count'] = df['message'].apply(lambda x: len(x.split()))

# Calculate character count for each message (including spaces)
df['character_count'] = df['message'].apply(lambda x: len(x))

# Calculate average word count by author
avg_word_count_by_author = df.groupby('author')['word_count'].mean().reset_index()
avg_word_count_by_author = avg_word_count_by_author.rename(columns={'word_count': 'average_word_count'})

# Calculate average character count by author
avg_character_count_by_author = df.groupby('author')['character_count'].mean().reset_index()
avg_character_count_by_author = avg_character_count_by_author.rename(columns={'character_count': 'average_character_count'})

# Display the averages
print("Average Word Count by Author:")
print(avg_word_count_by_author)

print("\nAverage Character Count by Author:")
print(avg_character_count_by_author)

try:
    findings_path = process_messages_and_save_findings(df, 75)
except Exception as e:
    print("error: ", e)
    pass
#print(f"Findings have been saved to: {findings_path}")