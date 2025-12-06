from apis import omdb, tmdb, youtube_api
from create_new_movie import create_new_movie

def assemble_selected_movie_data(title, year, tmdb_id):
    """
    Assemble movie data by fetching OMDB, TMDB (full details) and YouTube trailer.
    This function returns a movie object (Favorite model) or None.
    """

    # Basic validation
    if not title:
        print("assemble_selected_movie_data: missing title")
        return None

    # Try OMDB first (may return None)
    try:
        movie_details = omdb.get_movie_data(title, year)
    except Exception as e:
        print("assemble_selected_movie_data: OMDB fetch error:", e)
        movie_details = None

    # Safely get TMDB full details if id supplied
    tmdb_details = None
    if tmdb_id:
        try:
            tmdb_details = tmdb.get_tmdb_full_details(tmdb_id)
        except Exception as e:
            print("assemble_selected_movie_data: TMDB fetch error:", e)
            tmdb_details = None
    else:
        print("assemble_selected_movie_data: no tmdb_id provided")

    # YouTube trailer (best-effort)
    try:
        vid_title, vid_id = youtube_api.movie_trailer(title)
    except Exception as e:
        print("assemble_selected_movie_data: YouTube fetch error:", e)
        vid_title, vid_id = None, None

    # If we have neither OMDB nor TMDB details, we can't build the movie
    if not movie_details and not tmdb_details:
        print("assemble_selected_movie_data: no OMDB and no TMDB data available")
        return None

    # create_new_movie will accept optional tmdb_details via tmdb_id;
    # keep passing tmdb_id so create_new_movie may call TMDB if needed.
    new_movie = create_new_movie(movie_details, vid_id, vid_title, tmdb_id, tmdb_details=tmdb_details)
    return new_movie


def assemble_favorite_movie_object(title, date, tmdb_id):
    """
    For favorites stored in the DB: use the provided date (string), extract year,
    fetch OMDB/TMDB/YouTube as available and build Favorite object.
    """
    if not title:
        return None

    # Attempt to extract a year from the stored date string (if present)
    try:
        date_parts = date.split()
        year = date_parts[-1] if date_parts else None
    except Exception:
        year = None

    # OMDB
    try:
        movie_details = omdb.get_movie_data(title, year)
    except Exception as e:
        print("assemble_favorite_movie_object: OMDB fetch error:", e)
        movie_details = None

    # TMDB
    tmdb_details = None
    if tmdb_id:
        try:
            tmdb_details = tmdb.get_tmdb_full_details(tmdb_id)
        except Exception as e:
            print("assemble_favorite_movie_object: TMDB fetch error:", e)
            tmdb_details = None

    # YouTube
    try:
        vid_title, vid_id = youtube_api.movie_trailer(title)
    except Exception as e:
        print("assemble_favorite_movie_object: YouTube fetch error:", e)
        vid_title, vid_id = None, None

    if not movie_details and not tmdb_details:
        return None

    favorite = create_new_movie(movie_details, vid_id, vid_title, tmdb_id, tmdb_details=tmdb_details)
    return favorite


def show_add_to_favorites_button(favorite):
    return not bool(favorite)
