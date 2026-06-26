import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

# Load data
movies = pickle.load(open("movie_dict.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommender System")

# Dictionary values
movie_titles = list(movies["title"].values())

selected_movie = st.selectbox(
    "Type or select a movie",
    movie_titles
)

def recommend(movie):
    movie_index = movie_titles.index(movie)

    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_names = []
    recommended_posters = []

    for i in distances[1:6]:
        idx = i[0]
        movie_id = movies["movie_id"][idx]
        recommended_names.append(movies["title"][idx])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_names, recommended_posters

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])


