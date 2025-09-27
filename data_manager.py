from errors.custom_errors import (
    MovieInDatabaseError,
    NoMovieInApiError,
    MovieNotInDatabaseError,
    FailedQueryError,
)
from models import db, User, Movie
from sqlalchemy import exc, and_
from movie_storage.movie_fetcher import fetch_movie


class DataManager:
    # Crud operations as methods
    def create_user(self, name):
        """Creates a User."""
        new_user = User(name=name)
        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise FailedQueryError("Could not add the user")

    def get_users(self):
        """Return a list of all users in your database."""
        return db.session.query(User).all()

    def get_movies(self, user_id):
        """Return a list of all movies of a specific user."""
        return db.session.query(Movie).filter(Movie.user_id == user_id).all()

    def add_movie(self, user_id, title):
        """Add a new movie to a user’s favorites."""
        # Check if movie title exist in API
        movie_in_API = fetch_movie(title)
        if movie_in_API:
            # Check if movie in database
            name, director, year, poster_url = movie_in_API
            movie_in_database = (
                db.session.query(Movie)
                .filter(and_(Movie.name == name, Movie.user_id == user_id))
                .first()
            )

            if not movie_in_database:
                add_movie = Movie(
                    name=name,
                    director=director,
                    year=year,
                    poster_url=poster_url,
                    user_id=user_id,
                )

                try:
                    db.session.add(add_movie)
                    db.session.commit()
                except exc.SQLAlchemyError:
                    db.session.rollback()
                    raise FailedQueryError("Could not add the movie")
            else:
                raise MovieInDatabaseError("Movie is already in database!")
        else:
            raise NoMovieInApiError("Movie doesn't exist in API")

        return self.get_movies(user_id)

    def update_movie(self, movie_id, new_title):
        """Update the details of a specific movie in the database."""
        movie = db.session.get(Movie, movie_id)
        if movie:
            try:
                movie.name = new_title
                db.session.commit()
            except exc.SQLAlchemyError:
                db.session.rollback()
                raise FailedQueryError("Could not update the movie")
        else:
            raise MovieNotInDatabaseError("Movie doesn't exist in database")

    def delete_movie(self, movie_id):
        """Delete the movie from the user’s list of favorites."""
        movie = db.session.get(Movie, movie_id)
        if movie:
            try:
                db.session.delete(movie)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                raise FailedQueryError("Could not delete the movie")
        else:
            raise MovieNotInDatabaseError("Movie doesn't exist in database")
