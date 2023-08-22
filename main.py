import cv2
import cvzone
import numpy as np
import pickle

cap = cv2.VideoCapture("/home/c1ph3r/TensorFlow_Projects/Parking_space_project/CarParkProject/carPark.mp4")

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)
    
width, height = 107, 48

def checkParkingSpace(imgpro):
    
    space_counter = 0
    
    for pos in posList:
        x, y = pos
        imgCrop = imgpro[y:y+height, x:x+width]
        #cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y+height-3), scale = 1, thickness=2, offset=0, colorR=(0, 0, 255))
        
        if count<900:
            color = (0, 255, 0)
            thickness = 5
            space_counter+=1
        else: 
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        
    cvzone.putTextRect(img, f'Free: {space_counter}/{len(posList)}', (100, 50), scale = 3, thickness=5, offset=20, colorR=(0, 200, 0))

        
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img= cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreashold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    kernel = np.ones((3, 3), np.int8)
    imgMedian = cv2.medianBlur(imgThreashold, 5)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    
    checkParkingSpace(imgDilate)

    #for pos in posList:
        

    cv2.imshow("image", img)
    #cv2.imshow("image blur", imgBlur)
    #cv2.imshow("image Threshold", imgThreashold)
    #cv2.imshow("Image Median", imgMedian)
    #cv2.imshow("image dilate", imgDilate)
    cv2.waitKey(1)