import cv2
import numpy as np

img = cv2.imread('./img/CameronDiaz.jpg')
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#threshold를 이용하여 binary image로 변환
ret, th1 = cv2.threshold(imgray,100,255,cv2.THRESH_BINARY) # global threshold라 함.

th2 = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,2)
th3 = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2) # 젤 나은듯

#contours는 point의 list형태. 예제에서는 사각형이 하나의 contours line을 구성하기 때문에 len(contours) = 1. 값은 사각형의 꼭지점 좌표.
#hierachy는 contours line의 계층 구조
#contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#image = cv2.drawContours(img, contours, -1, (0,255,0), 3) #컨투어는 좌표고 그 위치에 그림 그리는거 인듯 - 정확

titles = ['Original','Global','Mean','Gaussian']
images = [imgray,th1,th2,th3]

for i in range(len(titles)) :
    cv2.imshow(titles[i], images[i])
cv2.waitKey(0)
cv2.destroyAllWindows()