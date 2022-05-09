import fuzzywuzzy
import jaro
import re
import unicodedata

def normalize_unicode_to_ascii(data):
    normal = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
    val = normal.decode("utf-8")
    val = val.lower()
    # remove special characters
    val = re.sub('[^A-Za-z0-9 ]+', ' ', val)
    # remove multiple spaces
    val = re.sub(' +', ' ', val)
    return val

def similarity_calculator(word1, word2):
    W1 = normalize_unicode_to_ascii(word1)
    W2 = normalize_unicode_to_ascii(word2)
    score_1 = fuzz.ratio(W1, W2) 
    score_2 = jaro.jaro_winkler_metric(W1, W2) 
    return  score_2 + score_1/100

def search_movie(movies : pd.DataFrame, input_str: str) -> list:
    res = movies.title.apply(lambda x : similarity_calculator(x,input_str)).sort_values(ascending=False).index.to_list()[:10]
    movies['index_col'] = movies.index
    results = movies[movies.title.apply(lambda s : s.lower()).str.contains(input_str)]
    idx = results['index_col'].to_list()
    return list(set(idx) | set(res))