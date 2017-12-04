from imutils import contours
import numpy as np
import imutils
import cv2

menuItems = ['Corn Tortilla', 'Flour Tortilla','Goody-Goody Tortilla','Ju-Ju Tortilla','Sweet Lucy Tortilla','Peezler Tortilla','Bowl','Tortilla Fritos', 'Add Rice','Add Black Beans',
    'House Made Chorizo','Braised Beef Brisket','Roasted Pollo','Pulled Pork','Shrimp Ceviche','Thai Chili Tofu','Roasted Portobellos','BBQ Pulled Jackfruit','Ghose Pepper Marinated Steak',
    'Special Protein of the Month','Lettuce','Tomatoes','Cilantro+Onions','Jicama+Cabbage Slaw','Red Cabbage','Pickled Red Onions','Queso Fresco','Middlefield Smoked Cheddar','Chihuahua',
    'Corn Salsa w/ Tomatoes+Peppers+Onions','Pineapple Salsa w/ Tomatoes+Pepper+Onions','Salsa Verde','Salsa Roja','Chipotle Crema','Chipotle Honey','Mexican Chimichuri','Cilantro/Lime Aioli',
    'Habenero/Mango BBQ','Condado Secret Taco Sauce','Ghost Pepper']
    
menuSides = ['Rice','Black Beans','Picked Jalapenos','Tradional Gauc', 'Sour Cream','Bacon Refried Beans']

tacoone = []
tacotwo = []
sides = []

answers = cv2.imread('./imgs/answer.jpg')
answersgray = cv2.cvtColor(answers, cv2.COLOR_BGR2GRAY)
answersblurred = cv2.GaussianBlur(answersgray, (5, 5), 0)

answersthresh = cv2.threshold(answersblurred, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

image = cv2.imread('./imgs/newuncropped.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

thresh = cv2.threshold(blurred, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# find contours in the blank thresholded image, then initialize
# the list of contours that correspond to fillable bubbles
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

	# in order to label the contour as a bubble, region
	# should be sufficiently wide, sufficiently tall, and
	# have an aspect ratio approximately equal to 1
	if w >= 35 and h >= 35 and w <= 46 and h <= 46 and ar >= 0.95 and ar <= 1.05:
		questionCnts.append(c)

cv2.drawContours(image, questionCnts, -1, (0,255,0), 3)
cv2.imwrite('./imgs/test.jpg', image)

#sort bubbles from top to bottom,we do not know how they are listed horizontally
questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]

bubbles = 0

dif = len(menuItems)*2

# loop through bubble contours
for (i, c) in enumerate(questionCnts):
	# draw bubbles onto filled in sheet one at a time
	mask = np.zeros(answersthresh.shape, dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1)
	
	# compute the total number of filled in pixels inside bounding bubble
	mask = cv2.bitwise_and(answersthresh, answersthresh, mask=mask)
	total = cv2.countNonZero(mask)
	
	# logic to discern if bubbles are to the left or right, and applying
	# the menu items from each loaction to the respective taco
	print(total)
	if total > 750:
		if (i+1) < dif:
			if i % 2 == 0 or i == 0:
				if questionCnts[i][0][0][0] < questionCnts[i+1][0][0][0]:
					if i == 0:
						tacoone.append(menuItems[i])
					else:
						tacoone.append(menuItems[int(i/2)])
				else:
					if i == 0:
						tacotwo.append(menuItems[i])
					else:
						tacotwo.append(menuItems[int(i/2)])
			else:
				if questionCnts[i][0][0][0] < questionCnts[i-1][0][0][0]:
					if i == 1:
						tacoone.append(menuItems[(i-1)])
					else:
						tacoone.append(menuItems[int((i-1)/2)])
				else:
					if i == 1:	
						tacotwo.append(menuItems[(i-1)])
					else:
						tacotwo.append(menuItems[int((i-1)/2)])
		else:
			if i % 2 == 0:
				if questionCnts[i][0][0][0] < questionCnts[i+1][0][0][0]:
					sides.append(menuSides[i-dif])
				else:
					sides.append(menuSides[i-dif]+1)
			else:
				if questionCnts[i][0][0][0] < questionCnts[i-1][0][0][0]:
					sides.append(menuSides[i-dif-1])
				else:
					sides.append(menuSides[i-dif])
			
print(tacoone)
print(tacotwo)
print(sides)

