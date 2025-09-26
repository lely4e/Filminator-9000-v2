from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie, User
import os
from errors.custom_errors import MyCustomError


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
def home():
    users = data_manager.get_users()
    return render_template("home.html", users=users)


@app.route("/users", methods=["POST"])
def add_user():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        add_user = data_manager.create_user(user_name)
        users = data_manager.get_users()
        return redirect(url_for("home", message="User added"))


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def list_movies(user_id):
    """Page represents all movies from specific user"""
    user = db.session.get(User, user_id)
    if not user:
        return redirect(url_for("home", message="User not found."))

    message = request.args.get("message")
    movies = data_manager.get_movies(user_id)
    return render_template(
        "list_movies.html", user=user, name=user.name, movies=movies, message=message
    )


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    """Add a new movie to a user’s list of favorite movies."""
    user = db.session.get(User, user_id)
    if not user:
        return redirect(
            url_for("list_movies", user_id=user_id, message="No user found.")
        )

    title = request.form.get("title")
    if not title:
        return redirect(
            url_for("list_movies", user_id=user_id, message="No title found.")
        )

    try:
        data_manager.add_movie(user_id, title)
        return redirect(
            url_for("list_movies", user_id=user_id, message="Movie added successfully")
        )
    except MyCustomError as e:
        return redirect(url_for("list_movies", user_id=user_id, message=f"{e}"))


# @app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
#: Modify the title of a specific movie in a user’s list,
# without depending on OMDb for corrections.


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    """Removes a specific movie from a user’s favorite movie list."""
    user = db.session.get(User, user_id)
    if user:
        movies = data_manager.get_movies(user_id)
        for movie in movies:
            if movie.id == movie_id:

                data_manager.delete_movie(movie_id)
                return redirect(
                    url_for(
                        "list_movies",
                        user_id=user_id,
                        message="Movie deleted successfully.",
                    )
                )


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()

    app.run(debug=True)
