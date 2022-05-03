from movie_recs import app, db, movies_df
from flask import render_template, request
from movie_recs.data import search_movie
from movie_recs.forms import SearchForm, ReviewForm
from movie_recs.models import Review

# TODO change db model

def get_results(search_form):
    input_str = search_form.data['search_term'].lower()
    res = search_movie(movies_df, input_str)
    return res

@app.route("/", methods=['GET', 'POST'])
def home():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        results = get_results(search_form)
    else: 
        results = []
    return render_template('home.html', form=search_form, results=results)

@app.route("/movie", methods=['GET', 'POST'])
def movie_page():
    review_form = ReviewForm()
    movie_id = request.args.get('movie_id')
    movie_data = movies_df.iloc[int(movie_id) - 1]
    if review_form.validate_on_submit():
        review = Review(rating=review_form.data['rating'], movie_id=int(movie_id))
    else:
        pass
    return render_template('movie.html', form=review_form, movie_data=movie_data)
