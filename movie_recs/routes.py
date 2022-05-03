from movie_recs import app, db, movies_df
from flask import render_template, request
from movie_recs.data import search_movie
from movie_recs.forms import SearchForm
from movie_recs.models import Reviews

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

@app.route("/movie")
def movie_page():
    movie_id = request.args.get('movie_id')
    movie_data = movies_df.iloc[int(movie_id) - 1]
    return render_template('movie.html', movie_data=movie_data)
