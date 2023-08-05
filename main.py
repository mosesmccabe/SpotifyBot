from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("REDIRECT_URI")


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope="playlist-modify-private"))

user_info = sp.current_user()
user_id = user_info["id"]
# print(user_id)
# queue = "track:Incomplete artist:Sisqo"
# song_uri = sp.search(q=queue, limit=2, type="track", market="ES")
# pprint(song_uri['tracks']['items'][0]['uri'])

yyyy_mm_dd = input("Which year do you want to travel to? Type the date in this format YYYY-MM_DD: ")

billboard_url = "https://www.billboard.com/charts/hot-100/"

response = requests.get(f"{billboard_url}{yyyy_mm_dd}")
billboard_top = response.text

soup = BeautifulSoup(billboard_top, "html.parser")

# get songs
songs = soup.find_all(name="div", class_="o-chart-results-list-row-container")
song_titles = [title.select_one(selector="li h3").getText().strip() for title in songs]
print("BillBoard Top 100 songs scraped")

# Used Spotipy to get songs uri
songs_uri = []
year = yyyy_mm_dd.split("-")[0]
for song_title in song_titles:
    q = f"track:{song_title} year:{year}"
    song_url = sp.search(q=q, type="track", market="ES")
    try:
        song_uri = song_url['tracks']['items'][0]['uri']
    except IndexError:
        continue
    else:
        songs_uri.append(song_uri)

print("Song URI retrieve for Spotify: successful ")

# Create playlist for a user
playlist_id = sp.user_playlist_create(user=user_id, name=f"{yyyy_mm_dd} Billboard 100", public=False, description=f"Travel back to {yyyy_mm_dd}")['id']
print("Playlist created on Spotify: Successful")


sp.playlist_add_items(playlist_id=playlist_id, items=songs_uri)

print("Songs added to Spotify Playlist: Successful")