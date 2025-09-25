from models import db, User, Movie


class DataManager:
    # Define Crud operations as methods
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        # Return a list of all users in your database.
        pass

    def get_movies(self, user_id):
        # Return a list of all movies of a specific user.
        pass

    def add_movie(self, movie):
        # Add a new movie to a user’s favorites. The process is similar to adding a new user.
        pass

    def update_movie(self, movie_id, new_title):
        # Update the details of a specific movie in the database.
        pass

    def delete_movie(self, movie_id):
        # Delete the movie from the user’s list of favorites.
        pass
