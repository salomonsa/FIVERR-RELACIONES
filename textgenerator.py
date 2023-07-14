import openai
import os
import re
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_TOKEN')

def get_completion(prompt, model="gpt-3.5-turbo"): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.77, # this is the degree of randomness of the model's output
        max_tokens=2500
    )
    return response.choices[0].message["content"]

title="El poder de los conflictos en la relación"
duration=10
minwords=duration*150
maxwords=minwords+100

prompt1 = f"""
Your task is to generate a text oriented to a general public about the subject of the title.

Generate the text using the title below, which is delimited by triple 
backticks, in at most {minwords} words.

Title: ```{title}```
"""
response = get_completion(prompt1)
i=0
palabras=len(re.findall(r'\w+', response))
while palabras<minwords:
    prompt2 = f"""
    Your task is to rewrite a text and do it longer.

    Rewrite the text, delimited by triple backticks, so it's longer than the original but no longer than {maxwords} words.

    Text: ```{response}```
    """
    response = get_completion(prompt2)
    palabras=len(re.findall(r'\w+', response))
    i+=1
    print("\ni: "+str(i))
    print("\npalabras: "+str(palabras))
    #print("\n\nRESPONSE: "+response)


print("\nRESPONSE: "+response)
