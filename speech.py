from gtts import gTTS
def speech_it(text):
    tts = gTTS(text=text, lang='ru')
    name = "speeched.mp3"
    tts.save(name)
