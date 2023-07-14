from TTS.streamlabs_polly import StreamlabsPolly
from mutagen.mp3 import MP3
import random, os
import argparse
import json
import time
import requests
import tqdm
import pexelsPy
from moviepy.editor import concatenate_audioclips, AudioFileClip
from moviepy.editor import *
from dotenv import load_dotenv
import re

def download_video(type_of_videos,i,duration):
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
        for data in videos:
            if data.width > data.height and data.duration>=duration*0.5: #look for horizontal orientation videos
                # write_file('downloaded_files.txt', data.url)
                url_video = 'https://www.pexels.com/video/' + str(data.id) + '/download' #create the url with the video id
                r = requests.get(url_video,headers = {'Authorization': PEXELS_API})
                with open('./stockvideos/'+str(i)+'.mp4', 'wb') as outfile:
                    outfile.write(r.content)
                return './stockvideos/'+str(i)+'.mp4' #download the video
        num_page += 1
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
        for data in videos:
            if data.width < data.height and data.duration>=duration*0.5: #look for horizontal orientation videos
                # write_file('downloaded_files.txt', data.url)
                url_video = 'https://www.pexels.com/video/' + str(data.id) + '/download' #create the url with the video id
                r = requests.get(url_video,headers = {'Authorization': PEXELS_API})
                with open('./stockvideos/'+str(i)+'.mp4', 'wb') as outfile:
                    outfile.write(r.content)
                return './stockvideos/'+str(i)+'.mp4' #download the video
        num_page += 1

