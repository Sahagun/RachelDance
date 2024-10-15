import cv2 # OpenCV library for image processing. 
import mediapipe as mp # MediaPipe library for various computer vision tasks. 
import numpy as np # Numerical computing library. 
import AngleCalc as sc

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import json

mpPose = mp.solutions.pose # MediaPipe's pose estimation solution. 
pose = mpPose.Pose()
mp_drawing = mp.solutions.drawing_utils
pose_connections = mp.solutions.pose.POSE_CONNECTIONS



file_path = "Dance_2.mp4" 
json_file_path = file_path + ".json"


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
    print("Angle File Created")



def make_recommendations(partIndex, angle_diff):
    ''' Returns the recommendation as a string '''
    global recommendation_part_index

    if (abs(angle_diff) < 20):
        recommendation_part_index = -1
        return "Great!"

    body_part = get_body_part(partIndex)
    recommendation_part_index = partIndex

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


def getLandmarkIndexFromBodyPartIndex(index):
    landmark_index = [ 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28 ]
    return landmark_index[index]


def normalize_angle(angle):
    normalized_angle = (angle + 180) % 360 - 180
    return normalized_angle

def scoreImage(originalAngles, userAngles): 
    '''
    Calculate the Score of the angles
    '''
    i = 0 
    totalPercentage = 0 
    calculatedAngles = 0 
    
    percents = []
    differences  = []
    while (i < len(originalAngles)): 
        if (originalAngles[i] is not None): 
            calculatedAngles += 1 
        if (userAngles[i] is not None) and (originalAngles[i] is not None): 
            diff = (userAngles[i] - originalAngles[i])
            differences.append(normalize_angle(diff))
            diff = abs(normalize_angle(diff))
            
            percentage = diff/180

            percentage = (1 - percentage)*100
            totalPercentage += percentage 
            percents.append(percentage)
        i+=1
    if calculatedAngles == 0:
        return -1,-1,[]
      
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


def placeScore(image, score, recommendation):
    ''' Add the text to the image '''
    font = cv2.FONT_HERSHEY_SIMPLEX

    org = (30, 50)
    fontScale = 1
    color = (128, 1, 255)
    thickness = 2

    text = "Score: {score:0.2f}".format(score=score)
    image = cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA)

    text = "Level: {level}".format(level= score // 100 + 1)
    image = cv2.putText(image, text, (30, 100), font, fontScale, color, thickness, cv2.LINE_AA)

    text = "{rec}".format(rec = recommendation)
    image = cv2.putText(image, text, (30, frame_height - 30), font, fontScale, color, thickness, cv2.LINE_AA)
    
    return image




def getLandmarkAngles(landmarks):
    res = sc.resultsLandmarks(landmarks)
    
    if len(res) > 0:
        videoAngles = []    
        videoAngles.append(sc.calculate_image_angle(23, 11, 13, res)) #left shoulder 
        videoAngles.append(sc.calculate_image_angle(24, 12, 14, res)) #right shoulder
        videoAngles.append(sc.calculate_image_angle(11, 13, 15, res)) #left elbow 
        videoAngles.append(sc.calculate_image_angle(12, 14, 16, res)) #right elbow 
        videoAngles.append(sc.calculate_image_angle(13, 15, 17, res)) #left wrist 
        videoAngles.append(sc.calculate_image_angle(14, 16, 18, res)) #right wrist 
        videoAngles.append(sc.calculate_image_angle(11, 23, 25, res)) #left leg lift 
        videoAngles.append(sc.calculate_image_angle(12, 24, 26, res)) #right leg lift 
        videoAngles.append(sc.calculate_image_angle(23, 25, 27, res)) #left knee 
        videoAngles.append(sc.calculate_image_angle(24, 26, 28, res)) #right knee 
        videoAngles.append(sc.calculate_image_angle(25, 27, 31, res)) #left shin ankle toes 
        videoAngles.append(sc.calculate_image_angle(26, 28, 32, res)) #right shin ankle toes 
        
        return videoAngles
    return None


def compareFrames(imageAngles, frameNumber):
    global danceScore, score_list, recommendation, users_landmarks, recommendation_part_index
    
    
    if imageAngles is not None:
        image1Angles = videoAngles[frameNumber] 

        imageScore, partIndex, diff = scoreImage(imageAngles, image1Angles) 
        if imageScore < 0:
            return
        danceScore += imageScore / 100
        users_landmarks = landmarks
        if frameNumber % update_every_nth_frame == 0:    
            recommendation = make_recommendations(partIndex, diff)

    else:
        if frameNumber % update_every_nth_frame == 0:    
            recommendation = ""
            recommendation_part_index = -1
        
        
        
def draw_landmarks_2(image, landmarks, connections=pose_connections): 
    global recommendation_part_index   
    # Draw landmarks on the image
    if landmarks.pose_landmarks and landmarks.pose_landmarks.landmark:
        # for landmark in landmarks.pose_landmarks.landmark:
        #     x = int(landmark.x * image.shape[1])
        #     y = int(landmark.y * image.shape[0])
        #     image = cv2.circle(image, (x, y), 5, (0, 255, 0), 5)
        
        # Show The recommended Landmark
        if(recommendation_part_index >= 0):
            index = getLandmarkIndexFromBodyPartIndex(recommendation_part_index)
            rec_landmark = landmarks.pose_landmarks.landmark[index]
            
            x = int(rec_landmark.x * image.shape[1])
            y = int(rec_landmark.y * image.shape[0])
            image = cv2.circle(image, (x, y), 5, (0, 0, 255), 20)


        # Show the Pose Estimation 
        if connections:
            mp_drawing.draw_landmarks(image, landmarks.pose_landmarks, connections)
        
        return image




danceScore = 0  
recommendation = ""
recommendation_part_index = -1
users_landmarks = []
frameNumber = 0 


cap = cv2.VideoCapture(0) # display what you would see in a camera right now 
cap1 = cv2.VideoCapture(file_path)

# frame_width = 800
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
frame_height = 800
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

update_every_nth_frame = 3

        
with mpPose.Pose(static_image_mode=False, model_complexity=0, enable_segmentation=True, min_detection_confidence=0.5) as pose:
    while cap.isOpened():
        # Capture frame-by-frame
        ret, camera_frame = cap.read() # WebCam
        if not ret:
            print("Error Reading Camera")
            break

        ret, video_frame = cap1.read() # Video
        
        camera_frame = cv2.flip(camera_frame, 1)

        if not ret:
            # Video Done
            cv2.waitKey()
            break
        
        
        landmarks = pose.process(camera_frame)
        landmarkAngles = getLandmarkAngles(landmarks)
        
        
        compareFrames(landmarkAngles, frameNumber)
        
        if frameNumber % update_every_nth_frame == 0:    
            '''
            TODO
            add audio here using the `recommendation` string variable
            '''
            pass



        video_frame = resize_image(video_frame, height = frame_height)
        camera_frame = resize_image(camera_frame, height = frame_height)
        
        if landmarks:
            image = draw_landmarks_2(camera_frame, landmarks)

        # image = cv2.hconcat([video_frame, camera_frame])
        image = cv2.vconcat([video_frame, camera_frame])
            
    
        image = placeScore(image, danceScore, recommendation)

        # Display the resulting frame
        cv2.imshow('Video', image)
        frameNumber+=1 

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture object and close all windows
cap.release()
cap1.release() 

cv2.destroyAllWindows()

exit()
