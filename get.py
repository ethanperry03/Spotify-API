
import cred
import tokenSP
import requests

'''
Summary: automates a song search query to get ID information of a given song
Pre: Strings of the song, artist, and album
Post: Returns the track, album, and artist ID's
'''
def getID(trackname, albumname, artistname, justTrackID):

    # accessing dictionary info with keys, print out json to trace (pretty simple)

    trackID = tokenSP.sp_modify_pub.search(q=artistname + ' ' + trackname + ' ' + albumname, type='track')

    if justTrackID:
        return trackID['tracks']['items'][0]['id']

    else:

        albumID = tokenSP.sp_modify_pub.search(q=artistname + " " + trackname + ' ' + albumname, type='album')

        artistID = trackID['tracks']['items'][0]['album']['artists'][0]['id']

        trackID = trackID['tracks']['items'][0]['id']

        albumID = albumID['albums']['items'][0]['id']

        return trackID, albumID, artistID


'''
Summary: function takes in a song ID and returns its attributes in a dictionary
Pre: id to create request with the song ID as well as the token
Post: returns dictionary of attributes
'''
def getAttributes(trackid):

    # Get token for request
    token = tokenSP.getToken(client=cred.client_id, secret=cred.client_secret)

    # create query url amd defined header from spotify API for request.get
    query = f'https://api.spotify.com/v1/audio-features/{trackid}'
    headers = {"Content-type": "application/json", "Authorization": "Bearer " + token}

    # get the response and use json to formulate it into dict
    response = requests.get(url=query, headers=headers)
    songAttributes = response.json()

    return songAttributes


'''
Summary: Input seed search to get artists genres
'''
def get_artists_genres(string_search):

    trackID = tokenSP.sp_modify_pub.search(q=string_search[1] + ' ' + string_search[0] + ' ' + string_search[2],
                                           type='track')

    artistID = trackID['tracks']['items'][0]['album']['artists'][0]['id']

    artistinfo = tokenSP.sp_modify_pub.artist(f'spotify:artist:{artistID}')
    genres = artistinfo['genres']

    return genres

