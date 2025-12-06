from exceptions.movie_error import MovieError
from model.movie_model import Favorite
from apis.tmdb import get_tmdb_full_details as tmdb_getter  # allow fallback if needed

def create_new_movie(omdb_data, youtube_video_id, youtube_video_title, tmdb_id, tmdb_details=None):
    """
    Build and return a Favorite object.
    Accepts:
      - omdb_data: dict or None
      - youtube_video_id/title: strings or None
      - tmdb_id: id or None
      - tmdb_details: optional dict as returned by apis.tmdb.get_tmdb_full_details()
    """

    # If OMDB and TMDB details are both missing, we can't build a movie
    if not omdb_data and not tmdb_details and not tmdb_id:
        raise MovieError("No movie data available from OMDB or TMDB.")

    # If tmdb_details wasn't provided but we have an id, try to fetch it (best-effort)
    if not tmdb_details and tmdb_id:
        try:
            tmdb_details = tmdb_getter(tmdb_id)
        except Exception as e:
            print("create_new_movie: TMDB fetch failed:", e)
            tmdb_details = None

    # Prefer TMDB details when present (richer)
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
        # Use OMDB data (safely)
        if not omdb_data:
            # nothing to use
            raise MovieError("OMDB data missing and no TMDB details available.")
        actors = omdb_data.get("Actors", "N/A") or "N/A"
        if actors != "N/A":
            actors_list = [a.strip() for a in actors.split(",") if a.strip()]
            actor_1 = actors_list[0] if len(actors_list) >= 1 else "None"
            actor_2 = actors_list[1] if len(actors_list) >= 2 else "None"
        else:
            actor_1 = "None"
            actor_2 = "None"

        title = omdb_data.get("Title") or "Unknown Title"
        director = omdb_data.get("Director") or "Unknown"
        released = omdb_data.get("Released") or "Unknown"
        poster = omdb_data.get("Poster") or None
        genre = omdb_data.get("Genre") or "Unknown"
        rated = omdb_data.get("Rated") or "N/A"
        plot = omdb_data.get("Plot") or "No plot available."

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
