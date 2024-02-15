from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import csv
import random

# Load .env file
def load_env_file():
    load_dotenv()

# Initialize SpotifyOAuth object
def init_spotipy():
    spotify_auth = SpotifyOAuth(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'), redirect_uri=os.getenv('REDIRECT_URL'), scope=os.getenv('SCOPE'))

    # Create a spotify object
    spotifyObj = Spotify(auth_manager=spotify_auth)
    # print("access token: ", spotify_auth.get_access_token(as_dict=False))

    return spotifyObj

# Load pre-saved spotify category csv file
def get_song_categories():
    file1 = open('categories.csv', 'r')
    category_file = csv.reader(file1)
    category_list = []
    for row in category_file:
        category_list.append({"name": row[0], "id": row[1]})

    return category_list


# Get a random category
def get_random_category(category_list):
    random_index = random.randint(0, len(category_list) - 1)
    chosen_cateogry = category_list[random_index]
    return chosen_cateogry


# Get a category playlist
def get_category_playlist(spotifyObj, category_id):
    category_playlists = spotifyObj.category_playlists(category_id=category_id, limit=1, offset=0)
    playlist = category_playlists["playlists"]["items"][0]
    return (playlist["name"], playlist["id"])


# Get a songs in the playlist
def get_playlist_songs(spotifyObj, playlist_id):
    track_list = []

    playlist_songs = spotifyObj.playlist_tracks(playlist_id, fields=None, limit=3, offset=0, additional_types=('track', ))
    for song in playlist_songs['items']:
        track_list.append({
            "track_id": song['track']['id'], 
            "track_name": song['track']['name'], 
            "artist_name": song['track']['artists'][0]['name']
            }
        )

    return track_list


# Get audio features of a track
def get_audio_analysis(spotifyObj, track_id):
    audio_analysis = spotifyObj.audio_analysis(track_id)
    return audio_analysis


# Save audio features of the tracks
def save_audio_analysis(song, audio_analysis): 
    # Check whether file already exists
    file_exists = os.path.isfile('audio_analysis.csv')

    # Open file in append mode and initiate headers
    with open ('audio_analysis.csv', 'a') as csvfile:
        headers = [
            "track_id", 
            "track_name", 
            "artisit_name", 
            "timestamp", 
            "analysis_time", 
            "num_samples", 
            "duration", 
            "loudness", 
            "tempo", 
            "tempo_confidence", 
            "key", 
            "key_confidence", 
            "mode", 
            "mode_confidence"
        ]
        
        # Create a csv writer object
        csv_writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers)

        # Write the header if the file doesn't exist
        if not file_exists:
            csv_writer.writeheader()  # file doesn't exist yet, write a header

        # Write the data
        csv_writer.writerow(
            {
                "track_id": song["track_id"], 
                "track_name": song["track_name"],
                "artisit_name": song["artist_name"],
                "timestamp": audio_analysis["meta"]["timestamp"],
                "analysis_time": audio_analysis["meta"]["analysis_time"],
                "num_samples": audio_analysis["track"]["num_samples"],
                "duration": audio_analysis["track"]["duration"],
                "loudness": audio_analysis["track"]["loudness"],
                "tempo": audio_analysis["track"]["tempo"],
                "tempo_confidence": audio_analysis["track"]["tempo_confidence"],
                "key": audio_analysis["track"]["key"],
                "key_confidence": audio_analysis["track"]["key_confidence"],
                "mode": audio_analysis["track"]["mode"],
                "mode_confidence": audio_analysis["track"]["mode_confidence"]
            }
        )

        # Close the file
        csvfile.close()


# Main Function
if __name__ == "__main__":
    # load environment variables
    load_env_file()

    # Remove the old audio_analysis csv file
    try:
        os.remove('audio_analysis.csv')
    except FileNotFoundError as e:
        print("File not found")

    # Initialize SpotifyOAuth object
    spotipyObj = init_spotipy()

    # Get song categories from csv file
    category_list = get_song_categories()

    # Get a random category
    # Order of dict: Category Name, Category ID
    chosen_category = get_random_category(category_list)
    print(chosen_category["name"].strip(), chosen_category["id"].strip())

    # Get a category playlist
    # Order of tuple: Playlist Name, Playlist ID
    category_playlist = get_category_playlist(spotipyObj, chosen_category["id"].strip())
    print("Chosen Playlist: ", category_playlist)

    # Get a songs in the playlist
    # Order of dict: Artist, Song Name, Song ID
    playlist_songs = get_playlist_songs(spotipyObj, category_playlist[1])
    print("Playlist Songs: ", playlist_songs)

    # Save audio features of per track
    for song in playlist_songs:
        audio_analysis = get_audio_analysis(spotipyObj, song["track_id"])
        save_audio_analysis(song, audio_analysis)