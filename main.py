
import const
import file
import playlist
import get
import recs
import tokenSP

def main():


    # ==================== input seed file to ... =======================================

    # inputseeds = file.inputseeds(const.inputseedfile)
    '''
    string_search = ['Haldern', 'Ants From Up There', 'Black Country, New Road']


    trackID = tokenSP.sp_modify_pub.search(q=string_search[1] + ' ' + string_search[0] + ' ' + string_search[2],
                                           type='track')

    artistID = trackID['tracks']['items'][0]['album']['artists'][0]['id']

    artistinfo = tokenSP.sp_modify_pub.artist(f'spotify:artist:{artistID}')
    print(artistinfo['genres'])
    '''
    # ------------------------ generate rec playlist from seeds --------------------------------
    '''
    rec_list = recs.rec_optimization(seedList=inputseeds, limit=const.rec_limit, length=const.rec_playlist_length)

    rec_playlist_id = playlist.trackID_to_playlist(trackIDs=rec_list, playlist_name=const.rec_playlist_name,
                                                   privacy=const.PUBLIC)

    rec_dict = playlist.playlistSongs(playlistURL=f"/{rec_playlist_id}?", justTrackID=False, privacy=const.PUBLIC)

    file.outputTSV(indict=rec_dict, outfile=const.seed_playlist_outfile, rank=False)

    print(f"spotify:playlist:{rec_playlist_id}")
    '''
    # ------------------------------------------------------------------------------------


    # ------------------------------- create playlist from file with dict -----------------------------------
    """
    file_to_playlist = file.inputseeds(infile=const.inputsongs)

    file_playlist_id = playlist.list_to_dict(inputmatrix=file_to_playlist, playlist_name=const.file_playlist_name,
                                             outfile=const.creation_output, privacy=const.PRIVATE)

    print(f"spotify:playlist:{file_playlist_id}")

# ----------------------------------------- playlist to TSV --------------------------

    matrix = playlist.playlist_to_list(playlistURL=const.playlist_to_read, privacy=const.playlist_privacy)

    file.output_seed_names(matrix=matrix, outfile=const.playlist_seed_file)
    """

    # ---------------------------------------------------------------------


    inputseeds = file.inputseeds('')

    iddd = playlist.list_to_playlist(inputmatrix=inputseeds, playlist_name='Rap Sorted', privacy=const.PUBLIC)

    print(f"spotify:playlist:{iddd}")



    return 0


# call main
if __name__ == '__main__':
    main()


