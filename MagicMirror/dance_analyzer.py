every_nth_frame = True
show_landmarks = True

import tkinter as tk 
import cv2 # OpenCV library for image processing. 
import mediapipe as mp # MediaPipe library for various computer vision tasks. 
import numpy as np # Numerical computing library. 
import AngleCalc as sc
from PIL import Image, ImageTk 
# import tkinter as tk 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import json

mpPose = mp.solutions.pose # MediaPipe's pose estimation solution. 
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils # Utility functions for drawing landmarks and connections. 

file_path = "Dance.mp4" 


json_file_path = file_path + ".json"

#print(json_file_path)

videoAngles = []

if os.path.exists(json_file_path):
    print("Loading Video data")
    with open(json_file_path, 'r') as file:
        videoAngles = json.load(file)
else:
    print("Analyzing Video")
    videoAngles = sc.getVideoAngles(file_path) 
    with open(json_file_path, 'w') as file:
        json.dump(videoAngles, file)
    print("File does not exist")



def make_recommendations(partIndex, angle_diff):
  if (abs(angle_diff) < 20):
    return "Great!"

  body_part = get_body_part(partIndex)

  if angle_diff < 0:
    return "Try moving your {} in.".format(body_part)
  else:
    return "Try moving your {} out.".format(body_part)

def get_body_part(index):
  parts = [
    "left shoulder", 
    "right shoulder",
    "left elbow," 
    "right elbow", 
    "left wrist", 
    "right wrist", 
    "left leg lift", 
    "right leg lift", 
    "left knee", 
    "right knee", 
    "left shin ankle toes", 
    "right shin ankle toes" 
  ]
  return parts[index]

def normalize_angle(angle):
    normalized_angle = (angle + 180) % 360 - 180
    return normalized_angle

def scoreImage(originalAngles, userAngles): 
    i = 0 
    totalPercentage = 0 
    calculatedAngles = 0 
    
    percents = []
    differences  = []
    while (i < len(originalAngles)): 
        if (originalAngles[i] is not None): 
            calculatedAngles += 1 
        if (userAngles[i] is not None) and (originalAngles[i] is not None): 
            # print(userAngles[i], originalAngles[i])
            diff = (userAngles[i] - originalAngles[i])
            differences.append(normalize_angle(diff))
            diff = abs(normalize_angle(diff))
            
            # print("angle_1: {}, angle_2: {}, diff: {}".format(originalAngles[i], userAngles[i], diff))
            # percentage = diff/originalAngles[i] 
            percentage = diff/180
            # print("percentage: {:.0f}".format((1 - percentage)*100))

            percentage = (1 - percentage)*100
            totalPercentage += percentage 
            percents.append(percentage)
        i+=1
    if calculatedAngles == 0:
        return 0
      
    min_index = percents.index(min(percents))
    
      
    score = totalPercentage/calculatedAngles
    # if score < 0:
    #     return 0
    return score, min_index, differences[min_index]

def resize_image(img, height = 720):
    h, w = img.shape[:2]
    aspect = w/h

    sh =  height
    sw = np.round(aspect * height).astype(int)


    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA
    else: # stretching image
        interp = cv2.INTER_CUBIC
        
    # aspect ratio of image    
    scaled_img = cv2.resize(img, (sw, sh), interpolation=interp)
    return scaled_img

    

cap = cv2.VideoCapture(0) # display what you would see in a camera right now 
cap1 = cv2.VideoCapture(file_path)

frame_width = 640
frame_height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

import threading

# Event to control frame processing
process_event = threading.Event()

# Create a lock
counter_lock = threading.Lock()


mp_drawing = mp.solutions.drawing_utils
pose_connections = mp.solutions.pose.POSE_CONNECTIONS

def draw_landmarks(image, landmarks, connections=pose_connections):
    # Convert the image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Draw landmarks on the image
    for landmark in landmarks:
        # print("landmark",landmark)
        if landmark:
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 5, (0, 255, 0), 5)
    print("Drawing on image")
    
    # Optionally draw connections between landmarks
    # if connections:
    #     mp_drawing.draw_landmarks(image, landmarks, connections)
    
    # Convert the image back to BGR
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    return image_bgr


def process_frame(camera_frame, frameNumber):
    # print("Processing frame:", frameNumber)
    global danceScore
    imageAngles = sc.getImageAngles(camera_frame)
    # print("imageAngles", imageAngles)
    
    if len(imageAngles) > 0:
        image1Angles = videoAngles[frameNumber] 

        imageScore = sc.imageScore(imageAngles, image1Angles) 
        danceScore += imageScore 
    process_event.set()  # Signal that processing is done

score_list = []

def process_nth_frame(camera_frame, frameNumber):
    # print("Processing nth frame:", frameNumber)
    global danceScore, score_list, recommendation, users_landmarks
    imageAngles, landmarks = sc.getImageAngles(camera_frame)
    # print("imageAngles", imageAngles)
    
    if imageAngles is not None:
        image1Angles = videoAngles[frameNumber] 

        # imageScore = sc.imageScore(imageAngles, image1Angles) 
        try:
            imageScore, partIndex, diff = scoreImage(imageAngles, image1Angles) 
            with counter_lock:
                # danceScore += 1
                recommendation = make_recommendations(partIndex, diff)
                danceScore += imageScore 
                users_landmarks = landmarks
        except:
            pass

    else:
        with counter_lock:
            recommendation = ""
            # users_landmarks = landmarks


    # print("Done processing nth frame:", frameNumber)



font = cv2.FONT_HERSHEY_SIMPLEX
# org = (20, frame_height - 20)
# fontScale = 2
# color = (0, 255, 0)
# thickness = 3

org = (30, 50)
fontScale = 1
color = (128, 1, 255)
thickness = 2

# Use putText() function

def placeScore(image, score, recommendation):
    text = "Score: {score:0.2f}".format(score=score)
    image = cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA)

    text = "Level: {level}".format(level= score // 100 + 1)
    image = cv2.putText(image, text, (30, 100), font, fontScale, color, thickness, cv2.LINE_AA)

    text = "{rec}".format(rec = recommendation)
    image = cv2.putText(image, text, (30, frame_height - 30), font, fontScale, color, thickness, cv2.LINE_AA)
    
    return image


danceScore = 0  
recommendation = ""
users_landmarks = []
frameNumber = 0 
countEveryFrame = 5

process_event.set()

while cap.isOpened():
    # Capture frame-by-frame
    _, camera_frame = cap.read() # WebCam
    ret, video_frame = cap1.read() # Video
    
    camera_frame = cv2.flip(camera_frame, 1)

    if not ret:
        print(len(score_list))
        cv2.waitKey()
        break


    if every_nth_frame:
        if frameNumber % countEveryFrame == 0:
            threading.Thread(target=process_nth_frame, args=(camera_frame,frameNumber,)).start()
            

    else:
        if process_event.is_set():
            process_event.clear()
            threading.Thread(target=process_frame, args=(camera_frame,frameNumber,)).start()


    video_frame = resize_image(video_frame, height = frame_height)
    #camera_frame = resize_image(camera_frame)
    if show_landmarks:
        if users_landmarks :
            draw_landmarks(camera_frame, users_landmarks)
    
    image = cv2.hconcat([video_frame, camera_frame])
        
        
    frameNumber+=1 
    # print("frameNumber:", frameNumber, " - danceScore:", danceScore)
    image = placeScore(image, danceScore, recommendation)

    # Display the resulting frame
    cv2.imshow('Video', image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cap1.release() 

cv2.destroyAllWindows()

exit()
