import requests
import os
from pprint import pprint

OMDB_KEY = os.environ.get("OMDB_KEY")

def test_movie(title, year=None):
    if year:
        url = f"http://www.omdbapi.com/?t={title}&y={year}&apikey={OMDB_KEY}"
    else:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_KEY}"

    print("\n====================================")
    print(f"Testing OMDb for: {title} ({year})")
    print("URL:", url)
    print("====================================")

    response = requests.get(url).json()
    pprint(response)

    if response.get("Response") == "False":
        print("❌ OMDb could not find this movie.")
    else:
        print("✅ OMDb data successfully returned!")

if __name__ == "__main__":
    # Try any movie you want
    test_movie("Zootopia 2", "2025")
    test_movie("Inception", "2010")
    test_movie("Kantara", "2022")
