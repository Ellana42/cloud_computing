from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    search_term = StringField("Movie Name", 
                              validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField("Search")

class ReviewForm(FlaskForm):
    rating = SelectField("Rating", choices=range(6), coerce=int)
    submit = SubmitField("Rate")
