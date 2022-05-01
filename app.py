from flask import Flask, render_template
from forms import SearchForm
from data import search_movie, get_data
from flask import request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

movies = get_data()

def get_results(search_form):
    input_str = search_form.data['search_term'].lower()
    res = search_movie(movies, input_str)
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
    movie_data = movies.iloc[int(movie_id) - 1]
    return render_template('movie.html', movie_data=movie_data)

if __name__ == "__main__":
    app.run(debug=True)
