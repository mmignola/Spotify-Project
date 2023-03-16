from flask import Flask, render_template, request
from dotenv import load_dotenv
from jinja2 import StrictUndefined
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# -------------------------------------------------- ROUTES --------------------------------------------------
@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/results", methods = ["POST"])
def search_results():
    """View search results."""

    token = get_token()
    search_term = request.form.get("search_term")
    album = search_for_album(token, search_term)
    artist_id = album["artists"][0]["id"]
    album_id = album["id"]
    genres = format_genres(get_artist_from_id(token, artist_id)["genres"])
    popularity = get_album_from_id(token, album_id)["popularity"]
    album_tracks = get_album_tracks_from_id(token, album_id)
    danceability = avg_danceability(album_tracks)
    energy = avg_energy(album_tracks)
    recommendations = get_recommendations(token, artist_id, genres)["tracks"]
    release_date = format_date(album["release_date"])
    cover_art = album["images"][1]["url"]

    return render_template("results.html", 
                           album = album, 
                           genres = genres, 
                           popularity = popularity,
                           danceability = danceability,
                           energy = energy,
                           recommendations = recommendations,
                           release_date = release_date,
                           cover_art = cover_art)


# -------------------------------------------------- FUNCTIONS --------------------------------------------------
def get_token():
    """Create authorization token."""
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_album(token, album_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={album_name}&type=album&limit=1"

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["albums"]["items"]
    
    if len(json_result) == 0:
        return None
    
    return json_result[0]


def get_album_tracks_from_id(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_results = json.loads(result.content)["items"]

    return json_results


def get_album_from_id(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_results = json.loads(result.content)

    return json_results


def get_artist_from_id(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_results = json.loads(result.content)

    return json_results


def get_track_from_id(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_results = json.loads(result.content)

    return json_results


def get_recommendations(token, artist_id, genres):
    url = f"https://api.spotify.com/v1/recommendations?limit=5&seed_artists={artist_id}&seed_genres={genres}&max_popularity=50"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_results = json.loads(result.content)

    return json_results


def avg_energy(tracks):
    """Calculates avg score across all tracks."""
    vals = []

    for track in tracks:
        track_info = get_track_from_id(get_token(), track["id"])
        vals.append(track_info["energy"])

    avg = sum(vals) / len(vals)

    return round(avg * 100)


def avg_danceability(tracks):
    """Calculates avg score across all tracks."""
    vals = []

    for track in tracks:
        track_info = get_track_from_id(get_token(), track["id"])
        vals.append(track_info["danceability"])

    avg = sum(vals) / len(vals)

    return round(avg * 100)


def format_date(date):
    """Reformats date pulled from data."""
    split_date = date.split("-")
    new = []
    for item in split_date:
        new.append(item.lstrip("0"))
    year = new.pop(0)
    new.append(year)
    reordered_date = "/".join(new)

    return reordered_date


def format_genres(genres):
    """Reformats genres from list into tidy string."""
    new = []
    for genre in genres:
        new.append(genre.capitalize())
    final_string = ", ".join(new)

    return final_string


# -------------------------------------------------- TESTING/PRINTING --------------------------------------------------
# album = search_for_album(get_token(), "bronco")
# album_name = album["name"]
# artist_id = album["artists"][0]["id"]
# artist_name = album["artists"][0]["name"]
# artist_genres = get_artist_from_id(get_token(), artist_id)["genres"]
# album_id = album["id"]
# album_release = album["release_date"]
# album_popularity = get_album_from_id(get_token(), album_id)["popularity"]
# album_genres = get_album_from_id(get_token(), album_id)["genres"] #albums always come up with an empty genre list ig?
# album_tracks = get_album_tracks_from_id(get_token(), album_id)
# cover = album["images"][1]["url"]

# recommendation = get_recommendations(get_token(), artist_id, artist_genres)["tracks"][0]
# artist_page = recommendation["artists"][0]["external_urls"]["spotify"]
# track_page = recommendation["external_urls"]["spotify"]
# track_name = recommendation["name"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)