import cv2
from matplotlib import pyplot as plt
def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)
    if len(im_data.shape) == 3:
        height, width, depth = im_data.shape  # Ảnh màu (RGB)
    else:
        height, width = im_data.shape  # Ảnh xám (grayscale)
        depth = 1  # Gán giá trị mặc định cho ảnh xám

    #what size does the figure need to be in inches to fit the image?
    figsize = width/float(dpi), height/float(dpi)

    #create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    #hide spines, ticks, etc.
    ax.axis('off')

    #display the image
    ax.imshow(im_data, cmap='gray')
    plt.show()
new = cv2.imread("Tuan3/data/bctcnghieng.jpg")
import numpy as np
def getSkewAngle(cvImage) -> float:
    #prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #Apply dilate to merge text into meaningful lines/paragraphs
    #Use larger kernel on X axis to merge characters into single line, canceling out any spaces
    #But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    #Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)
    
    #find largest contour and surround in min area box
    largestContour = contours[0]
    print(len(contours))
    minAraRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("Tuan3/temp/boxes.jpg", newImage)
    #determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAraRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle
#rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags = cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage
#deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)
fixed = deskew(new)
cv2.imwrite("Tuan3/temp/rolated_fixed.jpg", fixed)
display("Tuan3/temp/rolated_fixed.jpg")
    

    


