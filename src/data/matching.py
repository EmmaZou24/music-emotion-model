import lyricsgenius
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
import os

# authentication
load_dotenv()
genius = lyricsgenius.Genius("GENIUS_API_KEY")
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="SPOTIFY_CLIENT_ID",
    client_secret="SPOTIFY_CLIENT_SECRET"
))

# fetch from genius
def fetch_lyrics(artist, title):
    try:
        song = genius.search_song(title, artist)
        if song:
            return song.lyrics
        return None
    except Exception:
        return None

# fetch from spotify
def fetch_spotify_features(artist, title):
    results = spotify.search(q=f"track:{title} artist:{artist}", type="track", limit=1)
    tracks = results["tracks"]["items"]
    if not tracks:
        return None
    track_id = tracks[0]["id"]
    features = spotify.audio_features(track_id)[0]
    return features