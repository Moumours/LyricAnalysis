import os
from dotenv import load_dotenv
import json
import time
import lyricsgenius

class Lyrics_Utils:
    def __init__(self, spotify_data):
        self.spotify_data = spotify_data
        load_dotenv()
        self.client_id = os.getenv("GENIUS_CLIENT_ID")
        self.client_secret = os.getenv("GENIUS_CLIENT_SECRET")
        self.client_access_token = os.getenv("GENIUS_CLIENT_ACCESS_TOKEN")

    def get_all_songs_name(self, artist_name):
        songs_by_artist = []
        for song in self.spotify_data.user_data['favorite_songs']:
            if song[1] == artist_name:
                songs_by_artist.append(song[0])
        return songs_by_artist

    def get_all_artists_name(self):
        data = self.spotify_data.user_data['favorite_songs']
        artists = list({song[1] for song in data})
        return artists

    def get_lyrics_one_singer(self, songs, singer):
        genius = lyricsgenius.Genius(self.client_access_token)
        lyrics_list = []
        for song_name in songs:
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
        with open("./JSON_files/AllLyricsFavorite.json", "w") as file:
            json.dump(lyrics_list, file)

    def load_lyrics_from_file(self):
        file_path = "./JSON_files/AllLyricsFavorite.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        else:
            print(f"Le fichier {file_path} n'existe pas.")
            return []

    def load_lyrics_from_one_singer(self, singer_name):
        file_path = "./JSON_files/AllLyricsFavorite.json"

        if not os.path.exists(file_path):
            print(f"Le fichier {file_path} n'existe pas.")
            return []
        with open(file_path, "r") as file:
            try:
                all_lyrics = json.load(file)
            except json.JSONDecodeError:
                print(f"Erreur de décodage JSON dans le fichier {file_path}.")
                return []

        singer_lyrics = [lyric for lyric in all_lyrics if lyric[1].lower() == singer_name.lower()]

        return singer_lyrics


    def load_lyrics_from_one_song(self, singer_name, song_name):
        file_path = "./JSON_files/AllLyricsFavorite.json"

        if not os.path.exists(file_path):
            print(f"Le fichier {file_path} n'existe pas.")
            return []
        with open(file_path, "r") as file:
            try:
                all_lyrics = json.load(file)
            except json.JSONDecodeError:
                print(f"Erreur de décodage JSON dans le fichier {file_path}.")
                return []

        song_lyrics = [lyric for lyric in all_lyrics if
                       lyric[1].lower() == singer_name.lower() and lyric[0].lower() == song_name.lower()]

        return song_lyrics[0]

    def load_lyrics_except_artists(self, artist_names_to_exclude):
        file_path = "./JSON_files/AllLyricsFavorite.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                all_lyrics = json.load(file)
                filtered_lyrics = [lyric for lyric in all_lyrics if lyric[1] not in artist_names_to_exclude]
                return filtered_lyrics
        else:
            print(f"Le fichier {file_path} n'existe pas.")
            return []
    def initialize_lyrics(self):
        print("On commence les paroles")
        start_time = time.time()

        lyrics_list = self.get_all_lyrics_favorite()
        self.save_lyrics_to_file(lyrics_list)

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Les paroles de vos chansons favorites ont été téléchargées et sauvegardées. Temps écoulé : {execution_time:.2f} secondes.")
