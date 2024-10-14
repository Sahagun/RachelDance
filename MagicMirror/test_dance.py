from tkinter import NW, Tk, Canvas, PhotoImage
import cv2 
import numpy as np

def photo_image(img):
    h, w = img.shape[:2]
    data = f'P6 {w} {h} 255 '.encode() + img[..., ::-1].tobytes()
    return PhotoImage(width=w, height=h, data=data, format='PPM')

def update():
    ret1, img1 = cap1.read()
    # ret2, img2 = cap2.read()
    if ret1:
        photo = photo_image(img1)
        # photo = photo_image(np.hstack((img1, img2)))
        canvas.create_image(0, 0, image=photo, anchor=NW)
        canvas.image = photo
    root.after(15, update)

root = Tk()
root.title("Video")
cap1 = cv2.VideoCapture("/Users/terrorbyte/Documents/GitHub/MagicMirror/image test/Dance.mp4")
# cap1 = cv2.VideoCapture("Dance.mp4")
# cap2 = cv2.VideoCapture("video2.mp4")

canvas = Canvas(root, width=1200, height=700)
canvas.pack()
update()
root.mainloop()
cap1.release()