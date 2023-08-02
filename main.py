from videogenerador import *
from textgenerator import *
import ast
from moviepy.editor import *
from moviepy.config import change_settings
from upload import subida


change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

cleanup_folders()
ok=""
while not(ok=="si" or ok=="Si" or ok=="sí" or ok=="Sí") or len(title)<3:
    title=input("\nIntroduzca el título del vídeo deseado: ")
    ok=input(f"\nEl titulo será: {title}. ¿Está de acuerdo?(responde si o no) ")
    if(len(title)<3):
        print("El titulo es demasiado corto, introduce otro.")

done=False
while not done:
    try:
        duration=float(input("\nIntroduzca la duración deseada del vídeo (en minutos, para Shorts introduce un número igual o menor a 1): "))
        done=True
    except Exception as e:
        print("Introduzca un valor posible ej: 4, 2.5, 0.7")

#json.loads(x)
voz=""

while not(voz=="1" or voz=="2"):
    voz=(input("\nIntroduce 1 para voz masculina o 2 para voz femenina: "))




done=False
while done==False:
    try:
        print("\n\nGenerando guión...")
        guion=Creadortexto(title,duration)
        #print("\nGuión: "+guion)
        done=True

    except openai.error.ServiceUnavailableError as e:
        print("Service is overloaded. Retrying...")
        time.sleep(15) 

    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

done=False
while not done:
    try:
        lista=jasonmomoa(guion)
        print("\nGuión creado con exito.")
        descripcion=lista[0]
        tags=lista[1]
        division=lista[2]
        tematicas=lista[3]
        done=True

    except openai.error.ServiceUnavailableError as e:
        print("Service is overloaded. Retrying...")
        time.sleep(15) 
                
    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")
            
    except IndexError as e:
        print("No se encontraron videos que encajen con el guión, se reescribirá este")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        cleanup_folders()

done=False
while not done:
    try:
        print("\n\nMontando video...")
        final=video(division,tematicas,duration,voz)
        done=True

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        cleanup_folders()

        time.sleep(30)


final.write_videofile("./output/"+title+".mp4")
print("\nSubiendo video a Youtube")
subida("./output/"+title+".mp4",title,descripcion,tags)
print("\nEl video se ha subido con exito")

