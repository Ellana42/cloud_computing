from movie_recs import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f"Movie('{self.title}', '{self.date}')"
