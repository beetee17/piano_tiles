from os import path
from pydub import AudioSegment
import wave

AudioSegment.converter="/Users/brandonthio/downloads/ffmpeg"
notes= ['A#','C#','D#','F#','G#']
fullnote= list()
for letter in notes:
    for i in range(2,7):
        newletter=str(letter)+str(i)
        fullnote.append(newletter)

    
def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

##for note in fullnote:
##    sound = AudioSegment.from_file("/Users/brandonthio/downloads/Piano Sharps/{}.wav".format(note), format="wav")
##    start_trim = detect_leading_silence(sound)
##    end_trim = detect_leading_silence(sound.reverse())
##    duration = len(sound)    
##    trimmed_sound = sound[start_trim:duration-end_trim]
##    trimmed_sound.export("/Users/brandonthio/downloads/Trimmed Piano Sounds/{}(trim).ogg".format(note), format="ogg")

sound = AudioSegment.from_file("/Users/brandonthio/downloads/F_BIRD_JUMP copy.wav")
start_trim = detect_leading_silence(sound)
end_trim = detect_leading_silence(sound.reverse())
duration = len(sound)    
trimmed_sound = sound[start_trim:duration-end_trim]
trimmed_sound.export("/Users/brandonthio/downloads/F_BIRD_JUMP1.ogg", format="ogg")
