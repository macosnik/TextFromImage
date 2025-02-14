from image_utils import *
import time

start = time.time()

# blank1.png
image = load('picture.jpeg')
save(image, 'picture_output.bmp')

print(f"Код завершился за: {round(time.time() - start, 3)} секунды")
