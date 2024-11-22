import pandas as pd

def import_data():
    """
    Import Cleveland public comments from data source

    returns: pandas DataFrame with public comments
    """
    df = pd.read_csv("data/cleveland_public_comments.csv")
    return df

def fetch_row(df, row_num):
    """
    Fetch row from DataFrame by row number

    df: Input DataFrame
    row_num: number of row to fetch

    returns: dictionary with data from a row
    """
    row = df.iloc[row_num]
    return dict(row)

def print_row(row_dict):
    """
    Print data from the row dictionary

    row_dict: dictionary of row data
    """
    print("----------------")
    print("name:  ", row_dict['name'])
    print("date:  ", row_dict['date'])
    print("title: ", row_dict['title'])
    print("content:\n", row_dict['content'])
    print("----------------")


def print_tokens(doc):
    """
    Print the tokens from a SpaCy doc so they are easy to read

    doc: a SpaCy doc    
    """
    MAX_WORD_LEN = 25
    max_len = max([len(token.text) for token in doc if len(token.text) <= MAX_WORD_LEN])
    first_line = "TOKEN" + " "*(1+max_len-5) + "LEMMA" + " "*(1+max_len-5) + "POS"
    print(first_line)
    print("-"*len(first_line))
    for token in doc:
        if len(token.text) > MAX_WORD_LEN:
            continue
        if token.pos_ not in ['PUNCT', 'SPACE']:
            print(token.text + " "*(1 + max_len-len(token.text)) + token.lemma_ + " "*(1 + max_len-len(token.lemma_)) + token.pos_)
