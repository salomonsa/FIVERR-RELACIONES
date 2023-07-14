from videogenerador import *
from textgenerator import *
from subida import *
import ast
from moviepy.editor import *
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

title=input("Introduzca el título del vídeo deseado: ")
duration=float(input("Introduzca la duración deseada del vídeo (en minutos, para Shorts introduce un número igual o menor a 1): "))
#json.loads(x)
guion=Creadortexto(title,duration)
lista=jasonmomoa(guion)
descripcion=lista[0]
tags=lista[1]
division=ast.literal_eval(lista[2])
tematicas=ast.literal_eval(lista[3])
print(division)
print(tematicas)
final=video(division,tematicas,duration)
final.write_videofile("./output/"+title+".mp4")
subida("./output/"+title+".mp4",title,descripcion,tags,"27")