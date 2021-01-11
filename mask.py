import cv2
import numpy as np
# 색상 범위 설정

lower_blue = (0, 80, 80)

upper_blue = (140, 255, 255)

# 이미지 파일을 읽어온다

img = cv2.imread('./img/test.png')
# print(img.shape)
mask = np.zeros(img.shape[:2], dtype="uint8")
# print(img)

# BGR to HSV 변환

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 색상 범위를 제한하여 mask 생성

img_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)

# 원본 이미지를 가지고 Object 추출 이미지로 생성

img_result = cv2.bitwise_and(img, img, mask=img_mask)

# 결과 이미지 생성

cv2.imshow('original', img)
cv2.imshow('mask', img_result)
cv2.waitKey()