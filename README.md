# 🎬 ML-Powered Movie Recommender System

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-brightgreen)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blueviolet)](https://react.dev/)
[![Scikit-learn](https://img.shields.io/badge/Scikit-learn-1.5+-orange)](https://scikit-learn.org/)

A **full-stack Machine Learning-powered Movie Recommendation System** with **Netflix-inspired responsive UI**.

Uses **content-based filtering** (TF-IDF + Cosine Similarity on genres, title, overview) powered by MovieLens dataset and OMDb API for posters/ratings.

## 🚀 Live Demo

**Local Demo:** http://127.0.0.1:8000

*(Deployed link: Add after Render/Vercel deployment)*

## 📌 Features

### 🎯 ML Core

* ✅ **Content-Based Filtering**: TF-IDF vectorization (genres + title + overview), Cosine Similarity
* ✅ Real-time search with auto-suggestions
* ✅ Top-N recs (max 10, configurable)
* ✅ Sorting: similarity (default), rating, year, A-Z
* ✅ Dataset: MovieLens small (1000 movies sampled)
* ✅ Duplicate removal & fuzzy title matching

### 🎬 Netflix-Style UI

* ✅ Responsive dark theme (#0f0f0f + red accents)
* ✅ Horizontal trending scroll (hover scale)
* ✅ Hover trailer preview (YouTube embed, 600ms delay)
* ✅ Full movie modal (poster, rating, overview, trailer)
* ✅ Full-screen trailer modal
* ✅ Grid cards with play icon overlay

### ⚡ Production Ready

* ✅ OMDb API caching (`cache.json`)
* ✅ Pre-computed similarity matrix
* ✅ Single-server deployment (FastAPI serves React)
* ✅ Fallback images/ratings
* ✅ CORS enabled

## 🧠 ML Pipeline (Production)

**Algorithm:** Content-Based Filtering

**Features:** `tags = genres + title + overview`

**Vectorization:** `TfidfVectorizer(max_features=10000, stop_words='english')`

**Similarity:** `cosine_similarity(vectors)` (pre-computed matrix)

**Data Flow:**
```python
movies['tags'] = genres + \" \" + title + \" \" + overview  # OMDb fetched
vectors = cv.fit_transform(tags)
similarity = cosine_similarity(vectors)
```

**Notebook Prototype:** `notebook/movie_recommender.py` (CountVec + Collab filtering)

## 🏗️ Tech Stack

### 🔹 Backend API

* [FastAPI](https://fastapi.tiangolo.com/)
* [Pandas](https://pandas.pydata.org/)
* [Scikit-learn](https://scikit-learn.org/)
* [Uvicorn](https://www.uvicorn.org/)

### 🔹 Frontend

* [React 18](https://react.dev/) + [Vite](https://vitejs.dev/)
* [Axios](https://axios-http.com/)
* Tailwind-free custom Netflix CSS

### 🔹 Data & APIs

* [MovieLens small](https://grouplens.org/datasets/movielens/)
* [OMDb API](http://www.omdbapi.com/) (posters/ratings/overview, cached)
* [YouTube Embed](https://developers.google.com/youtube) (search trailers)

## 📁 Project Structure

```
Movie recommendation/
├── backend/
│   ├── main.py              # FastAPI + ML logic
│   ├── requirements.txt     # Dependencies
│   └── cache.json          # OMDb cache
├── frontend-vite/           # React + Vite
│   ├── src/
│   │   ├── App.jsx         # Main UI
│   │   └── App.css         # Netflix styling
│   ├── dist/               # Build output
│   └── package.json
├── data/                   # MovieLens data
│   ├── movies.csv
│   └── links.csv
├── data_sets/              # Data scripts
│   └── download_data.py
├── notebook/               # ML prototype
│   └── movie_recommender.py
└── TODO.md
```

## ⚙️ Quick Setup & Run

### 📥 1. Download Data

```bash
python data_sets/download_data.py
```

Downloads MovieLens small → extracts `data/movies.csv` + `data/links.csv`.

### 📦 2. Install Backend

```bash
cd backend
pip install -r requirements.txt
```

### 🎨 3. Build Frontend

```bash
cd ../frontend-vite
npm install
npm run build  # → dist/
```

### ▶️ 4. Run Server

```bash
cd ../backend
uvicorn main:app --reload
```

**Open:** http://127.0.0.1:8000 🎬

## 🌐 Deployment

**Single-server** (FastAPI serves React `dist/`).

### Render.com

**Build Command:**
```bash
cd frontend-vite && npm ci && npm run build && cd ../backend && pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT --reload
```

**Env Vars:** `OMDB_API_KEY=your_key`

### Railway/Heroku
Adapt similar build/start cmds.

## ⚠️ Production Notes

* Replace OMDb key in `backend/main.py` (line ~72)
* Initial run fetches overviews → populates `cache.json` (~5-10s)
* Free OMDb: 1000 req/day → cached forever after
* No auth/users (add Flask-Login/JWT for prod)
* Dataset: 1000 movies (MovieLens small, recent trending sample)

## 🔮 Next Steps

* 🔑 User system + watchlist (JWT + DB)
* 🎯 Hybrid: Add collaborative (ratings pivot in notebook)
* 🌐 TMDb v3 API (better images)
* 📱 Mobile PWA
* 🚀 Rate limiting + Redis cache

## 👨‍💻 Author

**Devaprasath** - AI/ML Engineer

Built with ❤️ using FastAPI + React + Scikit-learn

## 📄 License
MIT - Free to use/modify.

