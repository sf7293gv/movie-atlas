# Movie Atlas — Movie Discovery Web App

Movie Atlas is a movie discovery application where you can browse trending theatrical releases, explore cast and crew details, view posters, and watch official trailers — all in one place.

It integrates data from multiple APIs to deliver a complete movie experience:

- TMDB API → trending movies, posters, release dates
- OMDb API → directors, actors, genres, plot
- YouTube Data API → embedded trailers

Built with Flask, featuring a clean, modern UI inspired by TMDB and optimized for mobile.

## Features

Homepage — Top Theater Releases:
- Fetches the top 20 movies currently in U.S. theaters from TMDB
- Displays posters, titles, and release dates
- Each movie links to a detailed page

Movie Details Page includes:
- Poster
- Release date
- Director
- Cast
- Genres
- Plot
- Embedded YouTube trailer
- Add to Favorites button

Favorites System:
- Add movies to a Favorites list
- View all saved favorites
- Remove favorites anytime

Works through:
- Python
- Flask
- TMDB, OMDb, YouTube APIs

## Installation

Set environment variables:
YOUTUBE_API=your_key
TMDB_KEY=your_key
OMDB_KEY=your_key

Clone & run:
git clone https://github.com/sf7293gv/movie-atlas
cd movie-atlas
python -m venv venv
pip install -r requirements.txt
python main.py

Visit http://127.0.0.1:5000/
