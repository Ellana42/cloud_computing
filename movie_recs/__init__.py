from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from movie_recs.data import get_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev' # TODO change for finished dev
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
movies_df = get_data()

from movie_recs import routes
