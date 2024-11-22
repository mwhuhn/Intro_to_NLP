import pandas as pd
import random

words = pd.read_pickle("./data/word_list.pkl")
weights = pd.read_pickle("./data/word_weights.pkl")


def choose_word(df):
    max_i = df.shape[0]
    n = random.randint(0, max_i)
    