from flask import Flask, render_template, redirect, request
from apis.tmdb import get_tmdb
from database.favorites_db import FavoritesDB
from main_helper import (
    assemble_selected_movie_data,
    assemble_favorite_movie_object,
    show_add_to_favorites_button
)

app = Flask(__name__)

favorites_db = FavoritesDB()


@app.route('/')
def index():
    movies = get_tmdb()
    return render_template('index.html', movies=movies)


@app.route('/selected_movie')
def selected_movie():
    title = request.args.get('title')
    date = request.args.get('release_date')
    tmdb_id = request.args.get('tmdb_id')
    poster = request.args.get('poster')

    if not title or not date or not tmdb_id:
        return render_template('error.html')

    movie_details = assemble_selected_movie_data(title, date, tmdb_id)

    # Set the poster attribute (Favorite object supports attributes, not dict keys)
    movie_details.poster = poster

    movie_from_db = favorites_db.get_one_favorite(tmdb_id)
    show_favorites_btn = show_add_to_favorites_button(movie_from_db)

    return render_template(
        'movie_details.html',
        movie_object=movie_details,
        show_favorites_btn=show_favorites_btn
    )


@app.route('/add_to_favorites')
def add_to_favorites():
    title = request.args.get('title')
    date = request.args.get('release_date')
    tmdb_id = request.args.get('tmdb_id')

    if not title or not date or not tmdb_id:
        return render_template('error.html')

    favorite = assemble_favorite_movie_object(title, date, tmdb_id)
    favorites_db.add_favorite(favorite)

    return redirect('/favorite_movies')


@app.route('/favorite_movies')
def favorite_movies():
    favorite_movies = favorites_db.get_all_favorites()
    return render_template('favorite_movies.html', favorite_movies=favorite_movies)


@app.route('/delete_favorite')
def delete_favorite():
    tmdb_id = request.args.get('tmdb_id')

    if tmdb_id:
        favorites_db.delete_favorite(tmdb_id)

    return redirect('/favorite_movies')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
