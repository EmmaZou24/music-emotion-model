import lyricsgenius
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
import os

import pandas as pd
import time

# authentication
load_dotenv()
genius = lyricsgenius.Genius(os.getenv("GENIUS_API_KEY"))
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
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
    try:
        results = spotify.search(q=f"track:{title} artist:{artist}", type="track", limit=1)
        tracks = results["tracks"]["items"]
        if not tracks:
            return None
        track_id = tracks[0]["id"]
        features = spotify.audio_features(track_id)[0]
        return features
    except Exception:
        return None

def collect(output_path, checkpoint_every=100):
    df_tags = pd.read_csv("data/raw/autotagging_moodtheme.tsv", sep="\t")
    df_meta = pd.read_csv("../mtg-jamendo-dataset/data/raw.meta.tsv", sep="\t")
    df = pd.merge(df_tags, df_meta[["TRACK_ID", "ARTIST_NAME", "TRACK_NAME"]], 
                on="TRACK_ID", how="left")

    # load existing results if resuming from a checkpoint
    if os.path.exists(output_path):
        df_existing = pd.read_csv(output_path)
        completed_ids = set(df_existing["TRACK_ID"].tolist())
        results = df_existing.to_dict("records")
        print(f"Resuming! {len(completed_ids)} tracks already processed")
    else:
        completed_ids = set()
        results = []

    for i, row in df.iterrows():
        track_id = row["track_id"]

        # skip already-processed tracks
        if track_id in completed_ids:
            continue

        artist = row["ARTIST_NAME"]
        title = row["TRACK_NAME"]
        tags = row["TAGS"]

        # fetch from both APIs
        lyrics = fetch_lyrics(artist, title)
        spotify_features = fetch_spotify_features(artist, title)

        sample = {
            "track_id": track_id,
            "artist": artist,
            "title": title,
            "tags": tags,
            "lyrics": lyrics,
        }

        # add spotify features into the sample if found
        if spotify_features:
            sample.update(spotify_features)
        else:
            for col in ["valence","energy","danceability",
                        "tempo","loudness","acousticness",
                        "instrumentalness","speechiness",
                        "liveness","mode","key",
                        "time_signature"]:
                sample[col] = None
        results.append(sample)

        # checkpoint: save progress every N tracks
        if (i+1) % checkpoint_every == 0:
            pd.DataFrame(results).to_csv(output_path, index=False)
            print(f"Checkpoint saved @ {len(results)} tracks")

        # rate limiting...
        time.sleep(0.5)

    df_out = pd.DataFrame(results)
    df_out.to_csv(output_path, index=False)
    return df_out

if __name__ == "__main__":
    collect(output_path="data/processed/matched_tracks.csv")