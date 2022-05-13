from movie_recs import movies_df
from matrix_completion_recommender_system.simple_recommender_system import recommender_system
from pathlib import Path
from movie_recs.models import Review
import numpy as np

def dummy_rec():
    return movies_df.sample(5)

def reviews_to_array(user):
    reviews = Review.query.filter_by(author=user).all()
    ratings = {review.movie_id - 1: review.rating for review in reviews}
    ratings_array = np.array([0 if idx not in ratings.keys() else ratings[idx] for idx in range(2993)])
    return (ratings_array)

def get_recommendation(user, nb_to_rec=5):
    weights_path = Path('matrix_completion_recommender_system/reduced_netflix_model.pickle')
    recommender = recommender_system(100, 0.0001, 1)
    recommender.load_model(weights_path)
    user_reviews = reviews_to_array(user)
    recs = recommender.get_recommendation_new_user(user_reviews, nb_to_rec)
    recs_df = movies_df.loc[movies_df.index[recs]]
    return (recs_df)

def get_recs(user):
    movies_df['index_col'] = movies_df.index
    results = get_recommendation(user)
    titles = results['title'].to_list()
    dates = results['date'].to_list()
    idx = results['index_col'].to_list()
    res = [{'title' : title, 'date' : date, 'id': i} for title, date, i in zip(titles, dates, idx)]
    return res
