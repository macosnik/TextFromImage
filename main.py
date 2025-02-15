from image_utils import *
import time

start = time.time()

# blank1.png
image = load('test.jpg')
compression(image, 100, 100)
save(image, 'output.bmp')

print(f"Код завершился за: {round(time.time() - start, 3)} секунды")
