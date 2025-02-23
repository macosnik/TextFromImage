from neural_network import TwoLayersNeuralNetwork
from image_utils import Image

image = Image('DataCenter/tests/image_1.bmp')
arr = image.zero_to_one_list()

network = TwoLayersNeuralNetwork(625, 128, 64, 10)
network.predict(arr)
