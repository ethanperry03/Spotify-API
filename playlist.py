
import requests
import const
import get
import cred
import tokenSP
import file


'''
Summary: Takes a playlist by URL constant and returns data about it given justID bool param
Pre: PlaylistURl and bool specifying if the user just wants ID's or all dict data
Post: Data dict or ID list
'''
def playlistSongs(playlistURL, justTrackID, privacy):

    # reads in the share link for a playlist URL to convert to URI
    playURI = playlistURL.split('/')[-1].split('?')[0]

    # get response of playlist items from URI call with splay object depending on privacy level
    if privacy == const.PUBLIC:
        res = tokenSP.sp_read_pub.playlist_items(playURI)
    else:
        res = tokenSP.sp_read_priv.playlist_items(playURI)

# ============================== if statement for justTrackIDs =================================

    # loop to append all ID's (saves time to just get ID's rather than create dict first)
    if justTrackID:

        # initliaze empty list
        playlistIDs = []

        # loop through response dict to just pull ID's
        for i, j in enumerate(res['items']):
            playlistIDs.append(j['track']['id'])

        # return IDs
        return playlistIDs

# ================================ else statement to create dict ====================================

    else:

        # initialize master playlist data dict
        playlistData = {}

        # loop through items such that i is the index and j is the key
        for i, j in enumerate(res['items']):

        # =========================== temp dict creation =========================================
            # start the temp song data dict to store the ith songs information
            songData = {
                        'track_name': j['track']['name'],                       # track name
                        'track_id': j['track']['id'],                           # track id
                        'track_pop': j['track']["popularity"],                  # track pop
                        'album_name': j['track']['album']['name'],              # album name
                        'album_id': j['track']['album']['id'],                  # album ID
                        'album_release': j['track']['album']['release_date'],   # album release
                        'album_length': j['track']['album']['total_tracks']     # album length
                        }

        # ---------------------- explicit -------------------
            if j['track']['explicit']:
                songData['track_exp'] = 'explicit'
            else:
                songData['track_exp'] = 'clean'

        # ================================= artist info wiser ================================

            tempnames = ""
            tempIDs = ""
            tempgenres = ""

            for k in range(len(j['track']['artists'])):
                # artist name
                tempnames = f"{tempnames}, {j['track']['artists'][k]['name']}"

                # artist ID
                tempIDs = f"{tempIDs}, {j['track']['artists'][k]['id']}"

                artistinfo = tokenSP.sp_modify_pub.artist(j['track']['artists'][k]['uri'])
                artistGenres = artistinfo['genres']

                for item in artistGenres:
                    if item not in tempgenres:
                        tempgenres = f"{tempgenres}, {item}"

            songData['artist_names'] = tempnames[2::]
            songData['artist_ids'] = tempIDs[2::]
            songData['artists_genres'] = tempgenres[2::]


    # ================================== getting track attributes ====================================

            attributes = get.getAttributes(songData['track_id'])

            names = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                     'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

            for name in names:  # adding attributes to unordered dict
                songData[name] = attributes[name]

        # =============== ordering the dict =================================================

            dictOrdering = ['track_name', 'track_id', 'acousticness', 'danceability', 'duration_ms', 'energy',
                            'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo',
                            'time_signature', 'track_exp', 'track_pop', 'valence', 'artist_names', 'artist_ids',
                            'artists_genres', 'album_name', 'album_id', 'album_release', 'album_length']

            songData = {k: songData[k] for k in dictOrdering}

        # ------------------ key the ith dictionary entry with track name -------------------

            playlistData['playlist_track_' + str(i + 1)] = songData

        return playlistData


'''
Summary: adds songs to a specified playlist 
PRE: list of track ID's that are to be added to playlsit
POST: songs are added and playlsit is updated
note: playlist_build spotify object is defined in tokenSP for playlist updating
'''
def playlist_adder(listIDs, playlistURL, privacy):

    # reads in the share link for a playlist URL to convert to URI
    playlistURI = playlistURL.split('/')[-1].split('?')[0]

    # initiliaze track uri's in the playlist
    uriList = []

    if privacy == const.PUBLIC:

        if len(listIDs) < 100:

            # create uri's from id's
            for i in range(len(listIDs)):
                uriList.append(f"spotify:track:{listIDs[i]}")

            # add items to specified playlist
            tokenSP.sp_modify_pub.playlist_add_items(playlist_id=playlistURI, items=uriList)

        else:

            counter = 0     # initliaze it to 0 to begin loop

            # start while loop
            while counter < len(listIDs):

                # get uri list
                uriList.append(f"spotify:track:{listIDs[counter]}")

                strcount = str(counter)[::-1]

                if strcount[0:2] == '99':

                    # add items to playlist
                    tokenSP.sp_modify_pub.playlist_add_items(playlist_id=playlistURI, items=uriList)

                    # empty this list
                    uriList = []

                # update counter
                counter += 1

            # add remaining stuff
            tokenSP.sp_modify_pub.playlist_add_items(playlist_id=playlistURI, items=uriList)

    # ========================== private =================================

    else:

        if len(listIDs) < 100:

            # create uri's from id's
            for i in range(len(listIDs)):
                uriList.append(f"spotify:track:{listIDs[i]}")

            # add items to specified playlist
            tokenSP.sp_modify_priv.playlist_add_items(playlist_id=playlistURI, items=uriList)

        else:

            counter = 0  # initliaze it to 0 to begin loop

            # start while loop
            while counter < len(listIDs):

                # get uri list
                uriList.append(f"spotify:track:{listIDs[counter]}")

                strcount = str(counter)[::-1]

                if strcount[0:2] == '99':
                    # add items to playlist
                    tokenSP.sp_modify_priv.playlist_add_items(playlist_id=playlistURI, items=uriList)

                    # empty this list
                    uriList = []

                # update counter
                counter += 1

            # add remaining stuff
            tokenSP.sp_modify_priv.playlist_add_items(playlist_id=playlistURI, items=uriList)

    return 0


