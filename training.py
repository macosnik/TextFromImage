from neural_network import TwoLayersNeuralNetwork
from image_utils import Image
import os

symbols_lib = ["0", "1"]
lib = []

inputs_size = 625
hidden_1_size = 256
hidden_2_size = 128
outputs_size = len(symbols_lib)

for symbol in symbols_lib:
    for num_image in range(len(os.listdir(f'DataCenter/{symbol}'))):
        image = Image(f'DataCenter/{symbol}/image_{num_image + 1}.bmp')
        arr = image.zero_to_one_list()
        lib.append((arr, symbol))

network = TwoLayersNeuralNetwork(inputs_size, hidden_1_size, hidden_2_size, outputs_size)

for epoch in range(len(lib)):
    true_answer = [0] * len(symbols_lib)
    true_answer[symbols_lib.index(lib[epoch][1])] = 1

    network.train(lib[epoch][0], true_answer)

    if epoch % 100 == 0:
        total_error = 0

        for arr, symbol in lib:
            output = network.forward(arr)
            target = [0] * len(symbols_lib)
            target[symbols_lib.index(symbol)] = 1

            for i in range(outputs_size):
                error = output[i] - target[i]
                squared_error = error ** 2
                total_error += squared_error

        average_error = total_error / len(lib)
        print(f"Эпоха {epoch}, Средняя ошибка: {average_error}")

