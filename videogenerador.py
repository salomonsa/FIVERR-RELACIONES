from TTS.streamlabs_polly import StreamlabsPolly
from mutagen.mp3 import MP3
import random, os
import string
import time
import requests
import pexelsPy
from moviepy.editor import concatenate_audioclips, AudioFileClip
from moviepy.editor import *
from dotenv import load_dotenv
import re
from moviepy.video.fx import * 
from send2trash import send2trash
from textgenerator import *
import numpy as np


def download_video(type_of_videos,i,duration):
    from moviepy.editor import VideoFileClip
    from moviepy.video.fx.resize import resize

# ... rest of the code ...

    load_dotenv()  # take environment variables from .env.

    # Define the API key
    video_tag = type_of_videos
    PEXELS_API = os.getenv('PEXELS_API') #please add your API Key here
    api = pexelsPy.API(PEXELS_API) 
    video_found_flag = True
    num_page = 1
    
    while video_found_flag:
        
        api.search_videos(video_tag, page=num_page, results_per_page=40)
        videos = api.get_videos()
        aptos=[]
        for data in videos:
            if data.width > data.height and data.duration>=duration*0.2: #look for horizontal orientation videos
                aptos.append(data.id)
        id=random.choice(aptos)
        url_video = 'https://www.pexels.com/video/' + str(id) + '/download' #create the url with the video id
        r = requests.get(url_video,headers = {'Authorization': PEXELS_API})
        with open('./stockvideos/'+str(i)+'.mp4', 'wb') as outfile:
            outfile.write(r.content)
        num_page += 1
        return './stockvideos/'+str(i)+'.mp4' #download the video
        
def download_shorts(type_of_videos,i,duration):


    load_dotenv()  # take environment variables from .env.
    # Define the API key
    video_tag = type_of_videos
    PEXELS_API = os.getenv('PEXELS_API') #please add your API Key here
    api = pexelsPy.API(PEXELS_API) 
    video_found_flag = True
    num_page = 1
    
    while video_found_flag:

        api.search_videos(video_tag, page=num_page, results_per_page=40)
        videos = api.get_videos()
        aptos=[]
        for data in videos:
            if data.width < data.height and data.duration>=duration*0.2: #look for horizontal orientation videos
                aptos.append(data.id)
        id=random.choice(aptos)
        url_video = 'https://www.pexels.com/video/' + str(id) + '/download' #create the url with the video id
        r = requests.get(url_video,headers = {'Authorization': PEXELS_API})
        with open('./stockvideos/'+str(i)+'.mp4', 'wb') as outfile:
            outfile.write(r.content)
        num_page += 1
        return './stockvideos/'+str(i)+'.mp4' #download the video

def video(division, tematicas, duration,voz):
    if voz=="1":
        voices = [
            "Enrique",
            "Sergio"
            ]   
    else:
        voices = [
            "Conchita",
            "Lucia"
            ]   
    voice = random.choice(voices)
    audioclips=[]
    ftext = [[] for _ in range(40)]
    lengths=[]
    length=0
    video_concat=None

