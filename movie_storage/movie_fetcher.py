import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def fetch_movie(title):
    """
    Fetches movie data from the API.
    """
    api_url = "http://www.omdbapi.com/?t={}&apikey={}".format(title, API_KEY)
    response = requests.get(api_url)
    data = response.json()
    if data.get("Response") == "True":
        return (data["Title"], data["Writer"], data["Year"], data["Poster"])
        # return data
    return None


# print(fetch_movie("Titanic"))
