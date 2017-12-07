import numpy as np
import cv2

img = cv2.imread('./imgs/answer2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,127,255,1)

_,contours,h = cv2.findContours(thresh,1,2)


# print "countours: ", contours

i = 0
for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)

    if len(approx)==4:
        x,y,w,h = cv2.boundingRect(cnt)
        if w > 80 and h > 40:
            if i < 10:
                ROI=img[y:y+h, x:x+w]
                cv2.imwrite("cropped" + str(i) +".jpg", ROI)

            print "square"
            print "countours: ", [cnt]
            cv2.drawContours(img,[cnt],0,255,-1)
            i = i+1

cv2.imwrite('testing.png', img)

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 800, 1600)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
