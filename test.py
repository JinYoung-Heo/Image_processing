import cv2
import numpy as np

# Load image, grayscale, Otsu's threshold
rawImage = cv2.imread('./img/test.png')
image = cv2.imread('./img/test.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Everyone converts to grayscale because many functions expect grayscale
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
#hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
#hsv = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
h, s, v = cv2.split(hsv)
'''for i in range(len(v)) : # 평균치로 비교
    s = 0
    length = len(v[i])
    for j in range(length) :
        s += v[i][j]
    average = int(s/length)
    if average < 10 :
        v[i] = 0'''
for i in range(len(v)) : # 명도를 컨트롤 해주면 됨
    count = 0
    length = len(v[i])
    for j in range(length) :
        if v[i][j] > 180 : # 기준 명도. 얘를 주로 컨트롤 하면 됨.
            count += 1
    if count < 15 : # 5~10 일때 미세하게 걸러줌
        v[i] = 0
hsv[:,:,2] = v
hsv2bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) 
hsv2gray = cv2.cvtColor(hsv2bgr, cv2.COLOR_BGR2GRAY)
#orange = cv2.bitwise_and(hsv, hsv, mask = h)

thresh = cv2.threshold(hsv2gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find circles with HoughCircles
circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, minDist=150, param1=200, param2=18, minRadius=10) 
# 위치값임.
# 여긴 thresh 넣음(원 잘 찾기위해)
#print(circles)
#print(len(circles[0])) # The number of circles
# Draw circles
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x,y,r) in circles:
        cv2.circle(image, (x,y), r, (36,255,12), 3) 
a = circles[0][0]
b = circles[0][1]
r = circles[0][2]
for x in range(100) :
    for y in range(100) :
        if (x-a)(x-a) + (y-b)(y-b) <= r*r :
            # TODO: 여기에 해당하는 픽셀을 찾고 그 픽셀의 hsv값 구해오기
            pass

# (이미지, 원 중심, 반지름, 원의 색, 선 굵기) 여긴 thresh 대신 image? thresh로 알아낸 위치보고 image에 그림만 그려줄거니까

#cv2.imshow('thresh', thresh)
cv2.imshow('image', rawImage)
cv2.imshow('hsv', hsv2bgr)
#cv2.imshow('thresh', thresh)
cv2.imshow('detected', image)
cv2.waitKey()