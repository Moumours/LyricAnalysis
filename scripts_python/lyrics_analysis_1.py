import matplotlib.pyplot as plt
import math
import numpy as np

from textblob import TextBlob



class Lyrics_Analysis_1:
    def __init__(self, spotify_data):
        self.spotify_data = spotify_data

    #### Sentiment

    def get_lyrics_sentiment_song(self, lyrics_song, printable=False):
        blob = TextBlob(lyrics_song)
        sentiment_list = []

        for sentence in blob.sentences:
            if printable:
                print(sentence.raw, sentence.sentiment.polarity, sentence.sentiment.subjectivity)
            sentiment_list.append(
                sentence.sentiment.polarity * sentence.sentiment.subjectivity)  # Here we have a product of polarity and subjectivity

        return sentiment_list


    ## Sentiment analysis of all songs

    def get_singer_sentiment(self, singer_lyrics):
        all_sentiment = []
        for song in singer_lyrics:
            sentiment_list = self.get_lyrics_sentiment_song(song[2])
            x_values = list(range(len(sentiment_list)))
            all_sentiment.append((x_values, sentiment_list, song[0]))  # Use song[0] to get the song title
        return all_sentiment


    def get_mean_sentiment_singer(self, singer_sentiment, clean_mode):
        all_sentiment = []
        if clean_mode:
            for sentiment in singer_sentiment:
                threshold = 0.0001
                cleaned_y_values = [value for value in sentiment[1] if math.fabs(value) > threshold]
                if cleaned_y_values:
                    x = np.mean(cleaned_y_values)
                    all_sentiment.append((x, sentiment[2], len(cleaned_y_values) * 100 / len(sentiment[1])))
        else:
            for sentiment in singer_sentiment:
                all_sentiment.append((np.mean(sentiment[1]), sentiment[2]))
        return all_sentiment