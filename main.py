from videogenerador import *
from textgenerator import *
from subida import *
import ast
from moviepy.editor import *
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

cleanup_folders()
ok=""
while not(ok=="si" or ok=="Si" or ok=="sí" or ok=="Sí") or len(title)<3:
    title=input("\nIntroduzca el título del vídeo deseado: ")
    ok=input(f"\nEl titulo será: {title}. ¿Está de acuerdo?(responde si o no) ")
    if(len(title)<3):
        print("El titulo es demasiado corto, introduce otro.")

top=input("\n¿Quieres que el video tenga formato de top?(responde si o no) ")
while not(top=="si" or top=="Si" or top=="sí" or top=="Sí" or top=="no" or top=="No"):
    top=input("""\nSolo se acepta "si" o "no" como respuesta\n¿Quieres que el video tenga formato de top?(responde si o no)""")
duration=float(input("\nIntroduzca la duración deseada del vídeo (en minutos, para Shorts introduce un número igual o menor a 1): "))
#json.loads(x)
voz=""
while not(voz=="1" or voz=="2"):
    voz=(input("\nIntroduce 1 para voz masculina o 2 para voz femenina: "))

print("\n\nGenerando guión...")

done=False
while done==False:
    try:
        guion=Creadortexto(title,duration,top)
        done=True

    except openai.error.ServiceUnavailableError as e:
        print("Service is overloaded. Retrying...")
        time.sleep(15) 

    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

done=False
while done==False:
    try:
        lista=jasonmomoa(guion)
        done=True

    except openai.error.ServiceUnavailableError as e:
        print("Service is overloaded. Retrying...")
        time.sleep(15) 
        
    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")
        
    except Exception as e:
            print(f"An unexpected error occurred: {e}")
print("\nGuión creado con exito.")

descripcion=lista[0]
tags=lista[1]
division=lista[2]
tematicas=lista[3]

print("\n\nMontando video...")
final=video(division,tematicas,duration,voz)
final.write_videofile("./output/"+title+".mp4")
subida("./output/"+title+".mp4",title,descripcion,tags,"27")
