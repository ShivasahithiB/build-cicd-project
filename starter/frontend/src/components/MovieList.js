import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

function MovieList({ onMovieClick }) {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_MOVIE_API_URL}/movies`)
      .then((response) => {
        let movieData = [];

        if (Array.isArray(response.data)) {
          movieData = response.data;
        } else if (Array.isArray(response.data.movies)) {
          movieData = response.data.movies;
        }

        setMovies(movieData);
      })
      .catch((error) => {
        console.error('Error fetching movies:', error);
        setMovies([]);
      });
  }, []);

  return (
    <ul>
      {movies.map((movie) => (
        <li className="movieItem" key={movie.id} onClick={() => onMovieClick(movie)}>
          {movie.title}
        </li>
      ))}
    </ul>
  );
}

MovieList.propTypes = {
  onMovieClick: PropTypes.func.isRequired,
};

export default MovieList;
