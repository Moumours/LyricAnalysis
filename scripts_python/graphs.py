import math
import matplotlib.pyplot as plt

from scripts_python.lyrics_analysis_1 import Lyrics_Analysis_1
from scripts_python.lyrics_utils import Lyrics_Utils


class Graph:
    def __init__(self, spotify_data):
        self.spotify_data = spotify_data
        self.lyrics_analysis = Lyrics_Analysis_1(spotify_data)
        self.lyrics_utils = Lyrics_Utils(spotify_data)

    ## Internal methods

    def draw_sentiment_song(self, sentiment_list, clean_mode=True):
        if clean_mode:
            threshold = 0.0001
            sentiment_list = [value for value in sentiment_list if math.fabs(value) > threshold]

        x_values = list(range(len(sentiment_list)))
        max_x = len(sentiment_list) - 1

        plt.scatter(x_values, sentiment_list)
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.xlim(0, max_x)
        plt.ylim(-1, 1)
        plt.grid(True)
        plt.title('Sentiment Analysis' + (' (Cleaned)' if clean_mode else ''))
        plt.show()

    def draw_feelings_of_one_singer(self, plots_data, size_mode, clean_mode):
        rows = math.ceil(math.sqrt(size_mode))
        cols = math.ceil(size_mode / rows)

        fig, axes = plt.subplots(rows, cols, figsize=(12, 12))

        for i, ax in enumerate(axes.ravel()):
            if i < len(plots_data):
                x_values, y_values, title = plots_data[i]
                if clean_mode:
                    threshold = 0.0001
                    cleaned_y_values = [value if math.fabs(value) > threshold else None for value in y_values]
                    ax.scatter(x_values, cleaned_y_values)
                else:
                    ax.scatter(x_values, y_values)
                ax.set_ylabel('positivy * intensity')
                ax.set_xlim(0, len(x_values) - 1)
                ax.set_ylim(-1, 1)
                ax.grid(True)
                ax.set_title(title)
            else:
                ax.axis('off')

        plt.tight_layout()
        plt.show()



    ## Public methods

    def draw_lyrics_from_one_singer(self, artist_name, clean_mode = True):
        singer_lyrics = self.lyrics_utils.load_lyrics_from_one_singer(artist_name)
        singer_sentiment = self.lyrics_analysis.get_singer_sentiment(singer_lyrics)

        size_mode = len(singer_sentiment)
        self.draw_feelings_of_one_singer(singer_sentiment, size_mode, clean_mode)

    def draw_lyrics_from_one_song(self, artist_name, song_name, clean_mode=True):
        song_lyrics = self.lyrics_utils.load_lyrics_from_one_song(artist_name, song_name)

        sentiment_list = self.lyrics_analysis.get_lyrics_sentiment_song(song_lyrics[2])

        self.draw_sentiment_song(sentiment_list, clean_mode)

    def print_sentiment_from_one_song(self, artist_name, song_name):
        song_lyrics = self.lyrics_utils.load_lyrics_from_one_song(artist_name, song_name)

        sentiment_list = self.lyrics_analysis.get_lyrics_sentiment_song(song_lyrics[2], True)

