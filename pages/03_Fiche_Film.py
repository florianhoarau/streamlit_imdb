import streamlit as st
import pandas as pd
import seaborn as sns
import operator
import requests
from unidecode import unidecode
from streamlit_extras.switch_page_button import switch_page

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YTM0OGExMDhjMDVlMzI4ZmNkOWY4OWJiMDRmYWU2OSIsIm5iZiI6MTczMzg0NTA4MS40MzIsInN1YiI6IjY3NTg2MDU5OTkzNTliMDQ2OGE0Njc3ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.iybQH84AcS6kz6Ryzl83Y9Lg1VLbxGJmUaUc1e0AR-Y"
}

urln = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/nconst.tsv.gz"
urlt = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/tconst.tsv.gz"
dfn = pd.read_csv(urln, sep='\t')
dft = pd.read_csv(urlt, sep='\t')

st.set_page_config(page_title="Fiche Film", page_icon="")
st.sidebar.header("Fiche Film")

st.write(st.session_state.tconst)
st.write(dft.loc[dft['tconst']==st.session_state.tconst]['title'])
