from openai import OpenAI

def summarize(li, filename, chunksize):
    # Helper function to yield chunks from list
    def yield_chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    filename = "outputs/" + filename + ".txt"
    with open(filename, 'w') as file:  # Open the file in write mode
        for chunk in yield_chunks(li, chunksize):
            # Combine chunk into a single string for processing
            chunk_text = "\n\n".join(chunk)
            # Point to the local server
            client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

            completion = client.chat.completions.create(
            model="local-model",  # this field is currently unused
            messages=[
                {"role": "system", "content": f"""
                Summarize any noteworthy facts on the basis of the provided batch of messages. You should focus on topics around the keyword {filename}.
                """},
                {"role": "user", "content": f"""
                These are the next batch of messages:
                
                {chunk_text}.
                
                """}
            ],
            temperature=0.2,
            max_tokens=750,
            )
            #print(completion.usage.total_tokens)  # Optional, for debugging
            # Write the completion to the file
            file.write(completion.choices[0].message.content + '\n\n')
            # Optionally, add a separator or identifier for different chunks
            file.write("-" * 40 + "\n\n")
