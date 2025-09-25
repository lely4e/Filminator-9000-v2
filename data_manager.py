from models import db, User, Movie
from sqlalchemy import exc


class DataManager:
    # Define Crud operations as methods
    def create_user(self, name):
        # Creates a User
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        # Return a list of all users in your database.
        return db.session.query(User).all()

    def get_movies(self, user_id):
        # Return a list of all movies of a specific user.
        return db.session.query(Movie).filter_by(Movie.name == user_id).all()

    def add_movie(self, movie):
        # Add a new movie to a user’s favorites. The process is similar
        # to adding a new user.
        add_movie = Movie(name=movie)
        movie_in_database = (
            db.session.query(Movie).filter_by(Movie.name == movie).first()
        )
        if not movie_in_database:
            try:
                db.session.add(add_movie)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                print("Movie already exists in database")

    def update_movie(self, movie_id, new_title):
        # Update the details of a specific movie in the database.
        movie = db.session.get(Movie, movie_id)
        if movie:
            try:
                movie.name = new_title
                db.session.commit()
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                print("Movie doesn't exist in database")

    def delete_movie(self, movie_id):
        # Delete the movie from the user’s list of favorites.
        movie = db.session.get(Movie, movie_id)
        if movie:
            try:
                db.session.delete(movie)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                print("Cannot delete the movie")
