import os
import requests

tmdb_key = os.environ.get("TMDB_KEY")

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


# ============================================================
# GET POPULAR MOVIES (Homepage List)
# ============================================================

def get_tmdb():
    """Return a list of movies for the homepage, including genre IDs."""

    if not tmdb_key:
        print("TMDB_KEY missing")
        return []

    url = f"{TMDB_BASE_URL}/movie/popular?api_key={tmdb_key}&language=en-US&page=1"

    try:
        response = requests.get(url).json()

        if "results" not in response:
            print("TMDB returned no results.")
            return []

        movies = []

        for m in response["results"]:
            poster_path = m.get("poster_path")
            poster_url = TMDB_IMAGE_BASE + poster_path if poster_path else None

            movies.append({
                "title": m.get("title"),
                "release_date": m.get("release_date"),
                "id": m.get("id"),
                "poster": poster_url,
                "poster_path": poster_path,
                "genre_ids": m.get("genre_ids", [])  # ★ REQUIRED FOR AI HELPER
            })

        return movies

    except Exception as e:
        print("TMDB list error:", e)
        return []


# ============================================================
# GET FULL MOVIE DETAILS (Used on Movie Details Page)
# ============================================================

def get_tmdb_full_details(tmdb_id):
    """Return detailed TMDB data for a single movie."""
    
    if not tmdb_key:
        print("TMDB_KEY missing")
        return None

    try:
        # Movie details
        details = requests.get(
            f"{TMDB_BASE_URL}/movie/{tmdb_id}?api_key={tmdb_key}&language=en-US"
        ).json()

        # Cast / crew details
        credits = requests.get(
            f"{TMDB_BASE_URL}/movie/{tmdb_id}/credits?api_key={tmdb_key}&language=en-US"
        ).json()

        # Poster
        poster_path = details.get("poster_path")
        poster_url = TMDB_IMAGE_BASE + poster_path if poster_path else None

        # Director
        director = "Unknown"
        for person in credits.get("crew", []):
            if person.get("job") == "Director":
                director = person.get("name")
                break

        # Actors
        cast = credits.get("cast", [])
        actor_1 = cast[0]["name"] if len(cast) > 0 else "Unknown"
        actor_2 = cast[1]["name"] if len(cast) > 1 else "Unknown"

        # Genres
        genres = ", ".join([g["name"] for g in details.get("genres", [])])

        return {
            "title": details.get("title"),
            "release_date": details.get("release_date"),
            "plot": details.get("overview"),
            "genre": genres,
            "poster": poster_url,
            "poster_path": poster_path,
            "director": director,
            "actor_1": actor_1,
            "actor_2": actor_2
        }

    except Exception as e:
        print("TMDB full detail error:", e)
        return None
