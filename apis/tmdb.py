import os
import requests

tmdb_key = os.environ.get("TMDB_KEY")

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def get_tmdb():
    """Return a list of movies for the homepage."""
    if not tmdb_key:
        print("TMDB_KEY missing")
        return []

    url = f"{TMDB_BASE_URL}/movie/popular?api_key={tmdb_key}&language=en-US&page=1"

    try:
        res = requests.get(url).json()
        if "results" not in res:
            return []

        movies = []

        for m in res["results"]:
            poster_path = m.get("poster_path")
            poster_url = TMDB_IMAGE_BASE + poster_path if poster_path else None

            movies.append({
                "title": m.get("title"),
                "release_date": m.get("release_date"),
                "tmdb_id": m.get("id"),
                "poster": poster_url,
                "poster_path": poster_path  # raw path if needed
            })

        return movies

    except Exception as e:
        print("TMDB list error:", e)
        return []


def get_tmdb_full_details(tmdb_id):
    """Return detailed TMDB data."""
    if not tmdb_key:
        print("TMDB_KEY missing")
        return None

    try:
        details = requests.get(
            f"{TMDB_BASE_URL}/movie/{tmdb_id}?api_key={tmdb_key}&language=en-US"
        ).json()

        credits = requests.get(
            f"{TMDB_BASE_URL}/movie/{tmdb_id}/credits?api_key={tmdb_key}&language=en-US"
        ).json()

        # poster
        poster_path = details.get("poster_path")
        poster_url = TMDB_IMAGE_BASE + poster_path if poster_path else None

        # director
        director = "Unknown"
        for person in credits.get("crew", []):
            if person.get("job") == "Director":
                director = person.get("name")
                break

        # cast
        cast = credits.get("cast", [])
        actor_1 = cast[0]["name"] if len(cast) > 0 else "Unknown"
        actor_2 = cast[1]["name"] if len(cast) > 1 else "Unknown"

        # genres
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

    except:
        return None
