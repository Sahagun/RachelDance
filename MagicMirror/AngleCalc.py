import numpy as np # angles to compare 
import mediapipe as mp
import cv2

mp_pose = mp.solutions.pose

landmarks = [] 
landmarks.append(mp_pose.PoseLandmark.NOSE) #0 
landmarks.append(mp_pose.PoseLandmark.LEFT_EYE_INNER) 
landmarks.append(mp_pose.PoseLandmark.LEFT_EYE)
landmarks.append(mp_pose.PoseLandmark.LEFT_EYE_OUTER)
landmarks.append(mp_pose.PoseLandmark.RIGHT_EYE_INNER)
landmarks.append(mp_pose.PoseLandmark.RIGHT_EYE) #5 
landmarks.append(mp_pose.PoseLandmark.RIGHT_EYE_OUTER)
landmarks.append(mp_pose.PoseLandmark.LEFT_EAR)
landmarks.append(mp_pose.PoseLandmark.RIGHT_EAR)
landmarks.append(mp_pose.PoseLandmark.MOUTH_LEFT)
landmarks.append(mp_pose.PoseLandmark.MOUTH_RIGHT) #10
landmarks.append(mp_pose.PoseLandmark.LEFT_SHOULDER)
landmarks.append(mp_pose.PoseLandmark.RIGHT_SHOULDER)
landmarks.append(mp_pose.PoseLandmark.LEFT_ELBOW)
landmarks.append(mp_pose.PoseLandmark.RIGHT_ELBOW)
landmarks.append(mp_pose.PoseLandmark.LEFT_WRIST) #15
landmarks.append(mp_pose.PoseLandmark.RIGHT_WRIST)
landmarks.append(mp_pose.PoseLandmark.LEFT_PINKY)
landmarks.append(mp_pose.PoseLandmark.RIGHT_PINKY)
landmarks.append(mp_pose.PoseLandmark.LEFT_INDEX)
landmarks.append(mp_pose.PoseLandmark.RIGHT_INDEX) #20 
landmarks.append(mp_pose.PoseLandmark.LEFT_THUMB)
landmarks.append(mp_pose.PoseLandmark.RIGHT_THUMB)
landmarks.append(mp_pose.PoseLandmark.LEFT_HIP)
landmarks.append(mp_pose.PoseLandmark.RIGHT_HIP)
landmarks.append(mp_pose.PoseLandmark.LEFT_KNEE) #25 
landmarks.append(mp_pose.PoseLandmark.RIGHT_KNEE)
landmarks.append(mp_pose.PoseLandmark.LEFT_ANKLE)
landmarks.append(mp_pose.PoseLandmark.RIGHT_ANKLE)
landmarks.append(mp_pose.PoseLandmark.LEFT_HEEL)
landmarks.append(mp_pose.PoseLandmark.RIGHT_HEEL) #30 
landmarks.append(mp_pose.PoseLandmark.LEFT_FOOT_INDEX)
landmarks.append(mp_pose.PoseLandmark.RIGHT_FOOT_INDEX)

def inputImage(f): 
    file = f 
    image = cv2.imread(file) # Load the input image using `cv2.imread()`.
    return image 

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    roundAngle = round(angle, 1) 
    if (a[1] == b[1]): 
        if (a[0]>b[0]): 
            if (c[1]>a[1]): 
                return roundAngle
            else: 
                return -roundAngle 
        else: 
            if (c[1]<a[1]): 
                return roundAngle
            else: 
                return -roundAngle
    elif (a[0] == b[0]): 
        if (a[1]>b[1]): 
            if (c[0]>a[0]): 
                return roundAngle
            else: 
                return -roundAngle
        else: 
            if (c[0]<a[0]): 
                return roundAngle
            else: 
                return -roundAngle
    else: 
        slope = (b[1] - a[1]) / (b[0] - a[0])
        equation = (slope * c[0]) + (-slope*a[0] + a[1]) 
        yvalue_g = c[1] < equation 
        if (b[0]>a[0] and b[1]>a[1]): # Quadrant I 
            if (yvalue_g): 
                return roundAngle 
            else: 
                return -roundAngle
        elif (b[0]<a[0] and b[1]>a[1]): # Quadrant II 
            if (not yvalue_g): 
                return roundAngle 
            else: 
                return -roundAngle
        elif (b[0]<a[0] and b[1]<a[1]): # Quadrant III 
            if (not yvalue_g): 
                return roundAngle 
            else: 
                return -roundAngle
        elif (b[0]>a[0] and b[1]<a[1]): # Quadrant IV
            if (yvalue_g): 
                return roundAngle 
            else: 
                return -roundAngle

        # slope = (b[1] - a[1]) / (b[0] - a[0])
        # equation = (slope * c[0]) + (-slope*a[0] + a[1]) 
        # posneg = (c[1]-equation)/abs(c[1]-equation)
        # return posneg * round(angle, 1)

