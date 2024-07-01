import os
from dotenv import load_dotenv
import json

import matplotlib.pyplot as plt
import math
import numpy as np

from textblob import TextBlob
import lyricsgenius



class Lyrics_Utils:
    def __init__(self, spotify_data):
        self.spotify_data = spotify_data
        load_dotenv()
        self.client_id = os.getenv("GENIUS_CLIENT_ID")
        self.client_secret = os.getenv("GENIUS_CLIENT_SECRET")
        self.client_access_token = os.getenv("GENIUS_CLIENT_ACCESS_TOKEN")

    def getAllSongsName(self, artist_name):
        songs_by_artist = []

        for song in self.spotify_data.user_data['favorite_songs']:
            if song[1] == artist_name:
                songs_by_artist.append(song[0])

        return songs_by_artist

    ## Recuperer les paroles des chansons

    def get_lyrics_one_singer(self, songs, singer):
        # Exemple utilisation:
        # songs = ["Song1", "Song2", "Song3"]
        # singer = "Artist1"
        # lyrics = get_lyrics_one_singer(songs, singer)
        genius = lyricsgenius.Genius(self.client_access_token)

        lyrics_list = []
        for song_name in songs:
            # Concatenate singer and song_name for better search results
            search_query = f"{singer} {song_name}"

            try:
                song = genius.search_song(search_query)
                if song:
                    song_lyrics = song.lyrics.replace("\n", ". ")
                    lyrics_list.append([song_name, song_lyrics])
                else:
                    print(f"Lyrics not found for {song_name} by {singer}")
            except TimeoutError as e:
                print(f"Timeout error occurred for {song_name}: {e}")
            except Exception as e:
                print(f"An error occurred for {song_name}: {e}")

        return lyrics_list

    def get_all_lyrics_favorite(self):
        genius = lyricsgenius.Genius(self.client_access_token)

        lyrics_list = []

        for song_name in self.spotify_data.user_data['favorite_songs']:

            search_query = f"{song_name[1]} {song_name[0]}"

            try:
                song = genius.search_song(search_query)
                if song:
                    song_lyrics = song.lyrics.replace("\n", ". ")
                    lyrics_list.append([song_name[0], song_name[1], song_lyrics])
                else:
                    print(f"Lyrics not found for {song_name[0]} by {song_name[1]}")
            except TimeoutError as e:
                print(f"Timeout error occurred for {song_name}: {e}")
            except Exception as e:
                print(f"An error occurred for {song_name}: {e}")

        return lyrics_list

    def save_lyrics_to_file(self, lyrics_list):

        with open(
                "./JSON_files/AllLyricsSFavorite.json",
                "w") as file:
            json.dump(lyrics_list, file)

    def load_lyrics_from_file(self):
        file_path = "./JSON_files/AllLyricsSFavorite.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        else:
            print(f"Le fichier {file_path} n'existe pas.")
            return []

    def load_lyrics_from_one_singer(self, singer_name):
        file_path = "./JSON_files/AllLyricsSFavorite.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                all_lyrics = json.load(file)
                singer_lyrics = [lyric for lyric in all_lyrics if lyric[1] == singer_name]
                return singer_lyrics
        else:
            print(f"Le fichier {file_path} n'existe pas.")
            return []

    def load_lyrics_except_artists(artist_names_to_exclude):
        # Format liste []
        file_path = "./JSON_files/AllLyricsSFavorite.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                all_lyrics = json.load(file)
                filtered_lyrics = [lyric for lyric in all_lyrics if lyric[1] not in artist_names_to_exclude]
                return filtered_lyrics
        else:
            print(f"Le fichier {file_path} n'existe pas.")
            return []