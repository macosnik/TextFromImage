from neural_network import TwoLayersNeuralNetwork
from image_utils import Image

image = Image('DataCenter/tests/image_1.bmp')
arr = image.zero_to_one_list()

print(arr)

network = TwoLayersNeuralNetwork(625, 16, 16, 10)
network.forward(arr)
