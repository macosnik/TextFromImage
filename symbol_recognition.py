from neural_network import TwoLayersNeuralNetwork
from image_utils import Image

symbols_lib = ["0", "1", "2"]

network = TwoLayersNeuralNetwork(model_settings="numbers_model_parameters.txt")

image = Image('DataCenter/tests/image_6.bmp').zero_to_one_list()

result = network.forward(image)

print(result)

max_value = max(result)
max_index = result.index(max_value)
max_value = round(max_value, 2)

print(f"Символ: {symbols_lib[max_index]}, Вероятность: {int(max_value * 100)}%")

