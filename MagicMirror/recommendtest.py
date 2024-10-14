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

'''
0-left shoulder 
1-right shoulder
2-left elbow 
3-right elbow 
4-left wrist 
5-right wrist 
6-left leg lift 
7-right leg lift 
8-left knee 
9-right knee 
10-left shin ankle toes 
11-right shin ankle toes 
'''

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

def imageScore(originalAngles, userAngles): 
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
            
            print("angle_1: {}, angle_2: {}, diff: {}".format(originalAngles[i], userAngles[i], diff))
            # percentage = diff/originalAngles[i] 
            percentage = diff/180
            print("percentage: {:.0f}".format((1 - percentage)*100))

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
  

frame_path_1 = 'image_1.png'
frame_path_2 = 'image_1.png'

image_1 = cv2.imread(frame_path_1)
image_2 = cv2.imread(frame_path_2)
image_2 = cv2.flip(image_2, 1)


image_angles_1 = sc.getImageAngles(image_1)
image_angles_2 = sc.getImageAngles(image_2)

print((image_angles_1[1]))
print((image_angles_2[1]))

score, partIndex, diff = imageScore(image_angles_1, image_angles_2)

print()
print("score:", score)
print("part:", get_body_part(partIndex))
print("diff:", diff)

recommendation = make_recommendations(partIndex, diff)

print(recommendation)