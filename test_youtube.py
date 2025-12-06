import os
from googleapiclient.discovery import build

api_key = os.getenv("YOUTUBE_API")
if not api_key:
    print("YOUTUBE_API environment variable not set.")
    exit(1)

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.search().list(
    q="Inception Trailer",
    part="snippet",
    maxResults=3,
    type="video"
)
response = request.execute()

print("YouTube API works! Here are 3 video titles for 'Inception Trailer':")
for item in response.get('items', []):
    print("-", item['snippet']['title'])
