import cv2
import numpy as np
import math
from scipy.spatial import distance as dist



# Contour 영역 내에 텍스트 쓰기
# https://github.com/bsdnoobz/opencv-code/blob/master/shape-detect.cpp
def setText(image, brightness, contour):

   fontface = cv2.FONT_HERSHEY_SIMPLEX
   scale = 0.6
   thickness = 2

   size = cv2.getTextSize(brightness, fontface, scale, thickness)
   text_width = size[0][0]
   text_height = size[0][1]

   #x, y, width, height = cv2.boundingRect(contour)
   x_sum, y_sum = (0, 0)
   n_pt = len(contour)
   for i in range(n_pt) :
       x_sum += contour[i][0][0]
       y_sum += contour[i][0][1]
   x = int(x_sum/n_pt)
   y = int(y_sum/n_pt)
   r = math.sqrt( (x - contour[0][0][0])*(x - contour[0][0][0]) + (y - contour[0][0][1])*(y - contour[0][0][1]) )
   pt = (x - int(text_width/2), y - round(r))
   cv2.putText(image, brightness, pt, fontface, scale, (255, 255, 255), thickness, 8)



# 컨투어 내부의 색을 평균내서 red, green, blue 중 어느 색인지 체크
def findBrightness(image, contour):


   mask = np.zeros(image.shape[:2], dtype="uint8") # 1080(행) x 1920(열)의 2차원 배열 만든거. 
   cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1) # 검은 도화지에 그림을 그린거지. 왜 색상이 인자가 안먹히지 3번째 shape이 없어서 그렇네
   mask = cv2.erode(mask, None, iterations=2) # 선 굵기 부식시키는 느낌인듯 - 정확
   #cv2.imshow("afterErode", mask)
   #cv2.waitKey(0)
   mean = cv2.mean(image, mask=mask)[:3] # contour 내 평균 색상 구하는 함수 ㄷㄷ image 가 gray scale이면 명도를 구한다는데? ㄷㄷ
   brightness = int(mean[0])
   
   return str(brightness)

# 원본 이미지 불러오기
image = cv2.imread('./img/test.png')
cv2.imshow("Original", image)

# 이진화
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

# 색검출할 색공간으로 LAB사용
img_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

thresh = cv2.erode(thresh, None, iterations=2)

# 컨투어 검출
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# 컨투어 리스트가 OpenCV 버전에 따라 차이있기 때문에 추가
if len(contours) == 2:
   contours = contours[0]

elif len(contours) == 3:
   contours = contours[1]


# 컨투어 별로 체크
for contour in contours:
   # 컨투어를 그림
   cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

   # 컨투어 내부에 검출된 색을 표시
   brightness = findBrightness(gray, contour)
   setText(image, brightness, contour)

cv2.imshow("Image", image)
cv2.waitKey(0)