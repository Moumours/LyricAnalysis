from lyrics_utils import Lyrics_Utils
from gen_Spotify import SpotifyData
import time

def main():
    spotify_data = SpotifyData()

    if spotify_data.sp:
        spotify_data.get_user_data()
        spotify_data.load_spotify_favorite_songs()

        print("On commence les paroles")
        start_time = time.time()

        lyrics_analysis = Lyrics_Utils(spotify_data)
        lyrics_list = lyrics_analysis.get_all_lyrics_favorite()
        lyrics_analysis.save_lyrics_to_file(lyrics_list)

        end_time = time.time() - start_time
        execution_time = end_time - start_time

        print(f"Les paroles de vos chansons favorites ont été téléchargées et sauvegardées. Temps écoulé : {execution_time:.2f} secondes.")



if __name__ == "__main__":
    main()