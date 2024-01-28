# pip install SpeechRecognition
# pip install pyttsx3

import gtts as gs

from time import sleep
from pygame import mixer
from threading import Thread
from tempfile import TemporaryFile

from rc_utils.utils import *
from rc_utils.colores import *

string_global = ''

def recognizer_voice(recognizer, audio):
        global string_global
        
        # print("Reconociendo audio")
        try:
            transcription = recognizer.recognize_google(audio, language = 'es-AR')
            if "quiero" and "salir" in transcription:
                string_global = 'salir'

            elif "terminar" in transcription:
                string_global = 'terminar'           
                transcription = None
                
            elif "asistente" in transcription:
                string_global = transcription # Guarda la transcripcion en la variable global MI_STRING
                transcription = None # Limpia la variable transcription
            else:
                 transcription = None
        except Exception:
            transcription = None # Si no reconoce el audio limpia la variable transcription
            pass

def text_to_speech(texto):

    temp = TemporaryFile()
    resultado = gs.gTTS(texto, lang="es", lang_check=False)
    resultado.write_to_fp(temp)
    temp.seek(0)
    mixer.init()
    mixer.music.load(temp)
    mixer.music.play()
    while mixer.music.get_busy():  # Espera que finalice la reproduccion
            sleep(0.3)
    temp.close() # Una vez termine la reproduccion quitamos el mixer
    
def thread_text_to_speech(texto):     
     global tts_thread

     tts_thread = Thread(target=text_to_speech, args=(texto,))
     tts_thread.start()

def return_string():
     global string_global

     string = string_global
     string_global = ''

     return string