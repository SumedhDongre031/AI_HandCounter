import HandTrackingModule as htm
import cv2
import time
import os

wCam = 640
hCam = 480
pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

path = "finger imgs"
myList = os.listdir(path)
print(myList)
overlayList = []
for imgpath in myList:
    image = cv2.imread(f'{path}/{imgpath}')
    #print(f'{path}/{imgpath}')
    overlayList.append(image)

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList)

    if len(lmList) != 0:
        fingers = []


        #thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
                fingers.append(1)
        else:
                fingers.append(0)
        # 4 fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        h,w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]

        cv2.rectangle(img, (15,220), (150,425), (0,255,0), cv2.FILLED)
        cv2.putText(img, str(totalFingers),(40,370),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),15)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime 

    cv2.putText(img, f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("IMAGE",img)
    cv2.waitKey(1)