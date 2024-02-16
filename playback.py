from init_spotipy import init_spotipy
from emotion_detection import process_stream
from get_song_analysis import get_song_analytics
from emotion_x_song import get_song


# Get a playback device id
def get_device_id(spotipyObj):
    return spotipyObj.devices()["devices"][0]["id"]


# Print info
def print_info(dominant_emotion, track_id, track_name, artist_name, device_id):
    print("\n==================== NOW PLAYING ====================")
    print("Dominant Emotion: ", dominant_emotion)
    print("Selected Track ID: ", track_id)
    print("Selected Track Name: ", track_name)
    print("Selected Track Artist: ", artist_name)
    print("Playback Device ID: ", device_id)
    print("=====================================================\n")


# Main function
if __name__ == "__main__":
    # Initialize a new spotipy object
    spotipyObj = init_spotipy()

    # Call the process stream function to begin the program
    emotions_dict = process_stream()

    # Print the dominant emotion
    dominant_emotion = max(emotions_dict, key=emotions_dict.get)

    get_song_analytics(spotipyObj)
    song_info =  get_song(dominant_emotion)
    track_id = song_info['track_id']
    track_name = song_info['track_name']
    artist_name = song_info['artist_name']

    # Get devices
    device_id = get_device_id(spotipyObj)

    # Form a URI
    uri = 'spotify:track:' + track_id
    
    try:
        spotipyObj.start_playback(device_id=device_id, uris=[uri])
        print_info(dominant_emotion, track_id, track_name, artist_name, device_id)

    except Exception as e:
        print(e)
