# FIVERR-RELACIONES

Para instalar el programa escribe en la cmd, en la carpeta en la que quieras instalarlo: git clone https://github.com/salomonsa/FIVERR-RELACIONES

COSAS IMPORTANTES, LEER ANTES DE USAR EL PROGRAMA:

1. Cambia el nombre del archivo dotenv a .env, ábrelo y escribe tu token de API de OPENAI y tu token de API de PEXELS, los encontrarás en sus respectivas webs.

2. Instala todos los requisitos en el archivo requirements.txt. Utiliza el comando pip install -r requirements.txt para instalar todos los módulos y paquetes de Python que están enumerados en tu archivo requirements.txt. Además, y esto es ESENCIAL para que el programa funcione, instala por separado Imagemagick en su sitio web oficial.

3. Crea tu canal de Youtube si aún no existe y sigue los pasos de este video hasta llegar a tu Client ID y tu Client Secret: https://youtu.be/aFwZgth790Q (no es necesario hacerse una cuenta en google cloud, solo haz clic en consola cuando el tutorial lo haga), todo esto usando la cuenta del canal de Youtube al que quieras subir los videos. Una vez tengas tu Client ID y tu Client Secret sustityelos en el archivo "client_secrets.json".

4. Las carpetas stockvideos y speech no las debes tocar, en stockmusic has de meter los arhivos de música (mp3) que quieres que el video tenga, si metes una solo se repetirá en bucle durante todo el video, si metes varias el programa escogerá una al azar y la pondrá en bucle.

5. Cuando intentes correr el programa sea en la terminal o en VScode se te pedirá el titulo del video, la duración y el tipo de voz. Una vez elegidos el programa procede a crear el guión con OpenIA(lo cual suele ser ráìdo), seguidamente procede a montar el video, en esta parte pueden saltar algunos errores relacionados con limites de demandas a las APIs(en estos casos con esperar se arregla), y cuanto más largo sea el video mayor será la probabilidad de que estos aparezcan, por eso te recomiendo empezar probando el programa con videos cortos.

6. Al cambiar de dispositivo no es raro que aparezcan errores inesperados, si tienes alguna duda escribeme.


Algunos resultados del programa: https://www.youtube.com/channel/UCh-5_hTpJavkNrZf6NPT9yA
