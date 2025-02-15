from image_utils import *
import time

start = time.time()

image = load('test.bmp')
image = compression(image, 50, 50)
save(image, 'output.bmp')

print(f"Код завершился за: {round(time.time() - start, 3)} секунды")
