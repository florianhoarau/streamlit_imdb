import streamlit as st
import pandas as pd
import seaborn as sns
import operator
from pprint import pprint
import requests
from unidecode import unidecode
import time

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YTM0OGExMDhjMDVlMzI4ZmNkOWY4OWJiMDRmYWU2OSIsIm5iZiI6MTczMzg0NTA4MS40MzIsInN1YiI6IjY3NTg2MDU5OTkzNTliMDQ2OGE0Njc3ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.iybQH84AcS6kz6Ryzl83Y9Lg1VLbxGJmUaUc1e0AR-Y"
}

urln = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/nconst.tsv.gz"
urlt = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/tconst.tsv.gz"
dfn = pd.read_csv(urln, sep='\t')
dft = pd.read_csv(urlt, sep='\t')


movie_search = st.text_input("Rechercher un film", value="")
col1, col2 = st.columns(2)

with col1:
    case = st.checkbox("Ignorer majuscules", value=True, label_visibility="visible")
    accents = st.checkbox("Ignorer accents", value=True, label_visibility="visible")
with col2:
    nb_cards = st.number_input("Nombre de résultats", min_value=3, max_value=45, value=12, step=3, label_visibility="visible")

if case & accents:
    df_movie_search = dft.loc[dft["title"].apply(lambda x: unidecode(x)).str.lower().str.contains(unidecode(movie_search.lower()))].sort_values('rank', ascending=False).head(nb_cards)
elif case:
    df_movie_search = dft.loc[dft["title"].str.lower().str.contains(movie_search.lower())].sort_values('rank', ascending=False).head(nb_cards)
elif accents:
    df_movie_search = dft.loc[dft["title"].apply(lambda x: unidecode(x)).str.contains(unidecode(movie_search))].sort_values('rank', ascending=False).head(nb_cards)    
else:
    df_movie_search = dft.loc[dft["title"].str.contains(movie_search)].sort_values('rank', ascending=False).head(nb_cards)

#if movie_search:
#    placeholder.write(df_movie_search)



N_cards_per_row = 3
if movie_search:
    placeholder = st.empty()
    with placeholder.container():
        for n_row, row in df_movie_search.reset_index().iterrows():
            i = n_row%N_cards_per_row
            if i==0:
                placeholder.write("---")
                cols = placeholder.columns(N_cards_per_row, gap="large")
        # draw the card
            with cols[n_row%N_cards_per_row]:
                if placeholder.button((f"**{row['title']}**"), key=n_row):
                    placeholder.write("Clicked")

                placeholder.markdown(
                """
                <style>
                button {
                    background: none!important;
                    border: none;
                    padding: 0!important;
                    color: black !important;
                    text-decoration: none;
                    cursor: pointer;
                    border: none !important;
                }
                button:hover {
                    text-decoration: none;
                    color: black !important;
                }
                button:focus {
                    outline: none !important;
                    box-shadow: none !important;
                    color: black !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
)
                placeholder.markdown(f"**{row['title']}**")
                placeholder.markdown(f"**{row['rate']}**/10 _({int(row['vote'])})_")
                try:
                    path=requests.get('https://api.themoviedb.org/3/find/'+row['tconst']+'?external_source=imdb_id&language=fr', headers=headers).json()['movie_results'][0]['poster_path']
                    placeholder.image(f"https://image.tmdb.org/t/p/w500{path}", width=400)
                except:
                    placeholder.image(f"blank_mov.png", width=400)
