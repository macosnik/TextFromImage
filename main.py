from image_utils import *
import time

start = time.time()

# blank1.png
image = load('picture.jpeg')

print(round(time.time() - start, 3))

print(image)