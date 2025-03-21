from neural_network import TwoLayersNeuralNetwork
from image_utils import Image

symbols_lib = ["0", "1", "2"]

image = Image('DataCenter/tests/image_3.bmp')
arr = image.zero_to_one_list()

network = TwoLayersNeuralNetwork(model_settings="numbers_model_parameters.txt")

result = network.forward(arr)

max_value = max(result)
max_index = result.index(max_value)
max_value = round(max_value, 2)

print(f"Символ: {symbols_lib[max_index]}, Вероятность: {int(max_value * 100)}%")

