from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Representing a User.

    Attributes:
        id (int): Primary key.
        name (str): User’s name.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
    """Representing a movie.

    Attributes:
        id (int): Primary key.
        name (str): Movie’s name.
        director (str): Movie’s director.
        year (int): Year of release.
        poster_url (str): URL of the movie's poster.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String, nullable=False)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
