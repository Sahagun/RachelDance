import cv2 
from PIL import Image, ImageTk 
import tkinter as tk 

def update(): #recursive function 
    ret,frame = cap.read() # takes frame from webcame and gives it to another function and processes it 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img_tk = ImageTk.PhotoImage(image=img) #image displayed in tkinter 
    lbl_video.img_tk = img_tk # updating
    lbl_video.configure(image=img_tk) 
    lbl_video.after(10, update)  

cap = cv2.VideoCapture(0) # display what you would see in a camera right now 

root = tk.Tk() 
root.title("Video Feed in TKinter")
lbl_video = tk.Label(root)
lbl_video.pack() 
update() 

root.mainloop() 
cap.release() 