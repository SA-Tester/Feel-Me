#!/usr/bin/env python

# import pyfirmata2
import cv2
from deepface import DeepFace


# Get Video Input
def get_video_input():
    videoIn = cv2.VideoCapture(0, cv2.CAP_ANY)
    if not videoIn.isOpened():
        raise IOError("Cannot Open Webcam")
    return videoIn


# haarcascade_frontalface_default.xml is a pretrained model by OpenCV to detect faces
def load_face_cascade():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    return face_cascade


# Process the video stream
def process_stream():
    videoIn = get_video_input()
    face_cascade = load_face_cascade()
    detected_emotions = {"neutral": 0, "happy": 0, "angry": 0, "sad": 0, "surprise": 0, "disgust": 0, "fear": 0}

    while videoIn.isOpened():
        # _ to ignore the input of the boolean value that indicate whether or not the frame was captured successfully
        _, frame = videoIn.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        for x, y, w, h in face:
            # cv2.rectangle(image, start_point, end_point, color RGB Code, thickness)
            image = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            try:
                analyze = DeepFace.analyze(frame, actions=['emotion'])
                cv2.putText(image, analyze[0]['dominant_emotion'],
                            (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                detected_emotions[analyze[0]['dominant_emotion']] += 1 
                # print(analyze[0]['dominant_emotion'])
                
            except:
                cv2.putText(image, "No Face Detected", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Show video frame from camera
        cv2.imshow("video", frame)
        key = cv2.waitKey(1)

        # Terminate the process if "q" is pressed on keyboard
        if (key == ord('q')):
            break

    videoIn.release()
    cv2.destroyAllWindows()

    return detected_emotions


# Main function
if __name__ == "__main__":
    # Call the process stream function to begin the program
    emotions_dict = process_stream()

    # Print the dictionary of emotions
    print(emotions_dict)

    # Print the dominant emotion
    print(max(emotions_dict, key=emotions_dict.get))


# Function to process and the print the emotions array and the dominant emotion
# def process_and_print():
#     emotions_dict = process_stream()

#     # Print the dictionary of emotions
#     print(emotions_dict)

#     # Print the dominant emotion
#     print(max(emotions_dict, key=emotions_dict.get))

# if __name__ == "__main__":
#     # Create a Process
#     p = multiprocessing.Process(target=process_and_print)

#     # Start the process
#     p.start()

#     # Wait for 15 seconds or until process finishes
#     p.join(15)

#     # If thread is still active
#     if p.is_alive():
#         print("Process is still running, terminating now")
#         p.terminate()
#         p.join()