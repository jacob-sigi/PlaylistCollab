'''
Jacob Sigismonti
r/PlaylistCollab
Reddit CollabBot

MAKE SURE THE REDDIT POST IS A LINK POST
'''

import praw
import time
import config
import re
import spotifyxx

SUBREDDIT = "playlistcollab"

class CollabBot:

    def __init__(self):
        self.reddit = self._login()

    #login using credentials stored in "config.py"
    def _login(self) -> praw.Reddit:
        print("Logging in...")
        r = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = "CollabBot")
        print("Login Successful!")
        return r

    #extract url from submission class
    def _get_link_from_post(self,submission) -> str:
        return submission.url

    #checks if url is a valid spotify url
    def is_playlist_url(self,playlist_url:str) -> bool:
        regex = r'https://open\.spotify\.com/user/.+/playlist/([a-zA-Z0-9]+)\?'
        return re.match(regex,playlist_url) != None

    #get the id of from the shareable spotify playlist link
    def _get_playlist_id_from_url(self,url:str) -> str:
        regex = r'https://open\.spotify\.com/user/.+/playlist/([a-zA-Z0-9]+)\?'
        if self.is_playlist_url(url):
            #match regex
            playlist_id = re.match(regex,url)
            #extract the playlist id from matched text
            playlist_id = playlist_id.group(1)
            return playlist_id
        else:
            print("Not a valid playlist url!")
            return None

    #Checks to see if a comment is a command
    #A command is in the form of: "add: Artist - Song"
    def _comment_is_command(self,comment_body:str) -> bool:
        regex = r"[aA]dd:\s*(.+)\s*-\s*(.+)"
        match = re.match(regex,comment_body)
        return match != None


    def _get_artist_and_title(self,command:str) -> dict:
        regex = r"[aA]dd:\s*(.+)\s*-\s*(.+)"
        match = re.match(regex,command)
        return {'artist':match.group(1), 'song':match.group(2)}

    def run(self,subreddit:str) -> None:
        #for every post in new
        for com in self.reddit.subreddit(subreddit).stream.comments(skip_existing=True): #skip_existing=True
            #get the playlist link from post
            link = self._get_link_from_post(com.submission)
            #get playlist id from link
            playlist_id = self._get_playlist_id_from_url(link)
            #if it's a valid id then loop through comments
            if playlist_id != None:
                #initialize spotify object
                sp = spotifyxx.create_spotify_object()

                if self._comment_is_command(com.body):
                    #extract artist and song info
                    d = self._get_artist_and_title(com.body)
                    #search for song and get song id
                    track_id = spotifyxx.search_track(sp,d['artist'],d['song'])

                    if(track_id != None):
                    #add song to playlist
                        spotifyxx.add_track(sp,playlist_id,[track_id])
                        print("track added!")
                        com.reply("track added!")
                    else:
                        print("couldn't find track: {}".format(d['song']))
                        com.reply("sorry! I couldn't find that track!")
            else:
                print("not a valid playlist id")

if __name__ == '__main__':
    bot = CollabBot()
    bot.run(SUBREDDIT)
