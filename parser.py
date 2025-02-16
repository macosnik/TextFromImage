from image_utils import *
import time

start = time.time()

image = load('test.jpg')
image = simplify(image)
# image = compression(image, 180, 180)
# image = draw_line(image, 100, 0, 1000, 500, (255, 0, 0))
save(image, 'output.bmp')

print(f"Код завершился за: {round(time.time() - start, 3)} секунды")
