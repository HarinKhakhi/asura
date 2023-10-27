
from gtts import gTTS
import os
import playsound
tts = gTTS(text="harin", lang='en')
filename = "abc.mp3"
tts.save(filename)
playsound.playsound(filename)
os.remove(filename)
