from flask import Flask, render_template
from forms import SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

@app.route("/")
def home():
    search_form = SearchForm()
    return render_template('home.html', form=search_form)

if __name__ == "__main__":
    app.run(debug=True)
