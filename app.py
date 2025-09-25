from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie, User
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(
    app
)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager()  # Create an object of your DataManager class


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


#: The home page of your application.
# Show a list of all registered users and a
# form for adding new users. (This route is GET by default.)


# @app.route("/users", methods=["POST"])
# def list_users():
#     users = data_manager.get_users()
#     return str(users)  # Temporarily returning users as a string
#: When the user submits the “add user” form,
# a POST request is made.
# The server receives the new user info, adds it to
# the database, then redirects back to /.


@app.route("/users/<int:user_id>/movies", methods=["GET"])
# : When you click on a user name, the app retrieves that user’s
# list of favorite movies and displays it.
def list_movies(user_id):
    """Page represents all movies"""
    movies = data_manager.get_movies(user_id)
    if movies:
        return render_template(
            "list_movies.html", movies=movies, message=request.args.get("message", None)
        )
    else:
        return render_template(
            "home.html", movies=[], message="There are no movies found"
        )


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id, title):
    #: Add a new movie to a user’s list of favorite movies.
    user = db.session.get(User, user_id)
    if user:
        data_manager.add_movie(title)
        return redirect(url_for("list_movies", message="Movie was added successfully"))


# @app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
#: Modify the title of a specific movie in a user’s list,
# without depending on OMDb for corrections.


# @app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
#: Remove a specific movie from a user’s favorite movie list.


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()

    app.run()
