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
        