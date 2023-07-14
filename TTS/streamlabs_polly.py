import random
import requests
from requests.exceptions import JSONDecodeError
from utils import settings
from utils.voice import check_ratelimit

voices = [
    "Brian",
    "Russell",
    "Joey",
    "Matthew",
    "Geraint",
    "Justin",
    
]


# valid voices https://lazypy.ro/tts/

def randomvoice(self):
    return random.choice(self.voices)
class StreamlabsPolly:
    def __init__(self):
        self.url = "https://streamlabs.com/polly/speak"
        self.max_chars = 550
        self.voices = voices
    random_voice=True
    
    def run(self,text, filepath,voice):
    
        
        body = {"voice": voice, "text": text, "service": "polly"}
        response = requests.post("https://streamlabs.com/polly/speak", data=body)
        if not check_ratelimit(response):
            self.run(self,text, filepath,voice)

        else:
            try:
                voice_data = requests.get(response.json()["speak_url"])
                with open(filepath, "wb") as f:
                    f.write(voice_data.content)
            except (KeyError, JSONDecodeError):
                try:
                    if response.json()["error"] == "No text specified!":
                        raise ValueError("Please specify a text to convert to speech.")
                except (KeyError, JSONDecodeError):
                    print("Error occurred calling Streamlabs Polly")