#  0. nose 
# 11. left_shoulder 
# bisection 
# 12. right_shoulder 
# 13. left_elbow 
# 14. right_elbow 
# 15. left_wrist 
# 16. right_wrist
# 23. left_hip 
# 24. right_hip 
# 25. left_knee 
# 26. right_knee 
# 27. left_ankle 
# 28. right_ankle 
# 29. left_heel 
# 30. right_heel 
# 31. left_foot_index
# 32. right_foot_index 

# 23, 11, 13 
# 24, 12, 14 
# 11, 13, 15 
# 12, 14, 16
# 13, 15, 17 
# 14, 16, 18 
# 11, 23, 25 
# 12, 24, 26 
# 23, 25, 27
# 24, 26, 28 
# 25, 27, 31 
# 26, 28, 32
# 29, 31, 27
# 30, 32, 28 

def resultsLandmarks(results):
    try:
        i = 0
        listResults = [] 
        while (i < len(landmarks)): 
            results.pose_landmarks
            if (results.pose_landmarks.landmark[landmarks[i]].x < 0 or results.pose_landmarks.landmark[landmarks[i]].x > 1 or results.pose_landmarks.landmark[landmarks[i]].y < 0 or results.pose_landmarks.landmark[landmarks[i]].y > 1):
                listResults.append(None)  
            else: 
                listResults.append(results.pose_landmarks.landmark[landmarks[i]]) 
            i+=1 
        # print("listResults", listResults)
        return listResults 
    except:
        return []

def calculate_image_angle (a, b, c, ref): 
    if (ref[a] is None) or (ref[b] is None) or (ref[c] is None): 
        return None 
    return calculate_angle((ref[a].x, ref[a].y), (ref[b].x, ref[b].y), (ref[c].x , ref[c].y)) 
    # results.pose_landmarks.landmark[landmarks[a]].x 

def getImageAngles(f): 
    image = f 
    with mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=True, min_detection_confidence=0.5) as pose:
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    res = resultsLandmarks(results)
    # print("res", res)

    if len(res) > 0:
        videoAngles = []    
        videoAngles.append(calculate_image_angle(23, 11, 13, res)) #left shoulder 
        videoAngles.append(calculate_image_angle(24, 12, 14, res)) #right shoulder
        videoAngles.append(calculate_image_angle(11, 13, 15, res)) #left elbow 
        videoAngles.append(calculate_image_angle(12, 14, 16, res)) #right elbow 
        videoAngles.append(calculate_image_angle(13, 15, 17, res)) #left wrist 
        videoAngles.append(calculate_image_angle(14, 16, 18, res)) #right wrist 
        videoAngles.append(calculate_image_angle(11, 23, 25, res)) #left leg lift 
        videoAngles.append(calculate_image_angle(12, 24, 26, res)) #right leg lift 
        videoAngles.append(calculate_image_angle(23, 25, 27, res)) #left knee 
        videoAngles.append(calculate_image_angle(24, 26, 28, res)) #right knee 
        videoAngles.append(calculate_image_angle(25, 27, 31, res)) #left shin ankle toes 
        videoAngles.append(calculate_image_angle(26, 28, 32, res)) #right shin ankle toes 
        return videoAngles
    return None

def getVideoAngles(v): # v is a string in the form of '.mp4'
    cap = cv2.VideoCapture(v) # Use video file 
    frameAngles = [] 
    while(cap.isOpened()): 
        ret, frame=cap.read() 
        if ret is True: 
            frameAngles.append(getImageAngles(frame))

        else: 
            # print("Stream disconnected")
            cap.release()
            break  
    return frameAngles 

def imageScore(originalAngles, userAngles): 
    i = 0 
    totalPercentage = 0 
    calculatedAngles = 0 
    while (i < len(originalAngles)): 
        if (originalAngles[i] is not None): 
            calculatedAngles += 1 
        if (userAngles[i] is not None) and (originalAngles[i] is not None): 
            # print(userAngles[i], originalAngles[i])
            diff = (userAngles[i] - originalAngles[i])
            percentage = diff/originalAngles[i] 
            totalPercentage += percentage 
        i+=1
    if calculatedAngles == 0:
        return 0
    score = totalPercentage/calculatedAngles
    if score < 0:
        return 0
    return score 



