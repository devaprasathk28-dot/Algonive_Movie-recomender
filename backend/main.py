from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import json
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# =========================
# 🚀 SESSION (RETRY)
# =========================
session = requests.Session()
retries = Retry(total=2, backoff_factor=0.5)
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

# =========================
# 🚀 FASTAPI SETUP
# =========================
app = FastAPI()
# 🔥 Serve Vite static files
app.mount(
    "/assets",
    StaticFiles(directory="../frontend-vite/dist/assets"),
    name="assets",
)

# 🔥 Serve React app (Vite)
@app.get("/")
def serve_react():
    return FileResponse("../frontend-vite/dist/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 📂 LOAD DATA
# =========================
movies = pd.read_csv("../data/movies.csv")
links = pd.read_csv("../data/links.csv")  # ✅ FIXED NAME

movies = movies.merge(links, on="movieId")
movies = movies[movies['imdbId'].notna()].head(1000).reset_index(drop=True)

# =========================
# 🧹 PREPROCESSING
# =========================
movies['genres'] = movies['genres'].str.replace('|', ' ', regex=False)
movies['clean_title'] = movies['title'].str.lower().str.strip()
movies['overview'] = ""

# =========================
# 🔑 API KEYS
# =========================
OMDB_API_KEY = "c6ac3547"   # ⚠️ replace
TMDB_API_KEY = "98869963f7ce832dc4421deb03dca7d5"       # ⚠️ replace

# =========================
# 🧠 CACHE
# =========================
CACHE_FILE = "cache.json"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
else:
    cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

# =========================
# 🎬 HELPER FUNCTIONS
# =========================
def format_imdb_id(imdb_id):
    try:
        return "tt" + str(int(imdb_id)).zfill(7)
    except:
        return None


def fetch_movie_details(imdb_id):
    imdb_id = format_imdb_id(imdb_id)

    if imdb_id in cache:
        cached = cache[imdb_id]

        # 🔥 HANDLE OLD CACHE (2 values)
        if len(cached) == 2:
            poster, rating = cached
            return poster, rating, ""   # add empty overview

        return cached  # already 3 values

    try:
        url = "https://www.omdbapi.com/"
        params = {"apikey": OMDB_API_KEY, "i": imdb_id}

        res = session.get(url, params=params, timeout=5)
        data = res.json()

        if data.get("Response") == "True":
            poster = data.get("Poster", "https://via.placeholder.com/150")
            rating = data.get("imdbRating", "N/A")
            overview = data.get("Plot", "")
        else:
            poster, rating, overview = "https://via.placeholder.com/150", "N/A", ""

        # 🔥 ALWAYS SAVE 3 VALUES
        cache[imdb_id] = (poster, rating, overview)
        save_cache()

        return poster, rating, overview

    except:
        return "https://via.placeholder.com/150", "N/A", ""


# =========================
# 🤖 FETCH DESCRIPTIONS + VECTORIZATION
# =========================
print("Fetching descriptions...")

for i in range(len(movies)):
    imdb_id = movies.iloc[i].imdbId
    if pd.isna(imdb_id):
        continue
    _, _, overview = fetch_movie_details(imdb_id)
    movies.at[i, 'overview'] = overview

print("Descriptions loaded ✅")

movies['tags'] = (
    movies['genres'] + " " +
    movies['title'] + " " +
    movies['overview']
)
movies['tags'] = movies['tags'].fillna("")

cv = TfidfVectorizer(max_features=10000, stop_words='english')
vectors = cv.fit_transform(movies['tags'])
similarity = cosine_similarity(vectors)

# =========================
# 🔥 TRENDING FUNCTION (FIXED + FALLBACK)
# =========================
def get_trending_movies():
    movies['year'] = movies['title'].str.extract(r'\((\d{4})\)')
    movies['year'] = pd.to_numeric(movies['year'], errors='coerce')

    recent = movies.sort_values(by="year", ascending=False).head(100)

    trending = recent.sample(10)

    result = []

    for _, row in trending.iterrows():
        poster, rating, _ = fetch_movie_details(row["imdbId"])

        result.append({
            "title": row["title"],
            "poster": poster,
            "rating": rating
        })

    return result


# =========================
# 🎯 RECOMMENDATION API
# =========================
@app.get("/recommend/{movie}")
def recommend(movie: str, limit: int = 10, sort_by: str = "none"):

    limit = min(limit, 10)

    movie = movie.lower().strip()

    safe_movie = re.escape(movie)  # 🔥 escape regex characters

    match = movies[movies['clean_title'].str.contains(safe_movie, regex=True)]

    if match.empty:
        return {"error": "Movie not found"}

    movie_index = match.index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]  
    )



    seen_titles = set()
    result = []

    for i in movies_list:
        movie_row = movies.iloc[i[0]]
        title = movie_row.title

        # 🔥 skip duplicates
        if title in seen_titles:
            continue

        seen_titles.add(title)

        imdb_id = movie_row.imdbId
        if pd.isna(imdb_id):
            continue

        poster, rating, _ = fetch_movie_details(imdb_id)

        year = title[-5:-1] if "(" in title else "0000"

        result.append({
            "title": title,
            "poster": poster,
            "backdrop": poster,   # 🔥 for now reuse poster
            "rating": float(rating) if rating not in ["N/A", None] else -1,
            "year": int(year) if year.isdigit() else 0,
            "overview": movie_row.overview
        })

        # 🔥 STOP when limit reached
        if len(result) == limit:
            break

    # Remove duplicates
    seen = set()
    unique = []

    for r in result:
        if r["title"] not in seen:
            unique.append(r)
            seen.add(r["title"])

    result = unique

    # Sorting
    if sort_by == "rating":
        result.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "alphabet":
        result.sort(key=lambda x: x["title"])
    elif sort_by == "year":
        result.sort(key=lambda x: x["year"], reverse=True)

    result = result[:limit]

    return {"recommendations": result}


# =========================
# 🔥 TRENDING API
# =========================
@app.get("/trending")
def trending():
    return {"trending": get_trending_movies()}