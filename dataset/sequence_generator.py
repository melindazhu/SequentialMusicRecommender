import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_sample_dataframe(sp_client, recently_played):
    track_metadata = []
    track_ids = []

    for obj in recently_played['items']:
        track = obj['track']
        track_ids.append(track['id'])
        track_metadata.append({
            'track_id': track['id'],
            'track_name': track['name'],
            'artist': track['artists'][0]['name'], # just get the main artist
            'album': track['album']['artists'][0]['name'],
            'popularity': track['popularity'],
            'played_at': obj['played_at']
        })

    features = sp_client.audio_features(track_ids)

    # Add audio features to the track data
    for i, feature in enumerate(features):
        if feature:
            track_metadata[i].update({
                'danceability': feature['danceability'],
                'energy': feature['energy'],
                'key': feature['key'],
                'loudness': feature['loudness'],
                'speechiness': feature['speechiness'],
                'acousticness': feature['acousticness'],
                'instrumentalness': feature['instrumentalness'],
                'liveness': feature['liveness'],
                'valence': feature['valence'],
                'tempo': feature['tempo']
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(track_metadata)
    print(df.head()) # visualize


def main():
    # set up client
    sp_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="[redacted]",
        client_secret="[redacted]",
        redirect_uri="[redacted]",
        scope="user-read-recently-played user-top-read"
    ))

    try:
        recently_played = sp_client.current_user_recently_played(limit=10)
        get_sample_dataframe(sp_client, recently_played)
    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
    main()
