import spacy
import pandas as pd
from collections import Counter
import time
import requests

r = requests.get('https://raw.githubusercontent.com/tabatkins/wordle-list/main/words')
word_list = r.text.split("\n")



df = pd.DataFrame({'word': word_list})
all_words = df['word'].str.cat(sep='')
letter_freq = Counter(all_words)
letter_dict_list = [{'letter': l, 'freq': f} for l, f in letter_freq.items()]
letter_df = pd.DataFrame(letter_dict_list)
letter_df = letter_df.sort_values('freq', ascending=False).reset_index(drop=True)

def get_weight(word):
    weight = 0
    for letter in "".join(set(word)):
        weight += letter_freq[letter]
    return weight

df['weight'] = df['word'].apply(lambda x: get_weight(x))

def no_overlap(word1, word2):
    return len(set(word1 + word2)) == len(set(word1)) + len(set(word2))

df = df.sort_values("weight", ascending=False).reset_index(drop=True)


def pull_weight(word):
    return df.loc[df['word']==word, "weight"].item()

time_start = time.time()
combos = []
for i in range(df.shape[0]):
    word1 = df.iloc[i, 0]
    df_1 = df.iloc[i:].copy()
    mask1 = df_1['word'].apply(lambda x: no_overlap(word1, x))
    df_1 = df_1.loc[mask1]
    word1_weight = pull_weight(word1)
    for j in range(df_1.shape[0]):
        word2 = df_1.iloc[j, 0]
        df_2 = df_1.iloc[j:].copy()
        mask2 = df_2['word'].apply(lambda x: no_overlap(word2, x))
        df_2 = df_2.loc[mask2]
        if df_2.shape[0] > 0:
            word2_weight = pull_weight(word2)
            df_2['final_weight'] = df_2['weight'].apply(lambda x: x + word1_weight + word2_weight)
            df_2 = df_2.sort_values('final_weight', ascending=False).reset_index(drop=True)
            word3 = df_2.iloc[0, 0]
            final_weight = df_2.iloc[0, 2]
            combos.append({'word1': word1, 'word2': word2, 'word3': word3, 'weight': final_weight})
time_end = time.time()
elapsed_time = (time_end - time_start) / 60
print(f"elapsed: {elapsed_time}")

combos_df = pd.DataFrame(combos)

combos_df['weight1'] = combos_df['word1'].apply(lambda x: get_weight(x))
combos_df['weight2'] = combos_df['word2'].apply(lambda x: get_weight(x))
combos_df['weight12'] = combos_df['weight1'] + combos_df['weight2']

combos_df.sort_values(["weight", "weight12", "weight1"], ascending=False).head(20)

max_weight = combos_df['weight'].max()

combos_df.loc[combos_df['weight']==max_weight].sort_values("weight12", ascending=False).head(10)

best_2_words = combos_df[['word1', 'word2', 'weight1', 'weight12']].drop_duplicates()
best_2_words.sort_values(["weight12", 'weight1'], ascending=False).head(20)

best_1_word = combos_df[['word1', 'weight1']].drop_duplicates()
best_1_word.sort_values("weight1", ascending=False).head(10)

combos_df.to_pickle("./data/combos_df.pkl")


combos_df.loc[(combos_df['word1']=="stare") & (combos_df['word2']=="chimp")]


def sort_letters(word):
    return "".join(sorted(word))


df['sorted'] = df['word'].apply(lambda x: sort_letters(x))


df_sorted = df[['sorted', 'weight']].drop_duplicates()
letters1 = df_sorted.iloc[0,0]
mask = (df_sorted['sorted'].apply(lambda x: no_overlap(letters1, x)))
df_sorted = df_sorted.loc[mask]
letters2 = df_sorted.iloc[1,0]
mask = (df_sorted['sorted'].apply(lambda x: no_overlap(letters2, x)))
df_sorted = df_sorted.loc[mask]
letters3 = df_sorted.iloc[0,0]
print(letters1)
print(letters2)
print(letters3)

best_score = letter_df.iloc[:15, 1].sum()


pd.DataFrame({'word': word_list}).to_pickle("./data/word_list.pkl")
df.to_pickle("./data/word_weights.pkl")