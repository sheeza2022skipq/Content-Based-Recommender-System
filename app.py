import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=51012e3c20f92734f37619bb1c997e46&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommendersystem(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movie_lists = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:11]

    recommender_movies = []
    recommender_movies_poster = []
    for i in movie_lists:
        recommender_movies.append(movies.iloc[i[0]].title)
        recommender_movies_poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommender_movies, recommender_movies_poster


st.title('Movie Recommender System')
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movies_list)

if st.button('Show Recommendation'):
    recommendation, poster = recommendersystem(selected_movie)

    st.subheader("Recommended Movies:")

    # Create a grid layout for displaying recommendations
    num_columns = 3
    num_recommendations = len(recommendation)

    # Calculate the number of rows needed to display all recommendations
    num_rows = (num_recommendations - 1) // num_columns + 1

    # Loop through rows and columns to display recommendations
    for row in range(num_rows):
        with st.container():
            columns = st.columns(num_columns)
            for col in range(num_columns):
                recommendation_idx = row * num_columns + col
                if recommendation_idx < num_recommendations:
                    with columns[col]:
                        st.image(poster[recommendation_idx], caption=recommendation[recommendation_idx],
                                 use_column_width=True)

