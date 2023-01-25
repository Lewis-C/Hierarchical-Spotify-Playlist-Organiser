from dotenv import load_dotenv # For adding .env variable keys to os
import spotipy # For interacting with spotify api
from spotipy.oauth2 import SpotifyOAuth # For authorising spotify user

# Load environment variables (api keys and such)
load_dotenv() 

# Init spotify, setting scope for use and logging in
scope = "playlist-read-private" 
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope)) 

def get_children(playlist_name):
    """
    Get children of the playlist passed to function
    Takes playlist name string as parameter
    """
    # Empty list for storing all playlist children details
    playlist_children = []

    # For every playlist
    for playlist in playlist_identifiers:
        # If the playlist is not the one being checked for children, is within the checked playlists name and is only a single hierarchical level lower
        if  playlist_name != playlist[0] and playlist_name in playlist[0] and playlist[0].count(" - ") == (playlist_name.count(" - ") + 1):
            # Add the details to the list
            playlist_children.append((playlist[0], playlist[1]))
    
    # Return list
    return playlist_children

def get_songs(playlist_id):
    """
    Function to return list of song name / id of any playlist passed to it
    Takes playlist id as parameter
    """

    # Variable for playlist content
    playlist_songs_source = (sp.playlist_items(playlist_id))
    # Variable for playlist songs
    playlist_songs_data = (playlist_songs_source['items'])
    # While content has remaining values
    while playlist_songs_source['next']:
        # Move list to those remaining values
        playlist_songs_source=sp.next(playlist_songs_source)
        # Extend the list of songs with new values
        playlist_songs_data.extend(playlist_songs_source['items'])

    # List for songs details. For loop populates list
    playlist_songs = []
    for song in playlist_songs_data:
        playlist_songs.append( song['track']['id'])

    return(playlist_songs)

def empty_playlist(playlist):
    all_songs = get_songs(playlist[1])
    for x in range(0, len(all_songs), 100):
        sp.playlist_remove_all_occurrences_of_items(playlist[1],all_songs[x:x+100])     

def add_songs(playlist, playlist_songs):
    all_songs = playlist_songs
    for x in range(0, len(all_songs), 100):
        sp.playlist_add_items(playlist[1],all_songs[x:x+100])     


# Creates empty list to store playlist details
playlist_identifiers = []
playlists = []

# For user, populate playlist with id and name (abstracts playlist to relevant data)
for playlist in (sp.current_user_playlists()['items']):
    playlist_identifiers.append((playlist['name'], playlist['id']))

# For each playlist in the playlist details
def get_playlist_songs(playlist):

    # Empty list for playlist songs
    playlist_songs = []

    # Find children
    playlist_children = get_children(playlist[0])

    # If theres no children, populate songs list with current playlist and return
    if not playlist_children:
        playlist_songs = get_songs(playlist[1])
        return playlist_songs

    # If there is children
    elif playlist_children:
        # Empty the current playlist
        empty_playlist(playlist)
        # For each child, recurse and gather the songs, returning to parent
        for child_playlist in playlist_children:
            child_songs = get_playlist_songs(child_playlist)
            if child_songs:
                playlist_songs.extend(child_songs)
        # If songs have been returned, add them to the playlist and return (Allows for 2 step hierarchy)
        if playlist_songs:
            add_songs(playlist, playlist_songs)
            return playlist_songs


for x in playlist_identifiers:
    get_playlist_songs(x)
