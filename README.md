# Spotify Project

I created this project to get experience working with an API and parsing data for the first time. Users can search for an album and this app uses the Spotify API to retrieve/calculate stats that users can't normally see on Spotify. This app also generates recommendations for the user based on the album's genres and artist, and includes links to the recommended songs and their artists. 

## Screenshots

### Homepage
<img width="1440" alt="Screen Shot 2023-03-22 at 4 39 32 PM" src="https://user-images.githubusercontent.com/101783138/227065526-d20b4886-62ed-405d-84c6-39a414e4a9f7.png">

### Search Results
![Screen Shot 2023-03-22 at 4 41 30 PM](https://user-images.githubusercontent.com/101783138/227065564-b02bcd80-b95e-4ed9-8a5d-1bccbf8aba98.png)
![Screen Shot 2023-03-22 at 4 48 51 PM](https://user-images.githubusercontent.com/101783138/227065566-69101b86-6fc8-4219-a76c-48c9c609dccf.png)

### Tech Stack
- Front end: HTML, CSS, Jinja
- Back end: Python,Spotify API, Flask, JSON

### Setup/Installation

Create and enter virtual environment:
```sh
> virtualenv env
> source env/bin/activate
```

Install requirements:
```sh
> pip3 install -r requirements.txt
```

Run server.py:
```sh
> python3 server.py
```
