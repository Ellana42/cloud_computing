import pandas as pd
from pathlib import Path

def get_data():
    path = Path("data/movie_titles.csv")
    if not path.is_file():
        raise Exception('No movie data found !')
    movies = pd.read_csv("data/movie_titles.csv", sep='|', encoding="ISO-8859-1", index_col=0, dtype={'date': 'Int64'})
    return movies

def search_movie(movies : pd.DataFrame, input_str: str) -> pd.DataFrame:
    results = movies[movies.title.apply(lambda s : s.lower()).str.contains(input_str)]
    return results

if __name__ == "__main__":
    movies = get_data()
    input_str = "twi"
    results = search_movie(movies, input_str)
    print(results)
