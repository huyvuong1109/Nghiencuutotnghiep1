import cv2
from matplotlib import pyplot as plt
image_file = "Tuan3/data/bctc2019.jpg"
img = cv2.imread(image_file)
def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)
    height, width, depth, = im_data.shape

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

inverted_image = cv2.bitwise_not(img)
cv2.imwrite("Tuan3/data/bctc2019_inverted.jpg", inverted_image)
display("Tuan3/data/bctc2019_inverted.jpg")