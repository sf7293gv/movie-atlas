import os
import requests

api_key = os.getenv("OMDB_API_KEY")
if not api_key:
    print("OMDB_API_KEY environment variable not set.")
    exit(1)

# Example movie: "Inception"
url = f"http://www.omdbapi.com/?apikey={api_key}&t=Inception"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if data.get('Response') == 'True':
        print("OMDb API works! Movie title:", data.get('Title'))
    else:
        print("OMDb API error:", data.get('Error'))
else:
    print(f"OMDb API error: {response.status_code}")
