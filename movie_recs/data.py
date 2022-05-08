import pandas as pd
from pathlib import Path

def get_data():
    path = Path("movie_recs/data/movie_titles.csv")
    if not path.is_file():
        raise Exception('No movie data found !')
    movies = pd.read_csv(path, sep='|', encoding="ISO-8859-1", index_col=0, dtype={'date': 'Int64'})
    return movies

def search_movie(movies : pd.DataFrame, input_str: str) -> list:
    movies['index_col'] = movies.index
    print(movies)
    results = movies[movies.title.apply(lambda s : s.lower()).str.contains(input_str)]
    titles = results['title'].to_list()
    dates = results['date'].to_list()
    idx = results['index_col'].to_list()
    res = [{'title' : title, 'date' : date, 'id': i} for title, date, i in zip(titles, dates, idx)]
    return res

if __name__ == "__main__":
    movies = get_data()
    input_str = "twi"
    results = search_movie(movies, input_str)
    print(results)