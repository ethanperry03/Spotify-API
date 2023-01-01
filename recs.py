
import requests
import const
import get
import file
import cred
import tokenSP


'''
Summary: this function generates tailored recs based off seed info
Input: Album and Track ID's, limit of n recs, bool to just get rec ID's
POST: Either a dictionary of the rec attributes or Track ID's of the recs
'''
def getRecs(trackID, artistID, limit, genres, justID):

    # generate an access token to use the spotify object created in tokenSP
    token = tokenSP.getToken(client=cred.client_id, secret=cred.client_secret)

# ===============================================================================

    # define the url that will be used in the request
    rec_url = "https://api.spotify.com/v1/recommendations?"

    # this is the header for the request
    headers = {"Content-type": "application/json", "Authorization": "Bearer " + token}

    # this is the updated query request URL
    query = f'{rec_url}limit={limit}&market={const.market}&seed_genres={genres}&seed_artist={artistID}&seed_tracks={trackID}'

    # the response to this get is sorted using json and then information will be pulled after`
    res = requests.get(url=query, headers=headers)
    res = res.json()

# =================================== rec analysis  and sorting ================================

    # if just ID's are returned it'll break here instead of creating the entire dict
    if justID:
        # ID list initialization for return statement
        justIDlist = []
        # enumerating the objects in the class for more streamlined access to items
        for i, j in enumerate(res['tracks']):
            # append the ID's
            justIDlist.append(j['id'])
        # return the list of ID's
        return justIDlist

    # launch into the else statement for normal function
    else:
        # initialize empty dict that will collect every recommended songs attributes
        recData = {}

        # for each item in the json, let the iteration be i and the key of it be j
        for i, j in enumerate(res['tracks']):

            # this is the temp dictionary for  each for loop that will store the ith songs data
            songData = {}

    # ========================== track info =============================================

            songData['track_name'] = j['name']          # track name
            songData['track_id'] = j['id']              # track id
            songData['track_pop'] = j["popularity"]     # track popularity

            if j['explicit']:
                songData['track_exp'] = 'explicit'      # if track is explicit
            else:
                songData['track_exp'] = 'clean'         # else it is clean

    # ======================= album info ================================================

            songData['album_name'] = j['album']['name']               # album name
            songData['album_id']= j['album']['id']                    # album ID
            songData['album_release'] = j['album']['release_date']    # albums release date
            songData['album_length'] = j['album']['total_tracks']     # track length

    # ======================= artists info ==============================================

            # initlaizing the strings that will return artists info
            tempnames = ""
            tempIDs = ""
            tempgenres = ""

            # each artist credited in the song (Kth artist)
            for k in range(len(j['artists'])):
                # artist name
                tempnames = f"{tempnames}, {j['artists'][k]['name']}"

                # artist ID
                tempIDs = f"{tempIDs}, {j['artists'][k]['id']}"

                # artists genres
                artistinfo = tokenSP.sp_modify_pub.artist(j['artists'][k]['uri'])
                artistGenres = artistinfo['genres']

                # ensuring no repeats (note most of these are sub-genres and not GENRES)
                for item in artistGenres:
                    if item not in tempgenres:
                        tempgenres = f"{tempgenres}, {item}"

            # trimming the comma off the front
            songData['artist_names'] = tempnames[2::]
            songData['artist_ids'] = tempIDs[2::]
            songData['artists_genres'] = tempgenres[2::]

    # ============================== getting track attributes ===================================

            # calls the get attributes function
            attributes = get.getAttributes(songData['track_id'])

            # names of all of the attributes
            names = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                     'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

            for name in names:   # adding attributes to unordered dict
                songData[name] = attributes[name]

    # ============================= ordering the dict =================================================

            dictOrdering = ['track_name', 'track_id', 'acousticness', 'danceability', 'duration_ms', 'energy',
                            'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo',
                            'time_signature', 'track_exp', 'track_pop', 'valence', 'artist_names', 'artist_ids',
                            'artists_genres', 'album_name', 'album_id', 'album_release', 'album_length']

    # ========================== append to master dictionary ==========================================

            # ordering the songs based on the desired order
            songData = {j: songData[j] for j in dictOrdering}

            # creating an index key for each songData being added to recData
            recData['rec_track_' + str(i+1)] = songData

# ==================== end of loop, return master dict =================================

        return recData


'''
Summary: Passes in seeds and parameters to generate rec trackID's
PRE: Gets a matrix of seed songs by ID (track, album, artist), generation limit, 
     and the genre / sub-genres (of the artist) that is valid to pass into the request function
POST: Returns a list of the trackID's it recommends
'''
def rec_builder(matrix, limit, genre):

    # initialize empty builder lists
    rec_list_ids = []
    temp_list = []

    # loop through the input matrix
    for item in matrix:

        # get recs tracks from the ith seed in the matrix (limit amount)
        list_track_ids = getRecs(trackID=item[0], artistID=item[2], limit=limit, genres=genre, justID=True)

        # append rec ID to temp list
        temp_list.append(list_track_ids)

    # iterate through matrix to create a single list of ID's to return
    for i in range(len(temp_list)):
        for k in range(len(temp_list[i])):
            rec_list_ids.append(temp_list[i][k])

    return rec_list_ids


'''
Summary: This creates a more nuanced rec list by cross comparing a couple of lists and aims
         to find extra overlap to make the recs more accurate
PRE: Input is the string input one would search on the app to find the song as well as
     the limit of recs that will be produced by each list and target playlist length
POST: A list of rec trackID's will be returned to be analyzed and placed in playlists
'''
def rec_optimization(seedList, limit, length):

    # initialized lists
    convertedSeeds = []       # used to convert string seeds to their matching ID's
    masterList = []           # final list of the optimized recommendations
    gen = []                  # all genres and sub genres of the artists

    # loops through the seeds
    for i in range(len(seedList)):

        temp = []           # temp list initialized

        # convert strings to ID's using getID function call
        track, album, artist = get.getID(seedList[i][0], seedList[i][1], seedList[i][2], justTrackID=False)

        # add these ID's to the temp list
        temp.extend([track, album, artist])

        # append to converted seeds matrix
        convertedSeeds.append(temp)

        # get the genres of the given artist by ID
        genres = tokenSP.sp_modify_pub.artist(artist)

        # loop through and weed out any sub-genres (this isn't used in call but is left as an option)
        for k in range(len(genres['genres'])):
            if genres['genres'][k] in const.GENRES and genres['genres'][k] not in gen:
                gen.append(genres['genres'][k])

    # gen will now hold the genres from the artists as well as the seed genres
    for i in range(len(const.seed_genres)):
        if const.seed_genres[i] not in gen:
            gen.append(const.seed_genres[i])

# ================================= optimization =====================================

    # seedList through the following code is the converted
    seedList = convertedSeeds

    # add seeds to master list so that the user can see what seeded the list
    masterList = seedList

    # while the target length is not reached
    while len(masterList) < length:

        # loop through the seed genres (target rec genres)
        for item in gen:

            # create two competing lists with same params (rec function is not static)
            list1 = rec_builder(seedList, limit=limit, genre=item)
            list2 = rec_builder(seedList, limit=limit, genre=item)

            # seem which song ID is in both lists and not in final list (append if so)
            for element in list1:
                if element in list2:
                    if element not in masterList:
                        masterList.append(element)


    # this is where an attribute based optimazation can be put
    '''
    # trim list if it is over target
    if len(masterList) > length:
        masterList = masterList[1:length + 1]
    '''

    return masterList