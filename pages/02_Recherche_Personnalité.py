import streamlit as st
import pandas as pd
import operator
import requests
from unidecode import unidecode
from streamlit_extras.switch_page_button import switch_page
import time


headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YTM0OGExMDhjMDVlMzI4ZmNkOWY4OWJiMDRmYWU2OSIsIm5iZiI6MTczMzg0NTA4MS40MzIsInN1YiI6IjY3NTg2MDU5OTkzNTliMDQ2OGE0Njc3ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.iybQH84AcS6kz6Ryzl83Y9Lg1VLbxGJmUaUc1e0AR-Y"
}

urln = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/nconst.tsv.gz"
urlt = "https://raw.githubusercontent.com/florianhoarau/streamlit_imdb/main/tconst.tsv.gz"
dfn = pd.read_csv(urln, sep='\t')
dft = pd.read_csv(urlt, sep='\t')

#def npage(nconst):
#    st.session_state['nconst'] = nconst
#    switch_page('pers')

st.set_page_config(page_title="Recherche Personnalité", page_icon="")
st.sidebar.header("Recherche Personnalité")

actor_search = st.text_input("Rechercher une personnalité", value="")
col1, col2 = st.columns(2)

with col1:
    case = st.checkbox("Ignorer majuscules", value=True, label_visibility="visible")
    accents = st.checkbox("Ignorer accents", value=True, label_visibility="visible")
with col2:
    nb_cards = st.number_input("Nombre de résultats", min_value=3, max_value=45, value=12, step=3, label_visibility="visible")



if case & accents:
    df_actor_search = dfn.loc[dfn["primaryName"].apply(lambda x: unidecode(x)).str.lower().str.contains(unidecode(actor_search.lower()))].sort_values('rankk', ascending=False).head(nb_cards)
elif case:
    df_actor_search = dfn.loc[dfn["primaryName"].str.lower().str.contains(actor_search.lower())].sort_values('rankk', ascending=False).head(nb_cards)
elif accents:
    df_actor_search = dfn.loc[dfn["primaryName"].apply(lambda x: unidecode(x)).str.contains(unidecode(actor_search))].sort_values('rankk', ascending=False).head(nb_cards)    
else:
    df_actor_search = dfn.loc[dfn["primaryName"].str.contains(actor_search)].sort_values('rankk', ascending=False).head(nb_cards)

#if actor_search:
st.write(df_actor_search)
N_cards_per_row = 3
if actor_search:
    for n_row, row in df_actor_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            api=requests.get('https://api.themoviedb.org/3/find/'+row['nconst']+'?external_source=imdb_id', headers=headers).json()
            try:                
                gender=api['person_results'][0]['gender']
            except:
                gender=0
            listroles=[]
            numroles=[]
            listroles.append('Acteur')
            if operator.not_(pd.isna(row['actor'])):
                numroles.append(len(row['actor']))
            else:
                numroles.append(0)
            listroles.append('Actrice')    
            if operator.not_(pd.isna(row['actress'])):
                numroles.append(len(row['actress']))
            else:
                numroles.append(0)
            if gender==1:
                listroles.append('Réalisatrice')
                backupp='blank_fem.png'
            elif gender==2:
                listroles.append('Réalisateur')
                backupp='blank_male.png'
            else:
                listroles.append('Réalisat.eur.rice')
                backupp='blank_gend.jpg'
            if operator.not_(pd.isna(row['director'])):
                numroles.append(len(row['director']))
            else:
                numroles.append(0)
            listroles.append('Scénariste')
            if operator.not_(pd.isna(row['writer'])):
                numroles.append(len(row['writer']))
            else:
                numroles.append(0)
#            st.text(str(listroles))
#            st.text(str(numroles))
            listtt=pd.DataFrame(data={'role': listroles, 'num': numroles}).sort_values('num', ascending=False)
            st.caption(f"{(((listtt['num'].values[0]!=0)*listtt['role'].values[0])+'   '+((listtt['num'].values[1]!=0)*listtt['role'].values[1])).strip()+'   '+(((listtt['num'].values[2]!=0)*listtt['role'].values[2])+'   '+((listtt['num'].values[3]!=0)*listtt['role'].values[3])).strip()}")
            if st.button(f"**{row['primaryName']}**"):
                st.session_state['nconst'] = row['nconst']
                time.sleep(1.5)
                switch_page('04_Fiche_Personnalité')
            st.markdown(
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
            try:
                imgpath=api['person_results'][0]['profile_path']
                if (imgpath=='null') or (imgpath is None):
                    st.image(f"{backupp}", width=400)
                else:
                    st.image(f"https://image.tmdb.org/t/p/original{imgpath}", width=400)
            except:
                st.image(f"{backupp}", width=400)