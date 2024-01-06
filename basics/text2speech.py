# import pyttsx
# engine = pyttsx.init()
# rate = engine.getProperty('rate')
# engine.setProperty('rate', rate-40)
# engine.say('how are yo8u? 123456789 123 1 2 3 4 5 6 7 8 9')
# engine.runAndWait()

# REF: https://www.geeksforgeeks.org/convert-text-speech-python/
# https://www.geeksforgeeks.org/play-sound-in-python/
from gtts import gTTS
from playsound import playsound
import streamlit as st
import os
import uuid
import time

# TODO: (AWS Polly) https://docs.aws.amazon.com/polly/latest/dg/get-started-what-next.html

def play_text():
    txt = st.session_state['txtbox']
    myobj = gTTS(text=txt, lang='en', slow=False)

    #playsound assumes unix like paths (forward slash)
    # fpath = "./temp.mp3"
    # filename = "./" + str(uuid.uuid4()) + ".mp3"
    filename = "audio.mp3"
    # os.remove(filename)
    myobj.save(filename)
    time.sleep(1)

    # Playing the converted file
    if os.path.exists(filename):
        try:
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            st.write(e)
        
        

st.text_input('Enter the text to play', 'Hello', key='txtbox')
st.button('Play', on_click=play_text)