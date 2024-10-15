import cv2 # OpenCV library for image processing. 
import mediapipe as mp # MediaPipe library for various computer vision tasks. 

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


mpPose = mp.solutions.pose # MediaPipe's pose estimation solution. 
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils # Utility functions for drawing landmarks and connections. 
mp_drawing = mp.solutions.drawing_utils
pose_connections = mp.solutions.pose.POSE_CONNECTIONS


cap = cv2.VideoCapture(0) # display what you would see in a camera right now 

frame_width = 640
frame_height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

pose_connections = mp.solutions.pose.POSE_CONNECTIONS


def draw_landmarks(image, landmarksZ, connections=pose_connections):
    # Convert the image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Draw landmarks on the image
    if landmarksZ.pose_landmarks and landmarksZ.pose_landmarks.landmark:
        for landmark in landmarksZ.pose_landmarks.landmark:
        # if landmarks.pose_landmarks:
        #     for landmark in landmarks.pose_landmarks:
                # print("landmark",landmark)
          # if landmark:
            print("landmark:", landmark)
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 5, (0, 255, 0), 5)

    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    return image_bgr

def get_landmarks(image): 
    global mpPose
    with mpPose.Pose(static_image_mode=False, model_complexity=0, enable_segmentation=True, min_detection_confidence=0.5) as pose:
        return pose.process(image)

print("Start Video")


with mpPose.Pose(static_image_mode=False, model_complexity=0, enable_segmentation=True, min_detection_confidence=0.5) as pose:
    while cap.isOpened():
        print("loop")
        ret, camera_frame = cap.read() # WebCam
        

        print("flip")
        camera_frame = cv2.flip(camera_frame, 1)

        if not ret:
            cv2.waitKey()
            break

        print("process")
        landmarks = pose.process(camera_frame)
        print("landmarks", landmarks)

        if landmarks:
            draw_landmarks(camera_frame, landmarks)

        cv2.imshow('Video', camera_frame)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

exit()
