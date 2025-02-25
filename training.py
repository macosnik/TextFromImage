from neural_network import TwoLayersNeuralNetwork
from image_utils import Image
import os, time, random, sys

def load_animation(char, max_num, now_num):
    animation = "|/-\\"
    idx = now_num % len(animation)
    sys.stdout.write(f'\rЗагрузка символа: {char}: {animation[idx]} {now_num + 1}/{max_num}')
    sys.stdout.flush()

def train_animation(max_num, now_num):
    animation = "|/-\\"
    idx = now_num % len(animation)
    sys.stdout.write(f'\rОбучение: {animation[idx]} {now_num + 1}/{max_num}')
    sys.stdout.flush()

def train():
    len_lib = len(lib)
    for epoch in range(len_lib):
        train_animation(len_lib, epoch)

        true_answer = [0] * len(symbols_lib)
        true_answer[symbols_lib.index(lib[epoch][1])] = 1

        network.train(lib[epoch][0], true_answer)

symbols_lib = ["0", "1", "2"]
lib = []

inputs_size = 625
hidden_1_size = 16
hidden_2_size = 16
outputs_size = len(symbols_lib)

for symbol in symbols_lib:
    num_images = len(os.listdir(f'DataCenter/{symbol}'))
    for num_image in range(len(os.listdir(f'DataCenter/{symbol}'))):
        load_animation(symbol, num_images, num_image)
        image = Image(f'DataCenter/{symbol}/image_{num_image + 1}.bmp')
        arr = image.zero_to_one_list()
        lib.append((arr, symbol))
    print()

random.shuffle(lib)

# network = TwoLayersNeuralNetwork(model_settings="numbers_model_parameters.txt")
network = TwoLayersNeuralNetwork(inputs_size, hidden_1_size, hidden_2_size, outputs_size)

start_time = time.time()

for _ in range(10):
    train()

print()

print(f"Время обучения: {round(time.time() - start_time, 3)}")

network.calculate_global_error(lib, symbols_lib)

print(network.forward(Image('DataCenter/tests/image_1.bmp').zero_to_one_list()))
print(network.forward(Image('DataCenter/tests/image_2.bmp').zero_to_one_list()))
print(network.forward(Image('DataCenter/tests/image_3.bmp').zero_to_one_list()))
print(network.forward(Image('DataCenter/tests/image_4.bmp').zero_to_one_list()))
print(network.forward(Image('DataCenter/tests/image_5.bmp').zero_to_one_list()))
print(network.forward(Image('DataCenter/tests/image_6.bmp').zero_to_one_list()))
print(network.forward(Image('DataCenter/tests/image_7.bmp').zero_to_one_list()))

network.save_model("numbers_model_parameters.txt")

