import datetime
import webbrowser as wb
import keyboard
import pywhatkit as kit
import os
import pyjokes



def get_weather():
    pass

def youT(name):
    kit.playonyt(name)

def spotify():
    os.startfile(r'C:\Users\EazyDuzIt\AppData\Roaming\Spotify\Spotify.exe')

def google(name):
    kit.search(name)

def wiki(name):
    wb.open('https://en.wikipedia.org/wiki/' + name)

def joke():
    return pyjokes.get_joke(language="en", category="neutral")


