from flask import Flask, render_template, redirect, request, session, url_for, flash
import model
app = Flask(__name__)
app.secret_key = "thisisasecret"


@app.route("/")
def index():
    session_user_id = session.get('session_user_id')
    if session_user_id:
        user = model.get_user_by_id(session_user_id)
        return render_template("main.html", user_id = session_user_id, user = user)
    return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    submitted_email = request.form.get('email')
    submitted_password = request.form.get('password')
    
    user_id = model.login(submitted_email, submitted_password)
    if user_id:
        session['session_user_id'] = user_id 
        return redirect(url_for("index"))
    else:
        flash("Username or password incorect.")
        return redirect(url_for("process_login"))

@app.route("/register")
def get_registration_info():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_user():
    submitted_email = request.form.get('email')
    submitted_password = request.form.get('password')
    submitted_password_verify = request.form.get('password_verify')
    submitted_age = request.form.get('age')
    submitted_gender = request.form.get('gender')
    submitted_zipcode = request.form.get('zipcode')

    if model.check_for_user(submitted_email):
        flash("This user already exists.")
        return redirect(url_for("get_registration_info"))

    elif submitted_password != submitted_password_verify:
        flash("Passwords do not match")
        return redirect(url_for("get_registration_info"))
    else:
        model.register_user(submitted_email, submitted_password, submitted_age, submitted_gender, submitted_zipcode)
        flash("You've been added. Please sign-in below.")
        return redirect(url_for("index"))

@app.route("/user/<user_id>")
def view_user(user_id):
    ratings_list= model.get_ratings_by_user_id(user_id)
    return render_template("view_user.html", user_id=user_id, ratings_list=ratings_list)

@app.route("/movie_list") 
def movie_list():
    movie_list = model.get_all_movies()
    return render_template("movie_list.html", movies=movie_list)

@app.route("/user_list")
def user_list():
    user_list = model.get_all_users()
    return render_template("user_list.html", users=user_list)

@app.route("/view_movie/<movie_id>")
def view_movie(movie_id):
    movie_ratings=model.get_ratings_by_movie_id(movie_id) #list of rating objects

    movie = model.get_movie_by_id(movie_id)
    session_user_id = session.get('session_user_id')
    user_rating = None
    user_prediction = None
    eye_rating = None
    eye_prediction = None
    beratement=None
    average = model.average_ratings(movie_ratings)
    if session_user_id:
        user_rating, user_prediction = model.get_rating(session_user_id, movie_id, movie_ratings)
        eye_rating, eye_prediction = model.get_rating(1, movie_id, movie_ratings) #make eye_id
        if not eye_rating:
            eye_judgement = eye_prediction
        else: 
            eye_judgement = eye_rating
        if not user_rating:
            difference = None
        else:
            user_judgement = user_rating
            difference = abs(eye_judgement - user_judgement)

            messages = [ "I suppose you don't have such bad taste after all.",
                 "Why would anyone ever listen to your opinion.",
                 "Words fail me, as your taste in movies has clearly failed you.",
                 "That movie is great. For a clown to watch. Idiot.", "WHAT?!?! How could you possibly think that about this movie?."]

            beratement = messages[int(difference)]

    return render_template("view_movie.html", movie_ratings=movie_ratings, movie=movie, session_user_id= session_user_id, prediction=user_prediction, user_rating=user_rating, beratement=beratement, average=average)

@app.route("/view_movie/<movie_id>", methods=["POST"])
def add_rating(movie_id):
    user_id = session.get("session_user_id")
    rating = request.form.get("new_rating")

    model.add_rating(movie_id, user_id, rating)
    return redirect(url_for("view_movie", movie_id=movie_id))


@app.route("/clear")
def clear():
    session.clear()
    return redirect(url_for("index"))





if __name__ == "__main__":
    app.run(debug = True)

