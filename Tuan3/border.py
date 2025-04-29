import cv2
from matplotlib import pyplot as plt
image_file = "Tuan3/data/bctc2019.jpg"
img = cv2.imread(image_file)
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
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_image = grayscale(img)
# cv2.imwrite("Tuan3/temp/gray.jpg", gray_image)
# display("Tuan3/temp/gray.jpg")

thresh,im_bw = cv2.threshold(gray_image, 200, 230, cv2.THRESH_BINARY)
cv2.imwrite("Tuan3/temp/bw_image.jpg", im_bw)
#display("Tuan3/temp/bw_image.jpg")
def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)
no_noise = noise_removal(im_bw)
def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return(crop)

no_borders = remove_borders(no_noise)
# cv2.imwrite("Tuan3/temp/no_borders.jpg", no_borders)
# display("Tuan3/temp/no_borders.jpg")

color = [255, 255, 255]
top, bottom, left, right = [150]*4
image_with_border = cv2.copyMakeBorder(no_borders, top, bottom, left, right, cv2.BORDER_CONSTANT, value = color)
cv2.imwrite("Tuan3/temp/image_with_border.jpg", image_with_border)
display("Tuan3/temp/image_with_border.jpg")