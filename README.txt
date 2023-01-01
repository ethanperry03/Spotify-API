Created by Ethan Perry
link to https://github.com/ethanperry03
found in the repository Spotify-API

Summary:

    This project began when I realized by Spotify recommendation playlists weren't what I wanted exactly. I also
    have trouble finding new music I want to listen to so having random songs to maybe find new artists is the
    key use of this project. Having control over this while writing some code was a fun solution I found.

    The project uses the spotify API and python requests to use their methods and access a variety of information
    about my own account on spotify and music I take interest in.


Work you must to do get this up and running:

    - create and add the token info to your spotify api dashboard (see cred.py for instructions)
    - read this readme
    - other notes and things needed
        - add text and tsv files to read in information and output information as desired (in const)
        - add seed information, playlist links, and other limits (in const)


Usage of Main.py:

    This application has several uses and the flows will be listed.
    See main for the suggested flows for variety of uses.

    - Load a file of songs (from spreedsheet) and it will create a playlist instead of manually entry:
        It is important to note the text file is tab seperated and also it is in what I call either
        'string search' or 'seed string' format (song name, artist, album of song)
        This is very useful if you can find lists of songs you want in a tsv file or you'd rather type
        out songs instead of manual entry on spotify application.

    - Load seed songs to create a recommended playlist
        Load a file with songs you wish to seed a playlist with and the algorithm will bloom with realted songs
        It is very important to note there is some legwork to be done in const.py for this to work such as
        add seed genres, rec playlist length, name, and if you want to output attributes to files.

    - Read a playlist or files of songs or rec playlist to get data of tracks
        This is for the statically inclunded to analyse the attributes of their favorite songs to see if there
        are any patterns. These attributes are parameters in the rec function of spotify and can be used to
        get even better recs. This is yet to be implemented in my work.


Files included:

    README.txt  - this file

    main.py     - main environment that calls all other functions and is where user will write to access the refined
                  methods I created that access the spotify API

    cred.py     - this is where you enter the tokens for your API in the developer dashboard

    const.py    - This is where constants are held as well as certain pieces of user input for specifications in
                  playlist creation. Things such as seed genre, rec playlist length, text files, etc

    For the following, these are background methods doing much of the heavy lifting and the functions in each file
    have documentation that should explain the data flow of each:

    recs.py, get.py, file.py, playlist.py, tokenSP.py


Updates yet to be implemented:

    - A better method to use the recs.optimization when the list overflows target length

    - attribute based recommendations