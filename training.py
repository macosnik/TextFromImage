from neural_network import TwoLayersNeuralNetwork
from image_utils import Image
import time

image_0 = []
image_1 = []

epochs = 200

for num_image in range(epochs):
    image = Image(f'DataCenter/0/image_{num_image + 1}.bmp')
    arr = image.zero_to_one_list()
    image_0.append(arr)

for num_image in range(epochs):
    image = Image(f'DataCenter/1/image_{num_image + 1}.bmp')
    arr = image.zero_to_one_list()
    image_1.append(arr)

network = TwoLayersNeuralNetwork(625, 128, 64, 2)

for epoch in range(epochs):
    network.train(image_0[epoch], [1, 0])
    network.train(image_1[epoch], [0, 1])

image = Image(f'DataCenter/tests/image_1.bmp')
arr = image.zero_to_one_list()
print(network.forward(arr))

image = Image(f'DataCenter/tests/image_2.bmp')
arr = image.zero_to_one_list()
print(network.forward(arr))






