import streamlit as st
import pickle
import os
import pandas as pd 
import numpy as  np

import requests

def fetch_poster(music_title):
    # API endpoint might need adjustment based on actual API structure
    url = f"http://127.0.0.1:5000/get_poster?title={music_title}"  # Assuming a fixed search for Hindi music
    try:
        response = requests.get(url.format(music_title,))
        data = response.json()
        return data  # Assuming relevant poster data is in the response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for '{music_title}': {e}")
        return None  # Handle cases where poster cannot be fetched gracefully

def recommend(music, similarity, selected_music_name):
    try:
        music_index = music[music['title'] == selected_music_name].index[0]
        distances = similarity[music_index]
        music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_music = []
        recommended_music_poster = []
        for i in music_list:
            music_title = music.iloc[i[0]].title
            recommended_music.append(music.iloc[i[0]].title)
            recommended_music_poster.append(fetch_poster(music_title))
        return recommended_music, recommended_music_poster
    except (KeyError, IndexError):
        print(f"Error generating recommendations: Music '{selected_music_name}' not found or similarity matrix issue.")
        return [], None  # Handle missing music or similarity issues gracefully

file_dir = os.path.dirname(__file__)
music_file_path = os.path.join(file_dir, r'music-recommendation-frontend\\music_list.pkl','rb')
similarity_file_path = os.path.join(file_dir, r'music-recommendation-frontend\\similarity.pkl','rb')



try:
    music_dict = pickle.load(open(music_file_path, 'rb'))
    music = pd.DataFrame(music_dict)
    similarity = pickle.load(open(similarity_file_path, 'rb'))
except FileNotFoundError:
    print("Error: Pickle files not found")
except pickle.UnpicklingError:
    print("Error: Pickle files corrupted")

if st.button('Recommend'):
    recommended_music, recommended_music_poster = recommend(music_list, similarity, selected_music_name)

    if recommended_music:  # Check if recommendations were generated successfully
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_music[0])
            if recommended_music_poster[0]:
                st.image(recommended_music_poster[0])
            else:
                st.write("Poster unavailable")
        with col2:
            st.text(recommended_music[1])
            if recommended_music_poster[1]:
                st.image(recommended_music_poster[1])
            else:
                st.write("Poster unavailable")
        # ... repeat for remaining columns
    else:
        st.error("Error generating recommendations. Please try again with a different music selection.")