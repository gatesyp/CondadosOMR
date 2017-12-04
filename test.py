from imutils import contours
import numpy as np
import imutils
import cv2

answers = cv2.imread('./imgs/answer.jpg')
answersgray = cv2.cvtColor(answers, cv2.COLOR_BGR2GRAY)
answersblurred = cv2.GaussianBlur(gray, (5, 5), 0)

answersthresh = cv2.threshold(answersblurred, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

image = cv2.imread('./imgs/newuncropped.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 75)
#binarize image
thresh = cv2.threshold(blurred, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# find contours in the thresholded image, then initialize
# the list of contours that correspond to questions
cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
	cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
questionCnts = []

# loop over the contours
for c in cnts:
    # compute the bounding box of the contour, then use the
    # bounding box to derive the aspect ratio
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)

    # in order to label the contour as a question, region
    # should be sufficiently wide, sufficiently tall, and
    # have an aspect ratio approximately equal to 1
    if w >= 35 and h >= 35 and ar >= 0.95 and ar <= 1.05:
        questionCnts.append(c)

#cv2.drawContours(answers, questionCnts, -1, (0,255,0), 3)

#cv2.namedWindow("output", cv2.WINDOW_NORMAL)
#cv2.imshow("output", answers)
#cv2.waitKey(0)

questionCnts = contours.sort_contours(questionCnts,
    method="top-to-bottom")[0]

bubbles = 0

for (q, i) in enumerate(np.arange(0, len(questionCnts), 2)):
    # sort the contours for the current question from
	# left to right, then initialize the index of the
	# bubbled answer
	cnts = contours.sort_contours(questionCnts[i:i + 2])[0]
	bubbled = None

    # loop over the sorted contours
    for (j, c) in enumerate(cnts):
        # construct a mask that reveals only the current
        # "bubble" for the question
        mask = np.zeros(answersthresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        # apply the mask to the thresholded image, then
        # count the number of non-zero pixels in the
        # bubble area
        mask = cv2.bitwise_and(answersthresh, answersthresh, mask=mask)
        total = cv2.countNonZero(mask)

        # if the current total has a larger number of total
        # non-zero pixels, then we are examining the currently
        # bubbled-in answer
        if total > 200:
            bubbles++

print(bubbles)
