import openai
import os
import re
from dotenv import load_dotenv, find_dotenv
import json
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_TOKEN')

def get_completion(prompt, temp,model="gpt-3.5-turbo"): 
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temp, # this is the degree of randomness of the model's output
        max_tokens=2200
    )
    return response.choices[0].message["content"]
def Creadortexto(title,duration):
    minwords=float(duration)*150
    maxwords=minwords+100
    tru=True
    prompt1 = f"""
    Your task is to generate a text oriented to a general public about the subject of the title.

    Generate the text using the title below, which is delimited by triple 
    backticks, in at most {minwords} words.

    Title: ```{title}```
    """
    response = get_completion(prompt1,0.77)
    i=0
    palabras=len(re.findall(r'\w+', response))
    while tru:
        prompt2 = f"""
        Your task is to rewrite a text and do it longer.

        Rewrite the text, delimited by triple backticks, so it's longer than the original but no longer than {maxwords} words.

        Text: ```{response}```
        """
        response = get_completion(prompt2,0.77)
        palabras=len(re.findall(r'\w+', response))
        i=i+1
        if palabras>=minwords or i>4:
            tru=False
    return response

def jasonmomoa(guion):
    prompt=f"""
        Your task is to write a short 50 character description in spanish of the text below, which is delimited by triple backticks.

        Text: ```{guion}```
        """
    descripcion=get_completion(prompt,0.7)
    prompt2=f"""
        Your task is to write a string of 5 tags in spanish, separated from each other by commas, which represent the content of the text below, which is delimited by triple backticks.
        Text: ```{descripcion}```
        """
    tags=get_completion(prompt2,0.7)
    prompt3=f"""
        Your task is to divide the text below, which is delimited by triple backticks, into short 20 word (no longer than 25 words) parts (it must be done so in a way in which if one unites all of the parts, it generates the original text) and put them in a Python list.
        Text: ```{guion}```
        """
    division=get_completion(prompt3,0.2)
    prompt4=f"""
        Your task is to examine the sentiment/theme of each element of the list below (each sentiment/theme must be at most 3 words long), which is delimited by triple backticks, create a Python list containing these sentiments/themes in order translated to english. The number of elements in this list must be the same as the number as the number of elements in the list below delimited by triple backticks.

        Text: ```{division}```
        """
    tematicas=get_completion(prompt4,0.1)
    
    return [descripcion,tags,division,tematicas]

