import pickle
import streamlit as st
import requests
import pandas as pd

import time

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    max_retries = 3
    for retry in range(max_retries):
        try:
            data = requests.get(url)
            data.raise_for_status()  # Raise HTTPError for bad responses
            data = data.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        except requests.exceptions.RequestException as e:
            print(f"Error fetching poster: {e}")
            if retry < max_retries - 1:
                print(f"Retrying ({retry + 1}/{max_retries}) after 5 seconds...")
                time.sleep(5)
            else:
                raise



def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index.to_list()[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

def main():
    st.header('Movie Recommender System')

    movies = pd.read_pickle(r"C:\Users\Lenovo\Downloads\model\movie_list.pkl")
    similarity = pd.read_pickle(r"C:\Users\Lenovo\Downloads\model\similarity.pkl")

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)
        display_recommendations(recommended_movie_names, recommended_movie_posters)

def display_recommendations(names, posters):
    col_count = len(names)
    col_list = st.columns(col_count)

    for i in range(col_count):
        with col_list[i]:
            st.text(names[i])
            st.image(posters[i])

if __name__ == "__main__":
    main()

