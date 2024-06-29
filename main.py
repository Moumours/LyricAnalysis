from gen_Spotify import SpotifyData

if __name__ == "__main__":
    spotify_data = SpotifyData()

    if spotify_data.sp:
        spotify_data.get_user_data()
        spotify_data.load_spotify_favorite_songs()