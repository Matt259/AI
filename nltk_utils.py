import nltk
import numpy as np
nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

#NLP
# splits sentences into words
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

#takes the root of the word, also makes letters lower
def stem(word):
    return stemmer.stem(word.lower())

#replace with zeros and ones
def bag_of_words(tokenized_sentence, all_words):

    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w, in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag

