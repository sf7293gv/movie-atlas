from exceptions.movie_error import MovieError
from model.movie_model import Favorite
from apis.tmdb import get_tmdb_full_details as tmdb_getter


def create_new_movie(omdb_data, youtube_video_id, youtube_video_title, tmdb_id, tmdb_details=None):
    """Build the canonical Favorite movie object."""

    # If absolutely no info available
    if not omdb_data and not tmdb_details and not tmdb_id:
        raise MovieError("No movie data available from OMDB or TMDB.")

    # TMDB fallback
    if not tmdb_details and tmdb_id:
        try:
            tmdb_details = tmdb_getter(tmdb_id)
        except Exception:
            tmdb_details = None

    # Prefer TMDB because it's richer
    if tmdb_details:
        title = tmdb_details.get("title", "Unknown Title")
        director = tmdb_details.get("director", "Unknown")
        released = tmdb_details.get("release_date", "Unknown")
        actor_1 = tmdb_details.get("actor_1", "None")
        actor_2 = tmdb_details.get("actor_2", "None")
        poster = tmdb_details.get("poster")
        genre = tmdb_details.get("genre", "Unknown")
        rated = "N/A"
        plot = tmdb_details.get("plot", "No plot available.")

    else:
        # Use OMDB data
        actors = omdb_data.get("Actors", "N/A") or "N/A"
        if actors != "N/A":
            actors_list = [a.strip() for a in actors.split(",")]
            actor_1 = actors_list[0] if len(actors_list) > 0 else "None"
            actor_2 = actors_list[1] if len(actors_list) > 1 else "None"
        else:
            actor_1 = "None"
            actor_2 = "None"

        title = omdb_data.get("Title", "Unknown Title")
        director = omdb_data.get("Director", "Unknown")
        released = omdb_data.get("Released", "Unknown")
        poster = omdb_data.get("Poster")
        genre = omdb_data.get("Genre", "Unknown")
        rated = omdb_data.get("Rated", "N/A")
        plot = omdb_data.get("Plot", "No plot available.")

    youtube_title = youtube_video_title or "Trailer"
    youtube_id = youtube_video_id or ""

    return Favorite(
        tmdb_id,
        title,
        director,
        released,
        actor_1,
        actor_2,
        poster,
        genre,
        rated,
        plot,
        youtube_title,
        youtube_id
    )
