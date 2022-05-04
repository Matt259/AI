import numpy as np
import random
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nltk_utils import bag_of_words, tokenize, stem
from model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)

all_words = []
tags = []
#each string of patterns from the json with the tag next to it
xy = []

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    tag = intent['tag']
    # add to tag list
    tags.append(tag)
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = tokenize(pattern)
        # add to our words list
        all_words.extend(w)
        # add to xy pair
        xy.append((w, tag))

# stem and lower each word
ignore_words = ['?', '.', '!', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]

#Json pattern words with applied nltk
all_words = sorted(set(all_words))
# json tags; remove duplicates and sort
tags = sorted(set(tags))



# create training data
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: bag of words for each pattern_sentence, gathering training data
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)



    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)



#Hyper parameters
num_epochs = 1000 #Each full pass through dataset
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
#output size which is based on the amount of tags(functions)
output_size = len(tags)


#dataset map style class to feed into dataloader
class TalkDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples


dataset = TalkDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss() #Checks how far off the classifications are from reality

optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate) #adjusts the models weights and other params over time slowly

# Train the model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        # Forward function from model class
        outputs = model(words)
        #calculates the loss
        loss = criterion(outputs, labels)

        # Backward and optimize the loss
        optimizer.zero_grad()
        loss.backward()

        optimizer.step() # attempt to optimize weights to account for loss/gradients


#neuralNet data
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pt"
torch.save(data, FILE)


