import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [movie, setMovie] = useState("");
  const [results, setResults] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [trailer, setTrailer] = useState(null);
  const [limit, setLimit] = useState(10);
  const [sortBy, setSortBy] = useState("none");
  const [trending, setTrending] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [hoveredMovie, setHoveredMovie] = useState(null);
  const [hoverTimeout, setHoverTimeout] = useState(null);

  // 🔥 Load trending
  useEffect(() => {
    axios
      .get("/trending")
      .then((res) => setTrending(res.data.trending))
      .catch(() => setTrending([]));
  }, []);

  // 🔍 Suggestions
  const handleInput = async (value) => {
    setMovie(value);

    if (value.length > 2) {
      try {
        const res = await axios.get(
`/recommend/${encodeURIComponent(
            value
          )}?limit=5`
        );
        setSuggestions(res.data.recommendations || []);
      } catch {
        setSuggestions([]);
      }
    } else {
      setSuggestions([]);
    }
  };

  // 🎯 Get recommendations
  const getRecommendations = async () => {
    if (!movie) return;

    setLoading(true);
    try {
      const res = await axios.get(
`/recommend/${encodeURIComponent(
          movie
        )}?limit=${limit}&sort_by=${sortBy}`
      );
      setResults(res.data.recommendations || []);
    } catch {
      alert("Error fetching data");
    }
    setLoading(false);
  };

  // 🎬 Trailer
  const playTrailer = (title) => {
    const query = title + " trailer";
    setTrailer(
      `https://www.youtube.com/embed?listType=search&list=${query}`
    );
  };

  const closeTrailer = () => setTrailer(null);

  // 🎥 Hover preview logic
  const handleMouseEnter = (movie) => {
    const timeout = setTimeout(() => {
      setHoveredMovie(movie.title);
    }, 600);
    setHoverTimeout(timeout);
  };

  const handleMouseLeave = () => {
    clearTimeout(hoverTimeout);
    setHoveredMovie(null);
  };

  return (
    <div className="app">
      {/* 🎬 HEADER */}
      <h1 className="title">🎬 Movie Recommender</h1>

      {/* 🔥 TRENDING */}
      <h2 className="section-title">🔥 Trending Now</h2>
      <div className="row-wrapper">
        <div className="row-scroll">
          {trending.map((m, i) => (
            <div
              className="trending-card"
              key={i}
              onClick={() => setMovie(m.title)}
            >
              <img src={m.poster} alt={m.title} />
              <div className="trending-overlay">
                <p>{m.title}</p>
                <span>⭐ {m.rating}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 🔍 SEARCH */}
      <div className="search-box">
        <input
          type="text"
          placeholder="Search movies..."
          value={movie}
          onChange={(e) => handleInput(e.target.value)}
        />
        <button onClick={getRecommendations}>Search</button>
      </div>

      {/* ⚙️ CONTROLS */}
      <div className="controls">
        <select onChange={(e) => setSortBy(e.target.value)}>
          <option value="none">Default</option>
          <option value="rating">Rating</option>
          <option value="alphabet">A-Z</option>
          <option value="year">Year</option>
        </select>

        <input
          type="number"
          value={limit}
          onChange={(e) => setLimit(Number(e.target.value))}
        />
      </div>

      {/* 🔥 SUGGESTIONS */}
      {suggestions.length > 0 && (
        <div className="suggestions">
          {suggestions.map((s, i) => (
            <div
              key={i}
              onClick={() => {
                setMovie(s.title);
                setSuggestions([]);
              }}
            >
              {s.title}
            </div>
          ))}
        </div>
      )}

      {/* ⏳ LOADING */}
      {loading && <p className="loading">Loading...</p>}

      {/* 🎬 RESULTS */}
      <div className="grid">
        {results.map((m, index) => (
          <div
            className="card"
            key={index}
            onMouseEnter={() => handleMouseEnter(m)}
            onMouseLeave={handleMouseLeave}
            onClick={() => setSelectedMovie(m)}
          >
            {hoveredMovie === m.title ? (
              <iframe
                className="trailer-preview"
                src={`https://www.youtube.com/embed?autoplay=1&mute=1&controls=0&loop=1&playlist=${m.title} trailer`}
                title="preview"
                allow="autoplay"
              ></iframe>
            ) : (
              <img
                src={
                  m.poster && m.poster !== "N/A"
                    ? m.poster
                    : "https://via.placeholder.com/300x450?text=No+Image"
                }
                alt={m.title}
              />
            )}

            <div className="overlay">
              <h3>{m.title.replace(/\(\d{4}\)/, "")}</h3>
              <p>⭐ {m.rating > 0 ? m.rating : "Not Rated"}</p>
            </div>
          </div>
        ))}
      </div>

      {/* 🎥 TRAILER MODAL */}
      {trailer && (
        <div className="trailer-modal" onClick={closeTrailer}>
          <div
            className="trailer-content"
            onClick={(e) => e.stopPropagation()}
          >
            <iframe
              width="100%"
              height="400"
              src={trailer}
              title="Trailer"
              allowFullScreen
            ></iframe>
          </div>
        </div>
      )}

      {/* 🎬 MOVIE DETAILS MODAL */}
      {selectedMovie && (
        <div
          className="movie-modal"
          onClick={() => setSelectedMovie(null)}
        >
          <div
            className="movie-modal-content"
            style={{
              backgroundImage: `url(${selectedMovie.backdrop || selectedMovie.poster})`,
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="backdrop-overlay">
              <div className="movie-modal-inner">
                <img
                  src={selectedMovie.poster}
                  alt={selectedMovie.title}
                />

                <div className="movie-details">
                  <h2>{selectedMovie.title}</h2>

                  <p className="rating">
                    ⭐{" "}
                    {selectedMovie.rating > 0
                      ? selectedMovie.rating
                      : "Not Rated"}
                  </p>

                  <p className="description">
                    {selectedMovie.overview ||
                      "No description available"}
                  </p>

                  <button
                    onClick={() =>
                      playTrailer(selectedMovie.title)
                    }
                  >
                    ▶ Watch Trailer
                  </button>

                  <button
                    className="close-btn"
                    onClick={() => setSelectedMovie(null)}
                  >
                    ✖ Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;