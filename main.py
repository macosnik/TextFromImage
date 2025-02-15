from image_utils import *
import time

start = time.time()

# blank1.png
image = load('test.jpg')
image = compression(image, 2560, 1600)
save(image, 'output.bmp')

print(f"Код завершился за: {round(time.time() - start, 3)} секунды")
