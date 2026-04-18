import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv("../data/movies.csv")
ratings = pd.read_csv("../data/ratings.csv")
links = pd.read_csv("../data/links.csv")

# 🔥 MERGE DATA (IMPORTANT)
movies = movies.merge(links, on="movieId")
movies = movies[movies['imdbId'].notna()]   # remove missing IDs
# -----------------------------
# STEP 1: Basic Data Check
# -----------------------------
print("Movies Data:")
print(movies.head())

print("\nRatings Data:")
print(ratings.head())

# -----------------------------
# STEP 2: Data Cleaning
# -----------------------------
# Replace '|' with space in genres
movies['tags'] = movies['genres'] + " " + movies['title']



cv = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags'])

print("\nVector Shape:", vectors.shape)


# -----------------------------
# STEP 3: Convert Text → Vectors
# -----------------------------


cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['genres'])

if isinstance(vectors, csr_matrix):
    vectors = vectors.toarray()

print("\nVector Shape:", vectors.shape)

# -----------------------------
# STEP 4: Calculate Similarity
# -----------------------------


similarity = cosine_similarity(vectors)

print("Similarity Matrix Shape:", similarity.shape)

# -----------------------------
# STEP 5: Recommendation Function
# -----------------------------
def recommend(movie):
    if movie not in movies['title'].values:
        print("Movie not found. Please check the name.")
        return

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,
                         key=lambda x: x[1])[1:6]

    print("\nRecommended Movies for:", movie)
    print("-----------------------------------")

    for i in movies_list:
        print(movies.iloc[i[0]].title)


pivot = ratings.pivot_table(index='movieId', columns='userId', values='rating')
pivot.fillna(0, inplace=True)

print("Pivot Shape:", pivot.shape)
from sklearn.metrics.pairwise import cosine_similarity

movie_similarity = cosine_similarity(pivot)
movie_ids = pivot.index
movie_id_to_index = {movie_id: idx for idx, movie_id in enumerate(movie_ids)}
# -----------------------------
# rating based
# -----------------------------
def recommend_collab(movie):
    # Get movieId
    movie_id = movies[movies['title'] == movie]['movieId'].values

    if len(movie_id) == 0:
        print("Movie not found")
        return

    movie_id = movie_id[0]

    if movie_id not in movie_id_to_index:
        print("Movie not in ratings dataset")
        return

    idx = movie_id_to_index[movie_id]
    distances = movie_similarity[idx]

    similar_movies = sorted(list(enumerate(distances)),
                            reverse=True,
                            key=lambda x: x[1])[1:6]

    print("\nRecommended (User-Based):\n")

    for i in similar_movies:
        movie_id = movie_ids[i[0]]
        title = movies[movies['movieId'] == movie_id]['title'].values
        if len(title) > 0:
            print(title[0])
# -----------------------------
# STEP 6: Test the Model
# -----------------------------
# Change movie name if needed
recommend("Toy Story (1995)")