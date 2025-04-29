import pytesseract
from PIL import Image

img_file = "data/bctc2019.jpg"
no_noise = "temp/no_noise.jpg"
img = Image.open(img_file)
ocr_result = pytesseract.image_to_string(img)
print(ocr_result)