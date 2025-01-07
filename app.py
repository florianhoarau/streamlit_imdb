import streamlit as st
import pandas as pd
import seaborn as sns
import operator
from pprint import pprint
import requests
from streamlit_extras.switch_page_button import switch_page

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YTM0OGExMDhjMDVlMzI4ZmNkOWY4OWJiMDRmYWU2OSIsIm5iZiI6MTczMzg0NTA4MS40MzIsInN1YiI6IjY3NTg2MDU5OTkzNTliMDQ2OGE0Njc3ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.iybQH84AcS6kz6Ryzl83Y9Lg1VLbxGJmUaUc1e0AR-Y"
}

urln = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/nconst.tsv.gz"
urlt = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/tconst.tsv.gz"
dfn = pd.read_csv(urln, sep='\t')
dft = pd.read_csv(urlt, sep='\t')

if 'nconst' not in st.session_state:
    st.session_state['nconst'] = 'nm0000288'
st.write(st.session_state)


# Connect to the Google Sheet
# Show the dataframe (we'll delete this later)
actor_search = st.text_input("Search a person", value="")
df_actor_search = dfn.loc[dfn["primaryName"].str.contains(actor_search)].sort_values('rankk', ascending=False).head(9)

#if actor_search:
#    st.write(df_actor_search)
N_cards_per_row = 3
if actor_search:
    for n_row, row in df_actor_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{(((operator.not_(pd.isna(row['actor'])))*row.index[2].capitalize())+' '+(operator.not_(pd.isna(row['actress'])))*row.index[3].capitalize()).strip()+' '+(((operator.not_(pd.isna(row['director'])))*row.index[4].capitalize())+' '+(operator.not_(pd.isna(row['writer'])))*row.index[5].capitalize()).strip()}")
            st.markdown(f"**{row['primaryName']}**")
            try:
                path=requests.get('https://api.themoviedb.org/3/find/'+row['nconst']+'?external_source=imdb_id', headers=headers).json()['person_results'][0]['profile_path']
                st.image(f"https://image.tmdb.org/t/p/w500{path}", width=400)
            except:
                True