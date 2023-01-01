
'''
Summary: reads in a file and returns a list of lists (matrix) in the for of
         [ ['track1', 'artist1', 'album1'], ... , ['trackN', 'artistN', 'alubmN'] ]
PRE: called from main with const.file 
POST: returns matrix of (typically seed) information to use in query search of spotify
'''
def inputseeds(infile):

    # defining read in matrix
    inputmatrix = []

    # ensure that the input file is a tsv
    file = open(infile, "r")
    line = file.readline()

    while (line != ""):
        # splitting by tabs to lead the proper list
        line = line.split('\t')

        # removing the new line from entering
        line[-1] = line[-1].strip("\n")

        # adding this to the output matrix
        inputmatrix.append(line)

        # read a new line
        line = file.readline()

    # close file
    file.close()

    return inputmatrix


def outputTSV(indict, outfile, rank):

    file = open(outfile, "w")

    if rank:
        ordering = ['track_name', 'track_id', 'rank', 'acousticness', 'danceability', 'duration_ms',
                    'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness',
                    'tempo', 'time_signature', 'track_exp', 'track_pop', 'valence', 'artist_names',
                    'artist_ids', 'artists_genres', 'album_name', 'album_id', 'album_release', 'album_length']
    else:
        ordering = ['track_name', 'track_id', 'acousticness', 'danceability', 'duration_ms', 'energy',
                    'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo',
                    'time_signature', 'track_exp', 'track_pop', 'valence', 'artist_names', 'artist_ids',
                    'artists_genres', 'album_name', 'album_id', 'album_release', 'album_length']

    file.write('\t'.join(ordering) + '\n')

    for i, j in enumerate(indict):
        temp = []
        for name in ordering:
            temp.append(indict[j][name])
        file.write('\t'.join(str(item) for item in temp) + '\n')

    # ================= create track key list ==========================================

    file.close()

    return 0


'''
Summary: After calling playlist_to_list and returns the seed search strings.
         This will be used to have each title to search and be able to rank independently
         to then create an output dictionary of ranked songs
PRE: Inputs a matrix of the names to search for each track (see  example for inputseeds)
POST: outputs to a file the search strings needed 
'''
def output_seed_names(matrix, outfile):

    file = open(outfile, 'w')

    for i in range(len(matrix)):
        file.write('\t'.join(matrix[i]) + '\n')

    file.close()

    return 0