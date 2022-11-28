from picamera import PiCamera
import time
import cv2

camera=PiCamera()
camera.resolution = (640,640)
camera.vflip=True

j=0
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame=cap.read()
    print(ret)
    if ret==False: break
    frame=cv2.flip(frame, 1)
    j=j+1
    print("foto")
    if j==10:
        break

#camera.start_recording()
#time.sleep(3)
#camera.stop_recording()
