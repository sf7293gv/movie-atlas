import os
import requests

api_key = os.getenv("TMDB_API_KEY")
if not api_key:
    print("TMDB_API_KEY environment variable not set.")
    exit(1)

url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=en-US&page=1"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("TMDB API works! Here are the first 3 movie titles playing now:")
    for movie in data.get('results', [])[:3]:
        print("-", movie.get('title'))
else:
    print(f"TMDB API error: {response.status_code}")
