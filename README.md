# Hierarchical Spotify Playlist Organiser

This is a basic script using Spotipy (Python spotify package) to automically update spotify playlists based on a hierarchical structure. Upon running the script, any playlists recognised as "parents" will be refreshed with the contents of it's "children". Playlist hierarchy is identified using " - " between basic naming for a playlist. For example:

The script connects to the Spotify API using keys hidden in a .env file. To run the script, it will need to be connected via your own details.  
