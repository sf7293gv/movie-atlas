from apis import omdb, tmdb, youtube_api
from create_new_movie import create_new_movie


def assemble_selected_movie_data(title, release_date, tmdb_id):
    """Return a fully assembled movie object using TMDB + OMDB + YouTube."""

    if not title:
        return None

    # Extract year from release_date for OMDB lookup
    try:
        year = release_date.split("-")[0]
    except:
        year = None

    # --- Fetch OMDB ---
    try:
        omdb_data = omdb.get_movie_data(title, year)
        if omdb_data and omdb_data.get("Response") == "False":
            omdb_data = None
    except Exception as e:
        print("OMDB error:", e)
        omdb_data = None

    # --- Fetch TMDB full details ---
    try:
        tmdb_details = tmdb.get_tmdb_full_details(tmdb_id)
    except Exception as e:
        print("TMDB error:", e)
        tmdb_details = None

    # --- YouTube trailer ---
    try:
        yt_title, yt_id = youtube_api.movie_trailer(title)
    except Exception:
        yt_title, yt_id = None, None

    # If we at least have TMDB or OMDB, create the movie object
    if not omdb_data and not tmdb_details:
        print("No movie data available from OMDB or TMDB for:", title)
        return None

    movie = create_new_movie(
        omdb_data,
        yt_id,
        yt_title,
        tmdb_id,
        tmdb_details=tmdb_details
    )

    return movie
