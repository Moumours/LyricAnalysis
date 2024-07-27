from scripts_python.lyrics_utils import Lyrics_Utils
from scripts_python.gen_Spotify import SpotifyData
from scripts_python.lyrics_analysis_1 import Lyrics_Analysis_1
from scripts_python.graphs import Graph





def main():
    spotify_data = SpotifyData()
    lyrics_analysis = Lyrics_Analysis_1()
    lyrics_utils = Lyrics_Utils()
    graph = Graph(spotify_data)

    if spotify_data.sp:
        spotify_data.get_user_data()
        spotify_data.load_spotify_favorite_songs()

        # initialize_lyrics(spotify_data)
        graph.draw_lyrics_from_one_singer(lyrics_analysis, lyrics_utils)
        # draw_lyrics_from_one_song(spotify_data, True)
        # print_sentiment_from_one_song(spotify_data)






if __name__ == "__main__":
    main()