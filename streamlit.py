import datetime
import numpy as np
import pandas as pd
import streamlit as st
from nlp import NLPProcessor
from datetime import datetime
# import streamlit.components.v1 as components
from utils import read_json, add_entry, get_sentiment_text, get_emotion_scores

# Globals
nlp = NLPProcessor()
DATA = read_json()
DF = pd.DataFrame(DATA)

# Methods
def reload_dataframe():
    global DATA
    global DF
    DATA = read_json()
    DF = pd.DataFrame(DATA)

def post_entry():
    text = st.session_state.journal_entry
    sentiment = nlp.sentiment(text)
    sentiment = max(sentiment)
    entry = {
        'datetime':datetime.now().strftime("%d/%m/%Y"),
        'text':text,
        'sentiments':sentiment
    }
    add_entry(entry)
    reload_dataframe()    
    
# UI
# calendar_component = components.declare_component(
#     "calendar_component",
#     url="http://localhost:3001",
# )
# calendar = calendar_component(calendarName="Calendar", dataSource=DF.to_json())

# Data analysis UI
st.header('Sentiment Overview')
emotion_data = get_emotion_scores(DATA)

emotion_df = pd.DataFrame(
    [list(emotion_data.values())],
    columns=list(emotion_data.keys()),
)
st.bar_chart(data=emotion_df.T, width=0, height=0, use_container_width=True)

# Journal UI
journal_entry = st.text_area("Today's Entry", 
                            value="",
                            height=None,
                            max_chars=250,
                            key='journal_entry',
                            help=None,
                            on_change=None)


st.button("Submit",
          key='submit_entry',
          on_click=post_entry)


st.header('Journal Entries')
st.markdown(
    f"""<div style='text-align:center'>
         😠 Anger 🤢 Disgust 😨 Fear 😃 Joy 😐 Neutral 😔 Sad 😲 Suprise
    </div> <br>""", unsafe_allow_html=True)
st.markdown('***')
for i in reversed(DF.index):
    entry = DF.loc[i]
    # Headers
    col1, col2 = st.columns((10, 2))
    col1.subheader(f"Entry #{i+1}")
    col2.caption(f"{entry['datetime']}")
    
    # Values
    st.markdown(
        f"""<div style='text-align:center'>
            {get_sentiment_text(entry['sentiments'])}
        </div> <br>""", unsafe_allow_html=True)
    st.markdown(entry['text'])
    st.markdown("***")
        
# Data visulization