def video(division, tematicas, duration):
    voices = [
            "Brian",
            "Russell",
            "Joey",
            "Matthew"
        ]   
    voice = random.choice(voices)
    audioclips=[]
    lengths=[]
    acclengths=[]
    length=0
    if duration>1:
        for i in range(0, len(division)):
            mytext=division[i]
            if ('!' in mytext):
                mytext=mytext.replace('!','')
            try:
                # Passing the text and language to the engine, 
                # here we have marked slow=False. Which tells 
                # the module that the converted audio should 
                # have a high speed
                StreamlabsPolly.run(StreamlabsPolly, mytext, './speech/'+str(i)+'.mp3',voice)
                
                # Saving the converted audio in a mp3 file named
                # welcome 
                
                audio = MP3("./speech/"+str(i)+".mp3")
                audiolength=audio.info.length
                audioclips.append(
                    AudioFileClip("./speech/"+str(i)+".mp3")       
                )
                length=length+audiolength
                lengths.append(audiolength)
                acclengths.append(length)
            except (AssertionError):
                if os.path.exists("./speech/"+str(i)+".mp3"):
                    os.remove("./speech/"+str(i)+".mp3")
            except (ValueError):
                if os.path.exists("./speech/"+str(i)+".mp3"):
                    os.remove("./speech/"+str(i)+".mp3")
            except (NameError):
                print("Enter input again")
        videoclips=[]
        if length>=(duration*60-20):
            for i,tematica in enumerate(tematicas):
                download_video(tematica,i,lengths[i])
                clip = VideoFileClip("./stockvideos/"+str(i)+".mp4")
                clipduration=clip.duration
                if clipduration<lengths[i]:
                    clip=clip.fx( vfx.speedx, clipduration/lengths[i])
                else:
                    clip=clip.subclip(0,lengths[i])
                videoclips.append(clip)
            video_concat=concatenate_videoclips(videoclips)
            video_concat=video_concat.without_audio()
            audio_concat=concatenate_audioclips(audioclips)
            new_audioclip = CompositeAudioClip([audio_concat])
            video_concat.audio=new_audioclip
            textos=[]
            for i,texto in enumerate(division):
                textos.append(TextClip(
                texto,
                font='Amiri-Bold',
                fontsize=100,
                color='white',
                method='caption',
                size=(video_concat.size[0]*0.1, None),
                stroke_color='black',
                stroke_width=4
                ).set_duration(lengths[i]))
            text_concat = concatenate_videoclips(textos).set_position("bottom")
            final=CompositeVideoClip([video_concat, text_concat])
            return final
        else:
            if length*1.25>=(duration*60-20):
                ratio=length/(duration*60-20)
                audio_concat=concatenate_audioclips(audioclips)
                new_audioclip = CompositeAudioClip([audio_concat])
                new_audioclip=new_audioclip.fx( vfx.speedx, ratio)
                for lent in lengths:
                    lent=lent*(2-ratio)
                for i,tematica in enumerate(tematicas):
                    download_video(tematica,i,lengths[i])
                    clip = VideoFileClip("./stockvideos/"+str(i)+".mp4")
                    clipduration=clip.duration
                    if clipduration<lengths[i]:
                        clip=clip.fx( vfx.speedx, clipduration/lengths[i])
                    else:
                        clip=clip.subclip(0,lengths[i])
                    videoclips.append(clip)
                video_concat=concatenate_videoclips(videoclips)
                video_concat=video_concat.without_audio()
                video_concat.audio=new_audioclip
                textos=[]
                for i,texto in enumerate(division):
                    textos.append(TextClip(
                    texto,
                    font='Amiri-Bold',
                    fontsize=100,
                    color='white',
                    method='caption',
                    size=(video_concat.size[0]*0.1, None),
                    stroke_color='black',
                    stroke_width=4
                    ).set_duration(lengths[i]))
                text_concat = concatenate_videoclips(textos).set_position("bottom")
                final=CompositeVideoClip([video_concat, text_concat])
                return final
            else:
                length=length*1.25
                sum=((duration*60-20)-length)/len(division)
                audio_concat=concatenate_audioclips(audioclips)
                new_audioclip = CompositeAudioClip([audio_concat])
                new_audioclip=new_audioclip.fx( vfx.speedx, 0.75)
                lengths2=[]
                for lent in lengths:
                    lent=lent*1.25
                    lengths2.append(lent+sum)
                for i,tematica in enumerate(tematicas):
                    download_video(tematica,i,lengths2[i])
                    clip = VideoFileClip("./stockvideos/"+str(i)+".mp4")
                    clipduration=clip.duration
                    if clipduration<lengths2[i]:
                        clip=clip.fx( vfx.speedx, clipduration/lengths2[i])
                    else:
                        clip=clip.subclip(0,lengths2[i])
                    videoclips.append(clip)
                video_concat=concatenate_videoclips(videoclips)
                video_concat=video_concat.without_audio()
                video_concat.audio=new_audioclip
                textos=[]
                for i,texto in enumerate(division):
                    textos.append(TextClip(
                    texto,
                    font='Amiri-Bold',
                    fontsize=100,
                    color='white',
                    method='caption',
                    size=(video_concat.size[0]*0.1, None),
                    stroke_color='black',
                    stroke_width=4
                    ).set_duration(lengths[i]))
                text_concat = concatenate_videoclips(textos).set_position("bottom")
                final=CompositeVideoClip([video_concat, text_concat])
                return final
    else:
        for i in range(0, len(division)):
            mytext=division[i]
            if ('!' in mytext):
                mytext=mytext.replace('!','')
            try:
                # Passing the text and language to the engine, 
                # here we have marked slow=False. Which tells 
                # the module that the converted audio should 
                # have a high speed
                StreamlabsPolly.run(StreamlabsPolly, mytext, './speech/'+str(i)+'.mp3',voice)
                
                # Saving the converted audio in a mp3 file named
                # welcome 
                
                audio = MP3("./speech/"+str(i)+".mp3")
                audiolength=audio.info.length
                audioclips.append(
                    AudioFileClip("./speech/"+str(i)+".mp3")       
                )
                length=length+audiolength
                lengths.append(audiolength)
                acclengths.append(length)
            except (AssertionError):
                if os.path.exists("./speech/"+str(i)+".mp3"):
                    os.remove("./speech/"+str(i)+".mp3")
            except (ValueError):
                if os.path.exists("./speech/"+str(i)+".mp3"):
                    os.remove("./speech/"+str(i)+".mp3")
            except (NameError):
                print("Enter input again")
        videoclips=[]
        if length<60:
            for i,tematica in enumerate(tematicas):
                download_shorts(tematica,i,lengths[i])
                clip = VideoFileClip("./stockvideos/"+str(i)+".mp4")
                clipduration=clip.duration
                if clipduration<lengths[i]:
                    clip=clip.fx( vfx.speedx, clipduration/lengths[i])
                else:
                    clip=clip.subclip(0,lengths[i])
                videoclips.append(clip)
            video_concat=concatenate_videoclips(videoclips)
            video_concat=video_concat.without_audio()
            audio_concat=concatenate_audioclips(audioclips)
            new_audioclip = CompositeAudioClip([audio_concat])
            video_concat.audio=new_audioclip
            textos=[]
            ratios=[]
            i=0
            for texto in division:
                texto=texto.replace("\"", '')
                texto=re.split(r'[^\w\s\'\"!]', texto)
                total=0
                min=i
                for j in texto:
                    ratios.append(len(j))
                    total=total+len(j)
                    i+=1
                for j in range(min,i):
                    ratios[j]=ratios[j]/total
            i=0
            for texto in division:
                for j in texto:
                    textos.append(TextClip(
                    texto,
                    font='Amiri-Bold',
                    fontsize=100,
                    color='white',
                    method='caption',
                    size=(video_concat.size[0]*0.8, None),
                    stroke_color='black',
                    stroke_width=4
                    ).set_duration(lengths[i]*ratios[i]))
                    i+=1
            text_concat = concatenate_videoclips(textos).set_position("center")
            final=CompositeVideoClip([video_concat, text_concat])
            return final
        else:
            for i,audios in enumerate(audioclips):
                audios=audios.fx( vfx.speedx, length/59)
                lengths[i]=(59/length)*lengths[i]
            for i,tematica in enumerate(tematicas):
                download_shorts(tematica,i,lengths[i])
                clip = VideoFileClip("./stockvideos/"+str(i)+".mp4")
                clipduration=clip.duration
                if clipduration<lengths[i]:
                    clip=clip.fx( vfx.speedx, clipduration/lengths[i])
                else:
                    clip=clip.subclip(0,lengths[i])
                videoclips.append(clip)
            video_concat=concatenate_videoclips(videoclips)
            video_concat=video_concat.without_audio()
            audio_concat=concatenate_audioclips(audioclips)
            new_audioclip = CompositeAudioClip([audio_concat])
            video_concat.audio=new_audioclip
            textos=[]
            ratios=[]
            i=0
            for texto in division:
                texto=texto.replace("\"", '')
                texto=re.split(r'[^\w\s\'\"!]', texto)
                print(texto)
                total=0
                min=i
                for j in texto:
                    ratios.append(len(j))
                    total=total+len(j)
                    i+=1
                for j in range(min,i):
                    ratios[j]=ratios[j]/total
            i=0
            c=0
            print(ratios)
            print(division)
            for texto in division:
                for j in texto:
                    textos.append(TextClip(
                    j,
                    font='Amiri-Bold',
                    fontsize=100,
                    color='white',
                    method='caption',
                    size=(video_concat.size[0]*0.8, None),
                    stroke_color='black',
                    stroke_width=4
                    ).set_duration(lengths[c]*ratios[i]))
                    i+=1
                c+=1
            text_concat = concatenate_videoclips(textos).set_position("center")
            final=CompositeVideoClip([video_concat, text_concat])
            return final
            