#VIDEOS

    for i in range(0, len(division)):
        div=division[i]
        if ('!' in div):
            div=div.replace('!','.')
        mytext=re.split(r'[.,;:¡!¿?()\-\[\]\'\"]+', division[i])
        mytext = [parte for parte in mytext if parte]
        modified_chunks = []
        for k in range(len(mytext)):
            palabras = mytext[k].split()
            if len(mytext[k]) > 40:
                grupos = [palabras[j:j+3] for j in range(0, len(palabras), 3)]
                modified_chunks.extend([' '.join(grupo) for grupo in grupos])
            else:
                modified_chunks.append(mytext[k])
        for text in modified_chunks:
            ftext[i].append(text)
        #print("\nmytext: ")
        #print(mytext)
        division[i]=remove_punctuation(division[i])
        done=False
        while not done:
            try:
                StreamlabsPolly.run(StreamlabsPolly, div, './speech/'+str(i)+'.mp3',voice)
                audio = MP3('./speech/'+str(i)+'.mp3')
                audiolength=audio.info.length
                audioclips.append(
                    AudioFileClip('./speech/'+str(i)+'.mp3')       
                )
                length=length+audiolength
                lengths.append(audiolength)
                done=True
                
            except (AssertionError):
                if os.path.exists('./speech/'+str(i)+'.mp3'):
                    os.remove('./speech/'+str(i)+'.mp3')
            except (ValueError):
                if os.path.exists('./speech/'+str(i)+'.mp3'):
                    os.remove('./speech/'+str(i)+'.mp3')
            except (NameError):
                print("Enter input again")
                time.sleep(30)
            
    ftext = [fila for fila in ftext if fila]
    
    videoclips=[]
    short=False
    for i,tematica in enumerate(tematicas):
        done=False
        while not done:
            try:
                if duration>1:
                    download_video(tematica,i,lengths[i])
                else:
                    download_shorts(tematica,i,lengths[i])
                    short=True
                done=True
            except IndexError as e:
                print("No se encontraron videos que encajen con el guión, se reescribirá este")
                tematica=sinonimo(tematica)
                print("Sinonimo: "+tematica)

            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                tematica=sinonimo(tematica)
                
        clip = VideoFileClip("./stockvideos/"+str(i)+".mp4")
        clipduration=clip.duration
        if clipduration<lengths[i]:
            clip=clip.fx( vfx.speedx, clipduration/lengths[i])
        else:
            clip=clip.subclip(0,lengths[i])
        if not short:
            clip=clip.resize(width=1920)
        else: 
            clip=clip.resize(height=1920)
        clip=clip.set_position(("center", clip.size[1] // 2))
        videoclips.append(clip)
    video_concat=concatenate_videoclips(videoclips)
    video_concat=video_concat.without_audio()
    audio_concat=concatenate_audioclips(audioclips)
    new_audioclip = CompositeAudioClip([audio_concat])
    video_concat.audio=new_audioclip
    textos=[]

    for i, fila in enumerate(ftext):
        for texto in fila:

            textos.append(TextClip(
            texto,
            font='Amiri-Bold',
            fontsize=120,
            color='white',
            method='caption',
            size=(video_concat.size[0]*0.8, None),
            stroke_color='black',
            stroke_width=5
            ).set_duration((sum(1 for char in texto if char.isalpha())/sum(1 for char in division[i] if char.isalpha()))*lengths[i]))
    text_concat = concatenate_videoclips(textos).set_position("center")

    final=CompositeVideoClip([video_concat, text_concat])

    if short:
        if final.duration>=60:
            factor_velocidad = final.duration/58
            final = final.fx(vfx.speedx, factor_velocidad)
            print("Velocidad: "+str(factor_velocidad))
        image_path = 'logo.png'  # Reemplaza con la ruta de tu imagen
        image_clip = ImageClip(image_path, transparent=True)
        image_width = 200  # Ancho de la imagen (puedes ajustar este valor)

        # Asegurarse de que la imagen no ocupe mucho espacio
        image_clip = image_clip.resize(width=image_width)

        # Ajustar la duración de la imagen al video principal
        image_clip = image_clip.set_duration(final.duration)

        x_position = final.w - image_width - 100 
        y_position = final.h - image_clip.size[1] - 200  
        image_clip = image_clip.set_position((x_position, y_position))
        image_clip=image_clip.set_opacity( 0.5)
        # Superponer el clip de imagen con el video principal
        final_video = CompositeVideoClip([final, image_clip])
    else:
        if final.duration<=duration*60-duration*5:
            factor_velocidad=0.90
            final = final.fx(vfx.speedx, factor_velocidad)
            print("Velocidad: "+str(factor_velocidad))
        if final.duration>duration*60+duration*5:
            factor_velocidad = 1.10
            final = final.fx(vfx.speedx, factor_velocidad)
            print("Velocidad: "+str(factor_velocidad))
        final_video=final

    archivos_stockmusic = os.listdir("stockmusic")
    archivos_mp3 = [archivo for archivo in archivos_stockmusic if archivo.lower().endswith(".mp3")]

    if archivos_mp3:

        nombre_musica = random.choice(archivos_mp3)
        ruta_musica = os.path.join("stockmusic", nombre_musica)
        musica = AudioFileClip(ruta_musica)
        duracion_video = final_video.duration
        musica_en_bucle = afx.audio_loop(musica, duration=duracion_video)

        audio_actual = final_video.audio
        nuevo_audio = CompositeAudioClip([audio_actual, musica_en_bucle.volumex(0.07)])
        final_video = final_video.set_audio(nuevo_audio)
        
    else:
        print("No se encontraron archivos MP3 en la carpeta 'stockmusic', el video no tendrá música.")

    return final_video

def remove_punctuation(input_string):
    translator = str.maketrans('', '', string.punctuation)
    return input_string.translate(translator)

def cleanup_folders():
    stockvideos_path = './stockvideos/'
    speech_path = './speech/'

    for folder_path in [stockvideos_path, speech_path]:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) and not filename.lower().endswith('.txt'):
                    # Intentar eliminar el archivo directamente
                    try:
                        os.unlink(file_path)
                    except Exception:
                        send2trash(file_path)
            except Exception as e:
                print(f"Error while processing {file_path}: {e}")
