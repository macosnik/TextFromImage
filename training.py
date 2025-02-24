from neural_network import TwoLayersNeuralNetwork
from image_utils import Image
import os

symbols_lib = ["0", "1"]
lib = []

for symbol in symbols_lib:
    for num_image in range(len(os.listdir(f'DataCenter/{symbol}'))):
        image = Image(f'DataCenter/{symbol}/image_{num_image + 1}.bmp')
        arr = image.zero_to_one_list()
        lib.append((arr, symbol))

network = TwoLayersNeuralNetwork(625, 256, 128, 2)

for epoch in range(len(symbols_lib)):
    network.train(image_0[epoch], [1, 0])

#
# image = Image(f'DataCenter/tests/image_1.bmp')
# arr = image.zero_to_one_list()
# print(network.forward(arr))
#
# image = Image(f'DataCenter/tests/image_2.bmp')
# arr = image.zero_to_one_list()
# print(network.forward(arr))






