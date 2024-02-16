from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os


# Load .env file
def load_env_file():
    load_dotenv()


# Initialize SpotifyOAuth object
def init_spotipy():
    load_env_file()

    spotify_auth = SpotifyOAuth(
        client_id=os.getenv('CLIENT_ID'), 
        client_secret=os.getenv('CLIENT_SECRET'), 
        redirect_uri=os.getenv('REDIRECT_URL'), 
        scope=os.getenv('SCOPE'),
        open_browser=False
    )

    # Create a spotify object
    spotifyObj = Spotify(auth_manager=spotify_auth)
    # print("access token: ", spotify_auth.get_access_token(as_dict=False))

    return spotifyObj