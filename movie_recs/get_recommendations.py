from movie_recs import movies_df

def dummy_rec():
    return movies_df.sample(5)

def reviews_to_array():
    pass

def get_recs(current_user):
    movies_df['index_col'] = movies_df.index
    results = dummy_rec()
    titles = results['title'].to_list()
    dates = results['date'].to_list()
    idx = results['index_col'].to_list()
    res = [{'title' : title, 'date' : date, 'id': i} for title, date, i in zip(titles, dates, idx)]
    return res
