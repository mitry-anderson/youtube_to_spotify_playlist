import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import json
from requests_html import HTMLSession


# global variables to set (could get from user input if desired)
URL = "https://www.youtube.com/playlist?list=PL8nO15pqbkPuAraU0QhEaPtBVxeE2rTFw" 
playlistName = "Elias Jazz"
playlistDescription = "Converted from youtube playlist: " + URL


class playlistItem:
    def __init__(self, title, channel):
        self.title = title
        self.channel = channel


def getTrackID(title,author):

    if(title != '' and author != ''):
        title = re.sub('\n','',title)
        title = title.lower()

        author = re.sub('\n','',author)
        author = author.lower()

        q = title
        lim = 10
        track = sp.search(q, limit=lim, type='track')
        # formatted = json.dumps(track, indent=4)
        # print(formatted)

        titleWords = title.split(' ')
        authorWords = author.split(' ') + titleWords

        bestScore = 0
        bestID = ''
        for i in range(len(track["tracks"]["items"])):
            name = track["tracks"]["items"][i]["name"]
            artist = track["tracks"]["items"][i]["artists"][0]["name"]
            id = track["tracks"]["items"][i]["id"]
            trackMatchPercent = 0
            artistMatchPercent = 0
            artist = artist.lower()
            name = name.lower()

            for word in titleWords:
                if name.find(word) != -1:
                    trackMatchPercent += 1/len(titleWords)
            for word in authorWords:
                if artist.find(word) != -1:
                    artistMatchPercent += 1/len(authorWords)
            score = artistMatchPercent + trackMatchPercent
            
            if(score > bestScore):
                bestScore = score
                bestID = id
        
        return bestID
    return ''




session = HTMLSession()
r = session.get(URL)
r.html.render()
page = r.html.html

# file = open("website.html",'w')
# file.write(page)
# file.close()

soup = BeautifulSoup(page,"html.parser")

tags = soup.find_all('div',class_='ytd-playlist-video-renderer')
links = []
data = {}
for tag in tags:
    item = tag.find_all('a')
    title = ''
    author = ''
    for link in item:
        
        if(link!=None):
            if link.get('class')[2] == "yt-formatted-string":
                author = link.contents[0]
            elif link.get('title') != None:
                title = link.contents[0]

    data.update({title:author})

#print(data)

SPOTIPY_CLIENT_ID="934e5f9af47c45b4b812fa81999c8413"
SPOTIPY_CLIENT_SECRET="d60d7b2f8a094cd8b7f14e4fd174af51"
SPOTIPY_REDIRECT_URI='https://www.spotify.com'

scope = ["user-library-read","playlist-modify-private","playlist-modify-public"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI))

results = sp.current_user_playlists()
#print(results)

user = sp.current_user()['display_name']
print(user)
playlist = sp.user_playlist_create(user, playlistName, public=True, description=playlistDescription)
playlistID = playlist["id"]
#print(playlistID)

tracks = []

for song in data:
    print("------------")
    print("Searching for Youtube Song:")
    print(song + "  by: " + data[song])
    trackID = getTrackID(song,data[song])
    
    if(trackID != ''):
        tracks.append(trackID)
        print("Found Spotify Song:")
        print(sp.track(trackID)['name'] + "  by: " + sp.track(trackID)["artists"][0]["name"])


sp.user_playlist_add_tracks(user,playlistID,tracks)



    















