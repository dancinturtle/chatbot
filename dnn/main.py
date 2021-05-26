import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle

""" Virtual env : conda activate chatbot """


with open('intents.json') as file:
  data = json.load(file)

try:
  # rb stands for read byte
  with open('data.pickle', 'rb') as f:
    words, labels, training, output = pickle.load(f)
except:
  words = []
  labels = []
  docs_x = []
  docs_y = []

  for intent in data['intents']:
    for pattern in intent['patterns']: # How are you
      # stemming - take each word in the pattern and bring it down to root word
      # there? => there
      # whats => what
      # tokenize - get all the words in the pattern. splitting
      wrds = nltk.word_tokenize(pattern) # this is a list ['How', 'are', 'you']
      words.extend(wrds) # without looping, just extend the list by another list
      docs_x.append(wrds) # [['How', 'are', 'you']]
      docs_y.append(intent['tag']) # ['greeting']
    if intent['tag'] not in labels:
      labels.append(intent['tag']) # ['greeting]

  words = [stemmer.stem(w.lower()) for w in words if w != '?'] # ['how', 'are', 'you']
  words = sorted(list(set(words))) # remove all duplicated

  labels = sorted(labels)

  # training and testing output
  # we need to turn the words into numbers since nn needs numbers
  # BAG OF WORDS
  # one hot encoding (present or not, does not consider frequency of words)

  training = []
  output = []
  out_empty = [0 for _ in range(len(labels))]

  for x, doc in enumerate(docs_x):
    bag = []
    wrds = [stemmer.stem(w) for w in doc] # ['how', 'are', 'you']
    for w in words:
      if w in wrds:
        bag.append(1)
      else:
        bag.append(0)
    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1 # greeting gets a 1
    training.append(bag)
    output.append(output_row)

  training = np.array(training)
  output = np.array(output)
  # save, use wb for write
  with open('data.pickle', 'wb') as f:
    pickle.dump((words, labels, training, output), f)

# Buiding the model with tflearn

tf.compat.v1.reset_default_graph()
# INPUT LAYER
# since we one hot encoded, all lengths of lists in training are the same
# tell the model that it should expect list of that length
net = tflearn.input_data(shape=[None, len(training[0])])
# HIDDEN LAYERS
# add this hidden layer with 8 neurons
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
# OUTPUT LAYER
# use softmax to get probabilities for each ouput neuron
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)
# try to load the existing fitted model
try:
  model.load('model.tflearn')
except:
  #FIT THE MODEL
  # pass x, y, epochs, batch, whether to show metrics
  model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
  model.save('model.tflearn')

# MAKE PREDICTIONS
# feed it bags of words, since that is how it was trained

def bag_of_words(s, words):
  bag = [0 for _ in range(len(words))]
  s_words = nltk.word_tokenize(s)
  s_words = [stemmer.stem(word.lower()) for word in s_words]
  for se in s_words:
    for i, w in enumerate(words):
      if w == se:
        bag[i] = 1
  return np.array(bag)

def chat():
  print('Start chatting with the bot (type "quit" to stop!)')
  while True:
    inp = input('You: ')
    if inp.lower() == 'quit':
      break
    # we'll get our probabilities from the predict
    results = model.predict([bag_of_words(inp, words)])[0]
    results_idx = np.argmax(results)
    tag = labels[results_idx]
    # threshold of confidence before responding
    # otherwise prompt to try again
    # reduce the seemingly random responses.
    if results[results_idx] > 0.4:
      for obj in data['intents']:
        if obj['tag'] == tag:
          responses = obj['responses']
          break
      print(random.choice(responses))
    else:
      print("You'll have to try that one again.")
chat()