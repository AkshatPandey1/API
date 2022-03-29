import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


class Spotify:
    def __init__(self, clientID, clientSecret):
        self.SPOTIPY_CLIENT_ID = clientID

        self.SPOTIPY_CLIENT_SECRET = clientSecret
        self.SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback'

    def getRecently_played(self):
        sp_recently_played = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                                                                       client_secret=self.SPOTIPY_CLIENT_SECRET,
                                                                       redirect_uri=self.SPOTIPY_REDIRECT_URI,
                                                                       scope='user-read-recently-played'))
        results = sp_recently_played.current_user_recently_played(50)["items"]
        return results

    def getPlaylist(self):
        sp_playlist = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                                                                client_secret=self.SPOTIPY_CLIENT_SECRET,
                                                                redirect_uri=self.SPOTIPY_REDIRECT_URI,
                                                                scope='playlist-read-private'))
        results = sp_playlist.current_user_playlists(50)["items"]
        return results

    def getFollows(self):
        sp_follows = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                                                               client_secret=self.SPOTIPY_CLIENT_SECRET,
                                                               redirect_uri=self.SPOTIPY_REDIRECT_URI,
                                                               scope='user-follow-read'))
        results = sp_follows.current_user_followed_artists(50)["artists"]["items"]
        return results

    def getTop(self):
        sp_top = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                                                           client_secret=self.SPOTIPY_CLIENT_SECRET,
                                                           redirect_uri=self.SPOTIPY_REDIRECT_URI,
                                                           scope='user-top-read'))
        results = sp_top.current_user_top_tracks(50)["items"]
        return results


AP = Spotify(os.getenv('SPT_CID'), os.getenv('SPT_CSR'))

print(AP.getRecently_played())
print(AP.getFollows())
print(AP.getTop())
print(AP.getPlaylist())
