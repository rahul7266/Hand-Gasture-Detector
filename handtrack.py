import cv2
import mediapipe as mp
import numpy as np
import time
import autopy
import math
import pyautogui
pyautogui.FAILSAFE=False


def mouseMovement(a=0,b=0):
    global sizex,sizey
    try:
        x, y = pyautogui.position()
        if a>0:
            newx = x+10
        elif a<0:
            newx = x-10
        if b>0:
            newy = y-10
        elif b<0:
            newy = y+10

        if(newx>sizex):
            newx=sizex
        if(newy>sizey):
            newy=sizey

        pyautogui.moveTo(newx, newy)

    except Exception as exp:
        pass
        #print ('ERROR in mcontroller.py!!\n\tError:\n\t',exp)


cap=cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
pTime=0
cTime=0

while True:
    sucess,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    imgResize=cv2.resize(img,(800,800))
  #  imgResize=cv2.flip(imgResize,-1)
    results=hands.process(imgRGB)
#   print(results.multi_hand_landmarks)
    lmlist=[]
    if results.multi_hand_landmarks:
          for handlms in results.multi_hand_landmarks:
              for id,lm in enumerate(handlms.landmark):
                 # print(id,lm)
                  h,w,c=imgResize.shape
                  cx,cy= int(lm.x*w),int(lm.y*h)
                  r=[id,cx,cy]
                  lmlist.append(r)
         # print(lmlist)
          cv2.circle(imgResize,(lmlist[8][1],lmlist[8][2]),8,(255,0,255),cv2.FILLED)
          cv2.circle(imgResize,(lmlist[12][1],lmlist[12][2]),8,(255, 0, 255), cv2.FILLED)
          mx,my=(lmlist[8][1]+lmlist[12][1])//2,(lmlist[8][2]+lmlist[12][2])//2
          cv2.circle(imgResize, (mx, my), 8, (255, 0, 255), cv2.FILLED)
          cv2.line(imgResize,(lmlist[8][1],lmlist[8][2]),(lmlist[12][1],lmlist[12][2]),(255,0,0),3)
          dist1=math.dist((lmlist[8][1],lmlist[8][2]),(mx,my))
          dist2 = math.dist((lmlist[12][1], lmlist[12][2]), (mx, my))
          #print(dist1)
          #autopy.mouse.move(lmlist[12][1],lmlist[12][2])
          pyautogui.moveTo(lmlist[8][1],lmlist[8][2],0)
          if dist1<=18:
              cv2.circle(imgResize, (mx, my), 8, (0, 0, 255), cv2.FILLED)
              #autopy.mouse.click()
              pyautogui.leftClick()
             # pyautogui.scroll(50)
          mpDraw.draw_landmarks(imgResize,handlms,mpHands.HAND_CONNECTIONS)
    cTime=time.time()
    FPS=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(imgResize,str((int(FPS))),(10,70),cv2.FONT_HERSHEY_DUPLEX,3,(255,0,255),3)
    
    cv2.imshow("hand",imgResize)
    cv2.waitKey(1)

   