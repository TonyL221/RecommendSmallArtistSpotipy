import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Set up your Spotify API credentials
client_id = '1dd679e02daa4de4bf2de3d89a86180d'
client_secret = '88c84edcdcaf4f999fc3d11eed560856'

# Authenticate with Spotify using the client credentials flow
class UsefulFunctions:
    def __init__(self):
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))
        self.sp=sp
        
    def cleanUpLink(self,link):
        question_mark_index = link.find("?")
        link.split('https://open.spotify.com/playlist')
        cleaned = link[:question_mark_index] 
        return str(cleaned)
    
    def get_audio_features(self,track_id):
        audio_features = self.sp.audio_features(track_id)
        audio_features = audio_features[0]
        danceability = audio_features['danceability']
        energy = audio_features['energy']
        loudness = audio_features['loudness']
        liveness = audio_features['liveness']
        instrumentalness = audio_features['instrumentalness']
        acousticness = audio_features['acousticness']
        speechiness = audio_features['speechiness'] 
        duration = audio_features['duration_ms']
        tempo = audio_features['tempo']
        valence = audio_features['valence']
        arr = [acousticness,danceability,duration,energy,instrumentalness,liveness,loudness,speechiness,tempo,valence]
        return arr

    def get_target_values(self,setOfTrackIds):
        acousticness,danceability,duration,energy,instrumentalness,liveness,loudness,speechiness,tempo,valence=0,0,0,0,0,0,0,0,0,0
        l = len(setOfTrackIds)
        print(setOfTrackIds)
        for track_id in setOfTrackIds:
            print(track_id)
            acousticness+= self.get_audio_features(self,track_id)[0]
            danceability+= self.get_audio_features(self,track_id)[1]
            duration += self.get_audio_features(self,track_id)[2]
            energy+= self.get_audio_features(self,track_id)[3]
            instrumentalness+= self.get_audio_features(self,track_id)[4]
            liveness+= self.get_audio_features(self,track_id)[5]
            loudness+= self.get_audio_features(self,track_id)[6]
            speechiness+= self.get_audio_features(self,track_id)[7]
            tempo+= self.get_audio_features(self,track_id)[8]
            valence+= self.get_audio_features(self,track_id)[9] 
        arr = (acousticness/l,danceability/l,duration/l,energy/l,instrumentalness/l,liveness/l,loudness/l,speechiness/l,tempo/l,valence/l)
        return arr
