# youtube_to_spotify_playlist
Takes in a youtube playlist and adds a spotify playlist with best guess matches for the songs, using the power of Python!

The libraries used were:
  requests
  BeautifulSoup
  spotipy
  re
  json
  requests_html

All of them can be added with pip. I used python 3.8.10, not sure if it will work with other versions.

The project bascially scrapes the youtube playlist data directly from HTML, then searches spotify for each song, and then generates a new playlist for the user consisting of best guesses for each song in the original playlist.

