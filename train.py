import json
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
with open('College-Chat-Bot-main\originalintents.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)
def preprocess_text(text):
    words = word_tokenize(text)
    lem = WordNetLemmatizer()
    stopword = stopwords.words('english')
    final=[]
    for word in words:
        if word.isalpha():
            final.append(lem.lemmatize(word.lower()))
    return ' '.join(final)
vectorizer = CountVectorizer()
train_text=[]
for intent in intents['intents']:
    for pattern in intent['patterns']:
         train_text.append(preprocess_text(pattern))
vectorizer.fit(train_text)
patterns=[]
tags=[]
responses={}
for intent in intents['intents']:
    responses[intent['tag']]=intent['responses']
    for pattern in intent['patterns']:
          patterns.append(vectorizer.transform([preprocess_text(pattern)]).toarray())
          tags.append(intent['tag'])
train_model = {'model':vectorizer,'pattern':patterns,'tag':tags,'response':responses}

np.save('model.npy', train_model)