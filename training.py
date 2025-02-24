from neural_network import TwoLayersNeuralNetwork
from image_utils import Image
import os, time, random

symbols_lib = ["0", "1"]
lib = []

inputs_size = 625
hidden_1_size = 16
hidden_2_size = 16
outputs_size = len(symbols_lib)

for symbol in symbols_lib:
    for num_image in range(len(os.listdir(f'DataCenter/{symbol}'))):
        image = Image(f'DataCenter/{symbol}/image_{num_image + 1}.bmp')
        arr = image.zero_to_one_list()
        lib.append((arr, symbol))

random.shuffle(lib)

network = TwoLayersNeuralNetwork(inputs_size, hidden_1_size, hidden_2_size, outputs_size)

start_time = time.time()

for epoch in range(len(lib)):
    true_answer = [0] * len(symbols_lib)
    true_answer[symbols_lib.index(lib[epoch][1])] = 1

    network.train(lib[epoch][0], true_answer)

print(round(time.time() - start_time, 3))
start_time = time.time()

global_err = 0

for arr, symbol in lib:
    output = network.forward(arr)
    target = [0] * len(symbols_lib)
    target[symbols_lib.index(symbol)] = 1

    for i in range(outputs_size):
        global_err += (output[i] - target[i]) ** 2

average_error = global_err / len(lib)
print(f"Глобальная ошибка: {average_error}")

print(round(time.time() - start_time, 3))

print(network.forward(Image('DataCenter/tests/image_1.bmp').zero_to_one_list()))
print(network.forward(Image('DataCenter/tests/image_2.bmp').zero_to_one_list()))