'''
Sumamry: With the list of IDs wishing to be formulated, the name and privacy level of the new
         playlist are used to create it and add the songs to the correct users account.
PRE: id list, playlist name, and privacy level desired for the new playlist
POST: a created playlist is generated with the songs added and the ID is returned
'''
def playlist_creation(reclist_ids, playlist_name, privacy):

    # create token for request
    token = tokenSP.getToken(client=cred.client_id, secret=cred.client_secret)

    # creates a playlist to the user of API with playlist name given the privacy boolean
    if privacy == const.PUBLIC:
        tokenSP.sp_modify_pub.user_playlist_create(const.username, playlist_name, public=True)
    else:
        tokenSP.sp_modify_priv.user_playlist_create(const.username, playlist_name, public=False)

    # create necessary request features for get
    preurl = f"https://api.spotify.com/v1/users/{const.username}/playlists"
    header = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + token}

    # playlistres stores the response to the playlist creation
    playlistres = requests.get(url=preurl, headers=header)
    playlistres = playlistres.json()

    # pull the ID of the new playlist for add method
    createdID = playlistres['items'][0]['id']

    if privacy == const.PUBLIC:
        # add songs using sp object and add tracks method
        playlist_adder(listIDs=reclist_ids, playlistURL=f'/{createdID}?', privacy=const.PUBLIC)
    else:
        playlist_adder(listIDs=reclist_ids, playlistURL=f'/{createdID}?', privacy=const.PRIVATE)

    # returns the ID of new playlist for future reference
    return createdID


'''
Summary: creates a playlist from seed style track info input file
PRE: input matrix of strings to query, name of playlist to create, privacy level of creation
POST: returns playlist_id of the one created from the call
'''
def list_to_playlist(inputmatrix, playlist_name, privacy):

    # initialize to store the track ID's returned from the query
    outputID = []

    for item in inputmatrix:
        outputID.append(get.getID(item[0], item[1], item[2], True))

    # pass the collected track ID's and create a playlist using the creation method
    playlist_id = playlist_creation(outputID, playlist_name=playlist_name, privacy=privacy)

    # return created ID
    return playlist_id


def trackID_to_playlist(trackIDs, playlist_name, privacy):

    playlist_id = playlist_creation(reclist_ids=trackIDs, playlist_name=playlist_name, privacy=privacy)

    return playlist_id


'''
Summary: playlist URL passes in and returns the string query info for each song (used for ranking)
PRE: playlist URL
POST: 
'''
def playlist_to_list(playlistURL, privacy):

    # reads in the share link for a playlist URL to convert to URI
    playlistURI = playlistURL.split('/')[-1].split('?')[0]

    # get all the track ID's in the entered plalist using playlistSongs method
    trackIDs = playlistSongs(playlistURI, justTrackID=True, privacy=privacy)

    # initiliaze output matrix
    matrix = []

    for i in range(len(trackIDs)):

        # initialize a temp list to store the string names for each song
        temp = []

        # use sp method to get track info from ID
        track = tokenSP.sp_modify_pub.track(trackIDs[i], market='US')

        # store the string information
        trackname = track['name']
        albumname = track['album']['name']
        artistname = track['album']['artists'][0]['name']

        # append all to temp and then temp to master
        temp.extend([trackname, artistname, albumname])
        matrix.append(temp)

    # return matrix to use in ranking
    return matrix



def list_to_dict(inputmatrix, playlist_name, outfile, privacy):

    # get track IDs from input string list
    outputID = []
    for item in inputmatrix:
        outputID.append(get.getID(item[0], item[1], item[2], True))

    # creates a playlist with those songs
    playlistID = playlist_creation(outputID, playlist_name=playlist_name, privacy=privacy)

    # gets a dictionary output
    dict = playlistSongs(playlistID, justTrackID=False, privacy=privacy)

    for i, j in enumerate(dict):
        dict[j]["rank"] = inputmatrix[i][3]

    file.outputTSV(dict, outfile=outfile, rank=True)

    return dict