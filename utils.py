import json
import pandas as pd

def read_json():
    with open('./data.json', 'r') as f:
        data = json.loads(f.read())['entries']
    return data
        
        
def add_entry(entry):
    with open('./data.json', 'r') as f:
        data = json.loads(f.read())
    entries = data['entries']
    entries.append(entry)
    with open('./data.json', 'w') as f:
        f.write(json.dumps({'entries':entries}))
    
        
def get_sentiment_text(scores):
    emojis = ['😠', '🤢', '😨', '😃', '😐', '😔', '😲']
    out = ''
    for i, score in enumerate(scores):
        out += emojis[i]
        out += f' {round(score["score"], 2)} '
    return out
        
        
def get_emotion_scores(entries):
    anger, disgust, fear, joy, neutral, sadness, surprise = \
        0,0,0,0,0,0,0
    for entry in entries:
        sentiments = entry['sentiments']
        for s in sentiments:
            if s['label'] == 'anger':
                anger += s['score']
            elif s['label'] == 'disgust':
                disgust += s['score']
            elif s['label'] == 'fear':
                fear += s['score']
            elif s['label'] == 'joy':
                joy += s['score']
            elif s['label'] == 'neutral':
                neutral += s['score']
            elif s['label'] == 'sadness':
                sadness += s['score']
            elif s['label'] == 'surprise':
                surprise += s['score']
    return {
       'anger': round(anger, 2),
       'disgust': round(disgust, 2),
       'fear': round(fear, 2),
       'joy': round(joy, 2),
       'neutral': round(neutral, 2),
       'sadness': round(sadness, 2),
       'surprise': round(surprise, 2),
    }
        