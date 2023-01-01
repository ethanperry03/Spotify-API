
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import cred
import requests
import base64
import const

'''
Summary: encodes credentials and gets the token used for requesting
Pre: clientID and secretID are read in which are accesed from the credentials file attached to main
Post: user token is returned and will be used for other requests
'''
def getToken(client, secret):

    # Step 1 - Authorization
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    # Encode as Base64
    message = f"{cred.client_id}:{cred.client_secret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']

    return token


scope = "playlist-modify-public"
sp_modify_pub = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                               redirect_uri=cred.redirect_url, scope=scope))

sp_modify_priv = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                                   redirect_uri=cred.redirect_url, scope="playlist-modify-private"))

scope_playlist = "playlist-modify-public"
playlist_build = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                                           redirect_uri=cred.redirect_url, scope=scope_playlist))



sp_read_pub = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                                     redirect_uri=cred.redirect_url, scope="playlist-read-collaborative"))


sp_read_priv = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                                      redirect_uri=cred.redirect_url, scope="playlist-read-private"))


