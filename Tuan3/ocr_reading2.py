import pytesseract
import cv2

image = cv2.imread("data/bctc2019.jpg")
base_image = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
_,thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,50))
dilate = cv2.dilate(thresh, kernal, iterations=1)
cv2.imwrite("temp/bctc2019_sample.png", dilate)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    if h > 200 and w > 250:
        roi = base_image[y:y+h, x:x+w]
        cv2.rectangle(image, (x,y), (x+w, y+h),(36, 255, 12), 2)
cv2.imwrite("temp/sample_boxes.png", image)
orc_result_new = pytesseract.image_to_string(roi)
print(orc_result_new)