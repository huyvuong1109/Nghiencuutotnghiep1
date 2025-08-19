
from PIL import Image


im_file = "Tuan3/data/anh1.png"
im = Image.open(im_file)
# print(im.size)
# im.show()
im.save("Tuần 3/temp/anh1.png")
