#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import usb.core
from mic_array_tuning import Tuning


class MicArray(object):
    def __init__(self):
        self.dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
        if not self.dev:
            raise RuntimeError("Error, could not initialize mic array.")
        self.tuning = Tuning(self.dev)

    def getDoa(self):
        return self.tuning.direction
    
    def getIsSpeech(self):
        return self.tuning.is_speech()

    def doa2YawDelta(self, doa):
        yawDelta = doa - 90
        if yawDelta >= 180:
            yawDelta = yawDelta - 360
        return yawDelta

def test():
    m = MicArray()
    # obtain audio from the microphone
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    while True:
        with sr.Microphone() as source:
            print("Say something!")
            try:
                audio = r.listen(source, None, None, None, m.getIsSpeech)
                print("Vosk recognizer thinks you said " + r.recognize_vosk(audio))
            except sr.UnknownValueError:
                print("Vosk recognizer could not understand audio")
            except sr.RequestError as e:
                print("Vosk recognizer error; {0}".format(e))
            except sr.WaitTimeoutError:
                print("listening timed out")
            except KeyboardInterrupt:
                break
