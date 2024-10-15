import pyttsx3

# pip install comtypes
# pip install pyttsx3 <- Not this one!
# pip install py3-tts

class Voice:
    def __init__(self):
        self.engine = pyttsx3.init("sapi5")
        voice = self.engine.getProperty("voices")
        self.engine.setProperty('voice', voice[0].id)

    def speak(self, msg):
        self.engine.say(msg)
        self.engine.runAndWait()
        
voice = Voice()
voice.speak("Hello")