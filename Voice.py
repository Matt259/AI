import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import pyttsx3 as tts
import speech_recognition as sr
from functions import spotify, wiki, google, youT, joke


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

FILE = "data.pt"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def predict(command):
    sentence = tokenize(command)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)
    ouput = model(X)
    _, predicted = torch.max(ouput, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(ouput, dim=1)
    prob = probs[0][predicted.item()]

    return prob, tag

def talk(audio):
    engine.say(audio)
    engine.runAndWait()

listener = sr.Recognizer()
engine = tts.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0])


def get_Command():
    command = ""
    while len(command) == 0:
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source)
                voice = listener.listen(source)
                command = listener.recognize_google(voice)
                command = command.lower()
        except:
            talk("Could you repeat that")
    return command




