import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_TOKEN')

def get_completion(prompt, model="gpt-3.5-turbo"): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

title="El poder de los conflictos en la relación"

prompt1 = f"""
Your task is to generate a text oriented to a general public about the subject of the title.

Generate the text using the title below, delimited by triple 
backticks, in at most 200 words.

Title: {title}
"""
response1 = get_completion(prompt1)

prompt2 = f"""
Your task is to rewrite a text and doing it longer.

Rewrite the text, delimited by triple backticks, so it's longer than the original but no longer than 400 words.

Text: {response1}
"""
response2 = get_completion(prompt2)

print("\nRESPONSE 1: "+response1+"\n\n\nRESPONSE 2: "+response2)