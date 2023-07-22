import openai
import os
import re
from dotenv import load_dotenv, find_dotenv
import json
import ast
import time

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

def Creadortexto(title,duration,top):
    if duration>1:
        minwords=int(float(duration)*160)
    else:
        minwords=100
    maxwords=minwords+int(0.1*minwords)
    menor=True
    mayor=True
    if top=="si" or "Si" or "sí" or "Sí":
        prompt1 = f"""
        Tu trabajo es crear un top original de {minwords} palabras, debes crear el top en base al titulo de abajo entre triple tildes.
        Numera cada posición del top en orden descendente(3, 3a posicion. 2, 2a posicion. 1, 1a posicion).
        Adapta todo lo necesario el top para que no exceda las {maxwords} palabras en total.

        Titulo: ```{title}```
        """
    else:
        prompt1 = f"""
        Tu trabajo es generar un texto de {minwords} palabras, orientado a un publico general sobre el tema del titulo.

        Genera el texto usando el titulo de abajo, el cual se encuentra entre triple tildes, en como maximo {maxwords} palabras.

        Titulo: ```{title}```
        """
    response = get_completion(prompt1,0)
    i=0
    palabras=len(re.findall(r'\w+', response))
    if palabras>=minwords:
            menor=False
    while menor:
        prompt2 = f"""
        Tu trabajo es reescribir el texto dado y alargarlo.

        Reescribe el texto, delimitado por triple tildes, para que sea más largo que el original pero no más de {maxwords} palabras.

        Texto: ```{response}```
        """
        response = get_completion(prompt2,1)
        palabras=len(re.findall(r'\w+', response))
        if palabras>=minwords or i>4:
            menor=False
        i=i+1
    
    if palabras<=maxwords:
        mayor=False
    while mayor:
        prompt2 = f"""
        Tu trabajo es resumir el texto dado en {minwords}-{maxwords} palabras.

        Reescribe el texto, delimitado por triple tildes, para que sea más cortp que el original pero mayor de {minwords} palabras.

        Texto: ```{response}```
        """
        response = get_completion(prompt2,1)
        palabras=len(re.findall(r'\w+', response))
        if palabras<=maxwords or i>4:
            mayor=False
        i=i+1

    return response

    

def jasonmomoa(guion):
    division=[]
    tematicas=[]
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
    pdivision=get_completion(prompt3,0)
    division=ast.literal_eval(pdivision)
    
    for i,text in enumerate(division):
        prompt4=f"""
            Your task is to examine the sentiment of the text below, which is delimited by triple backticks(for exemple: happy, erotic, conflict).
            Examine the sentiment of the text and resume it in at most 2 or 3 words. 
            Your answer must only be the return of the resultant sentiment(always in english).

            Text: ```{text}```
            """
        tematicas.append(get_completion(prompt4,0))
        i+=1
        time.sleep(5)
    
    return [descripcion,tags,division,tematicas]

