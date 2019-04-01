import os
import pprint
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecoder

#Usage:

# get the username from terminal: python3 spotifyxx.py [user_id]
USERNAME = "1298941730"#sys.argv[1]
scope = 'playlist-modify-public playlist-modify-private'
# User ID: https://open.spotify.com/user/1298941730?si=vOrjogu3SNuos5-5GwXSng

client_id = 'c0b205b67cc8486c85f3c6e4c88f474c'
client_secret = '8ca6021b832444a2ad94a7e885e1a651'
redirect = 'https://google.com/'

# Create spotifyObject
def create_spotify_object():
# Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(USERNAME,scope,client_id,client_secret,redirect)
    except:
        os.remove(".cache-{}".format(USERNAME))
        token = util.prompt_for_user_token(USERNAME,scope,client_id,client_secret,redirect)

    # Create our spotifyObject
    #client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    #client_credentials_manager=client_credentials_manager
    spotifyObject = spotipy.Spotify(auth=token)
    spotifyObject.trace = False
    return spotifyObject

def create_playlist(sp,playlist_name) -> str:
    sp.user_playlist_create(USERNAME,playlist_name)

    playlist = sp.user_playlists(USERNAME,limit=50)
    id = ''
    for p in playlist['items']:
        if(p['name'] == playlist_name):
            id = p['id']
    return id

#search for song and return the id if song is found
def search_track(sp,artist,song) -> str:
    query = sp.search('track:{0} AND artist:{1}'.format(song,artist),limit=10,type='track')
    #check if any tracks were foundd
    if(query['tracks']['total'] != 0):
        #get the top results id
        track_id = query['tracks']['items'][0]['id']
        return track_id
    return None

def add_track(sp, playlist_id, track_id_list):
    sp.user_playlist_add_tracks(USERNAME, playlist_id,track_id_list)
    return

#search(q, limit=10, offset=0, type='track', market=None)
'''if __name__ == '__main__':
    sp = start_program()
    test = sp.search('track:"like what" AND artist:"tennyson"',limit=10,type='track')
    #If total num of tracks returned is 0, print error
    if(test['tracks']['total'] == 0):
        print("No track found!")
    #pprint.pprint(test)
    else:
        #get the id of the first track found
        song_id = test['tracks']['items'][0]['id']
        #add track to playlist
        #add_track(sp,create_playlist(sp,'testing'),[song_id])
        add_track(sp,"5YIPMIptAAEcXVMw4JvkaZ",[song_id])
'''
