import datetime
import pandas as pd
import streamlit as st
from nlp import NLPProcessor
from datetime import datetime
import streamlit.components.v1 as components
from utils import read_json, add_entry, get_sentiment_text

# Globals
nlp = NLPProcessor()
DF = pd.DataFrame(read_json())

# Methods
def reload_dataframe():
    global DF
    DF = pd.DataFrame(read_json())

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
calendar_component = components.declare_component(
    "calendar_component",
    url="http://localhost:3001",
)
calendar = calendar_component(calendarName="Calendar", dataSource=DF.to_json())
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
    st.text(entry['text'])
    st.markdown("***")
        
'''
Try to cheer up if user feeling sad?
'''