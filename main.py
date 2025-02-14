from image_utils import *

# blank1.png
image = load('picture.jpeg')
image = simplify(image)
save(image, 'blank1_output.bmp')
