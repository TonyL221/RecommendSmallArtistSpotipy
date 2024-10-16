import spotipy
from spotipy.oauth2 import SpotifyOAuth
from backend import UsefulFunctions
# Set your Spotify API credentials
CLIENT_ID = [clientID]
CLIENT_SECRET = [clientSecret]
REDIRECT_URI = 'http://127.0.0.1:8080/callback'  # Set this to a valid redirect URI

# Initialize Spotipy with OAuth authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope='playlist-modify-public playlist-modify-private'
))

UF = UsefulFunctions()




# Get the user's input playlist tracks
input_playlist_id = UF.cleanUpLink('https://open.spotify.com/playlist/4hOKQuZbraPDIfaGbM3lKI?si=7dee30b2cb144e1a')
if sp.playlist_items(playlist_id=input_playlist_id)['total']==0:
    print("Please input a playlist with actual songs in them")
    exit() 
input_playlist = sp.playlist_tracks(input_playlist_id)        

# Create a new playlist
user_id = sp.me()['id']
playlist_name = 'Smaller Artists Playlist'
playlist_description = 'Playlist with tracks from smaller artists'
new_playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description=playlist_description)
playlist_id = new_playlist['id']

# Extract track Ids and make sure no duplicates
trackIds = set()
for track in input_playlist['items']:
    trackIds.add(track['track']['id'])

#convert into list for ease of access
track_ids = list(trackIds)
#variable for iteration 
i=0

#PLAYLIST LENGTH VARIABLE
lengthOfPlaylist = 25
#MAX NUMBER OF FOLLWERS VARIABLE
maxFollowers = 10000

while sp.playlist_items(playlist_id=playlist_id)['total']<lengthOfPlaylist and i<len(track_ids):
    #for out of bounds errors and iteration problems
    listOfTrackIds = [track_ids[i]]

    acousticness,danceability,duration,energy,instrumentalness,liveness,loudness,speechiness,tempo,valence = UF.get_target_values(set(listOfTrackIds))

    # Get recommendations based on the input playlist artists
    recommendations = sp.recommendations(seed_tracks=listOfTrackIds, 
                                    limit=20,max_popularity=40, # Adjust the limit as needed
                                    target_danceability=danceability,
                                    target_energy=energy,
                                    target_instrumentalness=instrumentalness,
                                    target_liveness = liveness,
                                    target_speechiness = speechiness,
                                    target_valence = valence) 

    # Add tracks from smaller artists to the new playlist
    for track in recommendations['tracks']:
        artists = [artist['id'] for artist in track['artists']]
        artist_followers = sp.artists(artists)['artists'][0]['followers']['total']
        if (maxFollowers >= artist_followers>=100)and(sp.playlist_items(playlist_id=playlist_id)['total']<lengthOfPlaylist): 
            #the 100 is for quality control, feel free to change
            track_uri = track['uri']
            sp.playlist_add_items(playlist_id, [track_uri])
                
    print(i)
    i+=1
    #for ui make a thing that prompts for lengthOfPLaylist and maxFollowers
