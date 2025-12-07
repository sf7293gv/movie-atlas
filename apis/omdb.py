import requests
import os

OMDB_API_KEY = os.environ.get("OMDB_KEY")

# -----------------------------------------
# Get movie by Title + Year (fallback only)
# -----------------------------------------
def get_movie_data(title, release_year):
    if not OMDB_API_KEY:
        print("OMDB_KEY missing from environment!")
        return None

    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"

        if release_year:
            url += f"&y={release_year}"

        data = requests.get(url).json()

        if data.get("Response") == "False":
            return None

        return data

    except Exception as e:
        print("OMDB title lookup failed:", e)
        return None


# -----------------------------------------
# Get movie using IMDB ID (preferred method!)
# -----------------------------------------
def get_movie_by_imdb(imdb_id):
    if not imdb_id:
        return None

    if not OMDB_API_KEY:
        print("OMDB_KEY missing from environment!")
        return None

    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"
        data = requests.get(url).json()

        if data.get("Response") == "False":
            return None

        return data

    except Exception as e:
        print("OMDB IMDb lookup failed:", e)
        return None
