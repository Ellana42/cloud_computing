from movie_recs import app, db, movies_df, bcrypt
from flask import render_template, request, url_for, flash, redirect
from movie_recs.data import search_movie
from movie_recs.forms import SearchForm, ReviewForm, RegistrationForm, LoginForm
from movie_recs.models import Review, User
from flask_login import login_user, current_user, logout_user, login_required

@app.before_first_request
def create_tables():
    db.create_all()

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
    movie_id = int(request.args.get('movie_id'))
    if current_user.is_authenticated:
        past_review = Review.query.filter_by(movie_id=movie_id, author=current_user).first()
    else:
        past_review = None
    if (past_review is not None):
        review_form = ReviewForm(rating=past_review.rating)
    else :
        review_form = ReviewForm()
    movie_data = movies_df.iloc[movie_id - 1]
    if review_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You are not authenticated, you cannot rate movies !", "danger")
        else :
            print("Rating")
            print(review_form.data['rating']) # Does not update on submit for some reason
            new_review = Review(rating=review_form.data['rating'], movie_id=movie_id, author=current_user)
            if (past_review is not None):
                print("Deleting")
                db.session.delete(past_review)
                db.session.commit()
            db.session.add(new_review)
            db.session.commit()
            flash('Your review has been saved!', 'success')
            return redirect(url_for('home'))
    return render_template('movie.html', form=review_form, movie_data=movie_data)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
