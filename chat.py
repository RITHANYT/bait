import train
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random

import requests
from bs4 import BeautifulSoup
url = 'https://www.google.com/search?q='
def process_request(text):
    global url
    links=''
    bit='https://www.bitsathy.ac.in/'
    text=text.replace(' ','+')
    url=url+text+"+BAIT"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href')
        if 'https://www.bitsathy.ac.in/' in href:
            links=(href[7:].split('&')[0])
            break
    if(links[:10]!=bit[:10]):
        return ''
    return links
model = np.load('model.npy', allow_pickle=True).item()
def find_similar(matrix1,matrix2):
    matrix3=[]
    for i in range(len(matrix1)):
        l=[]
        for j in range(len(matrix1[0])):
            if(matrix1[i][j]==matrix2[i][j]):
                l.append(matrix1[i][j])
            else:
                l.append(0)
        matrix3.append(l)
    return matrix3
def getpattern(text):
    temp=text
    text = train.preprocess_text(text=text)
    sent1 = model['model'].transform([text]).toarray()
    scores={}
    index=0
    for pattern in model['pattern']:
        score = cosine_similarity(sent1, pattern)
        scores[score[0][0]]=index
        index+=1
    maxvalue = sorted(scores.keys())[-1]
    if(maxvalue>=0.7):
        tag = model['tag'][scores[maxvalue]]
        return random.choice(model['response'][tag])
    else:
          link = process_request(temp)
          if(len(link)!=0):
                text = 'Please Click the below to Explore Your Results <br> <a target=\"_blank\" style=\"color:white;\" href='+link+'>Click Here</a>'
                return  text
          responses = [
    "I'm sorry, but my knowledge is limited to the data I have been trained on.",
    "As an AI model, I have access to a large amount of information, but my knowledge is still limited to what has been programmed into me.",
    "While I may not have all the answers, I will do my best to provide accurate and helpful responses based on the data I have been trained on.",
    "I understand that my access to information is limited, but I am constantly learning and improving through ongoing training and updates.",
    "I may not have all the answers, but I can assist you to the best of my abilities based on the data and knowledge I have been programmed with.",
    "My knowledge is limited to what I have been trained on, but I am constantly expanding my understanding through ongoing updates and improvements.",
    "As an AI model, my access to information is limited, but I can provide helpful responses based on the data and knowledge I have been programmed with.",
    "While I may not know everything, I am here to assist you to the best of my abilities based on the information and data I have been trained on.",
    "I understand that my knowledge is limited, but I am constantly learning and improving through ongoing training and updates to provide the most accurate and helpful responses possible.",
    "I may not be able to answer all your questions, but I am always striving to improve my abilities and expand my knowledge through ongoing updates and training."]
          return random.choice(responses)
def process_text(request):
    response=getpattern(request)
    if "</a>" in response:
        return response
    else:
        return response.title()