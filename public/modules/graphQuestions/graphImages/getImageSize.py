# from PIL import Image

# im = Image.open("./interact/line_interact_01_americanCrabsCaught.jpg")
# print (im.size)

import cv2

img = cv2.imread("./interact/line_interact_01_americanCrabsCaught.png",1)
# imgSize = cv2.GetSize("./interact/line_interact_01_americanCrabsCaught.png",1)
# Returns a tuple of the amount of rows, column and channels
# Slicing the tuple to the first two values
imgSize = img.shape[:2]
print (img)
print (imgSize)
# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
