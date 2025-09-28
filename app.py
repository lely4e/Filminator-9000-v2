from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models.models import db, User, Movie
import os
from errors.custom_errors import (
    MovieInDatabaseError,
    MovieNotInDatabaseError,
    NoMovieInApiError,
    FailedQueryError,
)


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the database and the app
db.init_app(app)

# Create an object of your DataManager class
data_manager = DataManager()


@app.route("/", methods=["GET"])
def index():
    """Shows the home page with users."""
    users = data_manager.get_users()
    return render_template(
        "index.html", users=users, message=request.args.get("message")
    )


@app.route("/users", methods=["POST"])
def add_user():
    """Add user to the database."""
    user_name = request.form.get("user_name")

    try:
        data_manager.create_user(user_name)
        message = "User added."
    except FailedQueryError as e:
        message = e
    return redirect(url_for("index", message=message))


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def list_movies(user_id):
    """Page represents all movies from specific user."""
    user = db.session.get(User, user_id)
    if not user:
        return redirect(url_for("index", message="User not found."))

    message = request.args.get("message")
    movies = data_manager.get_movies(user_id)
    return render_template(
        "list_movies.html", user=user, name=user.name, movies=movies, message=message
    )


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    """Add a new movie to a user’s list of favorite movies."""
    user = db.session.get(User, user_id)
    title = request.form.get("title")

    if user and title:
        try:
            data_manager.add_movie(user_id, title)
            message = "Movie added successfully"
        except (MovieInDatabaseError, NoMovieInApiError, FailedQueryError) as e:
            message = e
    elif not user:
        message = "User not found."
    else:
        message = "Title not found."

    return redirect(url_for("list_movies", user_id=user_id, message=message))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id, movie_id):
    """Modify the title of a specific movie in a user’s list,
    without depending on OMDb for corrections."""
    user = db.session.get(User, user_id)
    if user:
        title = request.form.get("title")
        try:
            data_manager.update_movie(movie_id, title)
            message = "Movie updated successfully."
        except (MovieNotInDatabaseError, FailedQueryError) as e:
            message = e

        return redirect(url_for("list_movies", user_id=user_id, message=message))
    else:
        return redirect(url_for("index", message="User not found."))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    """Removes a specific movie from a user’s favorite movie list."""
    user = db.session.get(User, user_id)
    if user:
        try:
            data_manager.delete_movie(movie_id)
            message = "Movie deleted successfully."
        except (MovieNotInDatabaseError, FailedQueryError) as e:
            message = e

        return redirect(
            url_for(
                "list_movies",
                user_id=user_id,
                message=message,
            )
        )
    else:
        return redirect(url_for("index", message="User not found."))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", message=e), 404


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()

    app.run(debug=True)
