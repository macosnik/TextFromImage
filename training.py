from neural_network import TwoLayersNeuralNetwork
from image_utils import Image
import time

image = Image('DataCenter/tests/image_1.bmp')
arr = image.zero_to_one_list()

start_time = time.time()

network = TwoLayersNeuralNetwork(625, 128, 64, 10)
# network.forward(arr)
network.train(arr, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0])

print(time.time() - start_time)



