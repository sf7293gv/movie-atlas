from flask import Flask, render_template, request, jsonify
from apis.tmdb import get_tmdb
from main_helper import assemble_selected_movie_data
from urllib.parse import quote

app = Flask(__name__)

# ============================================================
# HOME PAGE
# ============================================================

@app.route('/')
def index():
    movies = get_tmdb()
    return render_template('index.html', movies=movies)

# ============================================================
# MOVIE DETAILS PAGE
# ============================================================

@app.route('/selected_movie')
def selected_movie():
    title = request.args.get('title')
    date = request.args.get('release_date')
    tmdb_id = request.args.get('tmdb_id')
    poster_path = request.args.get('poster_path')

    # Convert tmdb_id from string → int
    if tmdb_id:
        try:
            tmdb_id = int(tmdb_id)
        except:
            tmdb_id = None

    # Fetch full movie details (OMDb + TMDB + YouTube)
    movie_details = assemble_selected_movie_data(title, date, tmdb_id)

    # Attach poster_path for template display
    if movie_details:
        movie_details.poster_path = poster_path

    return render_template('movie_details.html', movie_object=movie_details)

# ============================================================
# AI HELPER PAGE
# ============================================================

@app.route('/ai_helper')
def ai_helper():
    return render_template('ai_helper.html')

# ============================================================
# AI HELPER LOGIC
# ============================================================

@app.route('/ai_helper_response', methods=['POST'])
def ai_helper_response():

    user_message = request.json.get("message", "").lower()

    # Load homepage movies (same data displayed on the homepage)
    movies = get_tmdb()
    if not movies:
        return jsonify({"reply": "I couldn't load movie data. Try again later."})

    # TMDB Genre ID → Genre Name Map
    GENRE_MAP = {
        28: "action",
        12: "adventure",
        16: "animation",
        35: "comedy",
        80: "crime",
        99: "documentary",
        18: "drama",
        10751: "family",
        14: "fantasy",
        36: "history",
        27: "horror",
        10402: "music",
        9648: "mystery",
        10749: "romance",
        878: "science fiction",
        10770: "tv movie",
        53: "thriller",
        10752: "war",
        37: "western"
    }

    # Detect which genre user mentioned
    detected_genre = None
    for genre_name in GENRE_MAP.values():
        if genre_name in user_message:
            detected_genre = genre_name
            break

    if not detected_genre:
        return jsonify({
            "reply": "Try asking for a genre like action, comedy, horror, romance, thriller, family, or drama!"
        })

    # Find all movies that match that genre
    matched_movies = []
    for m in movies:
        for gid in m.get("genre_ids", []):
            if GENRE_MAP.get(gid) == detected_genre:
                matched_movies.append(m)
                break

    if not matched_movies:
        return jsonify({
            "reply": f"No {detected_genre.title()} movies found on the homepage."
        })

    # Build clickable results
    reply = f"Here are some {detected_genre.title()} movies:<br><br>"

    for m in matched_movies:
        title = quote(m["title"])
        poster = quote(m["poster_path"] or "")
        release = m["release_date"]

        # FIX: TMDB ID is stored as "id"
        tmdb_id = m["id"]

        link = (
            f'/selected_movie?title={title}'
            f'&release_date={release}'
            f'&tmdb_id={tmdb_id}'
            f'&poster_path={poster}'
        )

        reply += f'• <a href="{link}" class="movie-link">{m["title"]}</a><br>'

    return jsonify({"reply": reply})


# ============================================================
# RUN APP
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)
