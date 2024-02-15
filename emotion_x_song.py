from emotion_detection import process_stream
from get_song_analysis import get_song_analytics
import csv

# For simplification process we shall asuume emotions to be either positive or negative
# Positive Emotions: Happy, Suprise, Neutral
# Negative Emotions: Sad, Fear, Disgust, Anger

# Get loudness decision
# Spotify Typical Loudness Interval: -60 to 0
def get_loudness_descision(loudness):
    if loudness < -50:
        return 0 #"SAD"
    elif loudness < -40:
        return 0 # "FEAR" or DISGUST
    elif loudness < -30:
        return 1 #"SUPRISE"
    elif loudness < -20:
        return 0 #"ANGER"
    elif loudness < -10:
        return 1 # "HAPPY"
    else:
        return 1 #"NEUTRAL"
    

# Get tempo decision
# Typical BPM Ramge: 60 - 180
def get_tempo_decision(tempo, tempo_confidence):
    if tempo > 150 and tempo_confidence > 0.7:
        return 1 # "HAPPY"
    elif tempo > 150 and tempo_confidence > 0.5:
        return 0 # "ANGRY"
    elif tempo > 120 and tempo_confidence > 0.7:
        return 1 # "SUPRISE"
    elif tempo > 120 and tempo_confidence > 0.3:
        return 0 # "FEAR"
    elif tempo > 80 and tempo_confidence > 0.7:
        return 0 # "SAD"
    elif tempo > 80 and tempo_confidence > 0.5:
        return 0 # "DISGUST"
    else:
        return 1 # "NEUTRAL"
    

# Get mode (major/ minor) decision
def get_mode_decision(mode, mode_confidence):
    if mode == "Major" and mode_confidence > 0.7:
        return 1 # "HAPPY"
    elif mode == "Major" and mode_confidence > 0.5:
        return 1 # "SUPRISE"
    elif mode == "Minor" and mode_confidence > 0.8:
        return 0 # "ANGER"
    elif mode == "Minor" and mode_confidence > 0.7:
        return 0 # "SAD"
    elif mode == "Minor" and mode_confidence > 0.5:
        return 0 # "FEAR"
    elif mode == "Minor" and mode_confidence > 0.3:
        return 0 # "DISGUST"
    else:
        return 1 # "NEUTRAL"
    

# Get positivity value
def get_positivity_value(loudness_decision, tempo_decision, mode_decision):
    if (loudness_decision + tempo_decision + mode_decision) >= 2:
        return "positive"
    else:
        return "negative"
    

# Classify the emotion into positive, negative or neutral
def map_emotion_to_positivity(emotion):
    if emotion in ["happy", "surprise", "neutral"]:
        return "positive"
    else:
        return "negative"


# Map emotions and songs
def get_song(dominant_emotion):
    # Open the file in read mode and pass it to CSV DictReader
    file = open('audio_analysis.csv', 'r')
    reader = csv.DictReader(file)

    # Initialize the song_emotion_matrix
    song_emotion_matrix = []

    # Iterate through the CSV file and append decisions to the song_emotion_matrix
    for song in reader:
        song_emotion_matrix.append(
            {
                "track_id": song["track_id"],
                "track_name": song["track_name"],
                "artist_name": song["artist_name"],
                "loudness_decision": get_loudness_descision(float(song["loudness"])),
                "tempo_decision":  get_tempo_decision(float(song["tempo"]), float(song["tempo_confidence"])),
                "mode_decision": get_mode_decision(song["mode"], float(song["mode_confidence"])),
                "final_decision": get_positivity_value(
                    get_loudness_descision(float(song["loudness"])), 
                    get_tempo_decision(float(song["tempo"]), float(song["tempo_confidence"])), 
                    get_mode_decision(song["mode"], float(song["mode_confidence"]))
                )
            }
        )

    # Close the file
    file.close()

    # Iterate through the song_emotion_matrix and return the track_id of the song that matches the dominant emotion
    for song in song_emotion_matrix:
        if song["final_decision"] == map_emotion_to_positivity(dominant_emotion):
            return song["track_id"]
        
   
# Main function
if __name__ == "__main__":
    # Call the process stream function to begin the program
    emotions_dict = process_stream()

    # Print the dominant emotion
    dominant_emotion = max(emotions_dict, key=emotions_dict.get)
    print("Dominant Emotion: ", dominant_emotion)

    get_song_analytics()
    print("Selected Track ID: ", get_song(dominant_emotion))