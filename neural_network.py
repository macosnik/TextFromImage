import random

def sigmoid(i):
    return 1 / (2.718281828459045 ** (- i) + 1)

def sigmoid_derivative(i):
    return (1 - i) * i

def exit_nums(arr):
    return_arr = []
    e_sum = []

    for i in arr:
        e_sum.append(2.718281828459045 ** i)

    e_sum = sum(e_sum)

    for i in arr:
        return_arr.append(2.718281828459045 ** i / e_sum)

    return return_arr

def __calculate_global_error__(network, lib, symbols_lib):
    global_err = 0

    for arr, symbol in lib:
        output = network.forward(arr)
        target = [0] * len(symbols_lib)
        target[symbols_lib.index(symbol)] = 1

        for i in range(network.outputs_size):
            global_err += (output[i] - target[i]) ** 2

    average_error = global_err / len(lib)
    print(f"Глобальная ошибка: {round(average_error, 4)}")

class TwoLayersNeuralNetwork:
    def __init__(self, inputs_size=None, hidden_1_size=None, hidden_2_size=None, outputs_size=None, model_settings=None):
        self.weights_1 = []
        self.weights_2 = []
        self.weights_3 = []
        self.bias_1 = []
        self.bias_2 = []
        self.bias_3 = []
        self.hidden_inputs1 = []
        self.hidden_outputs1 = []
        self.hidden_inputs2 = []
        self.hidden_outputs2 = []
        self.output_inputs = []
        self.output = []

        if model_settings is None:
            self.inputs_size = inputs_size
            self.hidden_1_size = hidden_1_size
            self.hidden_2_size = hidden_2_size
            self.outputs_size = outputs_size

            for _ in range(inputs_size):
                part = []
                for _ in range(hidden_1_size):
                    part.append(random.uniform(-0.5, 0.5))
                self.weights_1.append(part)

            for _ in range(hidden_1_size):
                part = []
                for _ in range(hidden_2_size):
                    part.append(random.uniform(-0.5, 0.5))
                self.weights_2.append(part)

            for _ in range(hidden_2_size):
                part = []
                for _ in range(outputs_size):
                    part.append(random.uniform(-0.5, 0.5))
                self.weights_3.append(part)

            for _ in range(hidden_1_size):
                self.bias_1.append(random.uniform(-0.1, 0.1))
            for _ in range(hidden_2_size):
                self.bias_2.append(random.uniform(-0.1, 0.1))
            for _ in range(outputs_size):
                self.bias_3.append(random.uniform(-0.1, 0.1))

        else:
            with open(model_settings, "r") as file:
                arr = file.read().split(' ')
                arr = arr[:len(arr) - 1]

            self.inputs_size = int(arr[1])
            self.hidden_1_size = int(arr[2])
            self.hidden_2_size = int(arr[3])
            self.outputs_size = int(arr[4])

            arr = arr[5:]

            for input_index in range(self.inputs_size):
                part = []
                for hidden_index in range(self.hidden_1_size):
                    part.append(float(arr[input_index * hidden_index + hidden_index]))
                self.weights_1.append(part)

            for hidden_1_index in range(self.hidden_1_size):
                part = []
                for hidden_2_index in range(self.hidden_2_size):
                    part.append(float(arr[hidden_1_index * hidden_2_index + hidden_2_index]))
                self.weights_2.append(part)

            for hidden_2_index in range(self.hidden_2_size):
                part = []
                for output_index in range(self.outputs_size):
                    part.append(float(arr[hidden_2_index * output_index + output_index]))
                self.weights_3.append(part)

            print(len(self.weights_1), len(self.weights_1[0]))
            print(len(self.weights_2), len(self.weights_2[0]))
            print(len(self.weights_3), len(self.weights_3[0]))

            # arr = arr[len(self.inputs_size) * 1:]

            # for bias in range

    def forward(self, image):
        self.hidden_inputs1 = []
        self.hidden_outputs1 = []

        for neuron_index in range(self.hidden_1_size):
            weighted_sum = 0
            for input_index in range(self.inputs_size):
                weighted_sum += image[input_index] * self.weights_1[input_index][neuron_index]
            weighted_sum += self.bias_1[neuron_index]
            self.hidden_inputs1.append(weighted_sum)

        for value in self.hidden_inputs1:
            self.hidden_outputs1.append(sigmoid(value))

        self.hidden_inputs2 = []
        self.hidden_outputs2 = []

        for neuron_index in range(self.hidden_2_size):
            weighted_sum = 0
            for input_index in range(self.hidden_1_size):
                weighted_sum += self.hidden_outputs1[input_index] * self.weights_2[input_index][neuron_index]
            weighted_sum += self.bias_2[neuron_index]
            self.hidden_inputs2.append(weighted_sum)

        for value in self.hidden_inputs2:
            self.hidden_outputs2.append(sigmoid(value))
        
        self.output_inputs = []
        self.output = []

        for neuron_index in range(self.outputs_size):
            weighted_sum = 0
            for input_index in range(self.hidden_2_size):
                weighted_sum += self.hidden_outputs2[input_index] * self.weights_3[input_index][neuron_index]
            weighted_sum += self.bias_3[neuron_index]
            self.output_inputs.append(weighted_sum)

        self.output = exit_nums(self.output_inputs)

        return self.output

    def train(self, image, true_answer, speed=0.1):
        self.forward(image)

        output_error = []

        for i in range(self.outputs_size):
            output_error.append(self.output[i] - true_answer[i])

        delta_3 = output_error
        gradient_weights_3 = []
        gradient_bias_3 = []

        for hidden_2_index in range(self.hidden_2_size):
            part = []
            for output_index in range(self.outputs_size):
                part.append(self.hidden_outputs2[hidden_2_index] * delta_3[output_index] * speed)
            gradient_weights_3.append(part)

        for output_index in range(self.outputs_size):
            gradient_bias_3.append(delta_3[output_index] * speed)

        delta_2 = []
        gradient_weights_2 = []
        gradient_bias_2 = []

        for hidden_2_index in range(self.hidden_2_size):
            error = 0
            for output_index in range(self.outputs_size):
                error += delta_3[output_index] * self.weights_3[hidden_2_index][output_index]
            derivative = sigmoid_derivative(self.hidden_outputs2[hidden_2_index])
            delta_2.append(error * derivative)

        for hidden_1_index in range(self.hidden_1_size):
            part = []
            for hidden_2_index in range(self.hidden_2_size):
                part.append(self.hidden_outputs1[hidden_1_index] * delta_2[hidden_2_index] * speed)
            gradient_weights_2.append(part)

        for hidden_2_index in range(self.hidden_2_size):
            gradient_bias_2.append(delta_2[hidden_2_index] * speed)

        delta_1 = []
        gradient_weights_1 = []
        gradient_bias_1 = []

        for hidden_1_index in range(self.hidden_1_size):
            error = 0
            for hidden_2_index in range(self.hidden_2_size):
                error += delta_2[hidden_2_index] * self.weights_2[hidden_1_index][hidden_2_index]
            derivative = sigmoid_derivative(self.hidden_outputs1[hidden_1_index])
            delta_1.append(error * derivative)

        for input_index in range(self.inputs_size):
            part = []
            for hidden_1_index in range(self.hidden_1_size):
                part.append(image[input_index] * delta_1[hidden_1_index] * speed)
            gradient_weights_1.append(part)

        for hidden_1_index in range(self.hidden_1_size):
            gradient_bias_1.append(delta_1[hidden_1_index] * speed)

        for input_index in range(self.inputs_size):
            for hidden_1_index in range(self.hidden_1_size):
                self.weights_1[input_index][hidden_1_index] -= gradient_weights_1[input_index][hidden_1_index]

        for hidden_1_index in range(self.hidden_1_size):
            for hidden_2_index in range(self.hidden_2_size):
                self.weights_2[hidden_1_index][hidden_2_index] -= gradient_weights_2[hidden_1_index][hidden_2_index]

        for hidden_2_index in range(self.hidden_2_size):
            for output_index in range(self.outputs_size):
                self.weights_3[hidden_2_index][output_index] -= gradient_weights_3[hidden_2_index][output_index]

        for hidden_1_index in range(self.hidden_1_size):
            self.bias_1[hidden_1_index] -= gradient_bias_1[hidden_1_index]

        for hidden_2_index in range(self.hidden_2_size):
            self.bias_2[hidden_2_index] -= gradient_bias_2[hidden_2_index]

        for output_index in range(self.outputs_size):
            self.bias_3[output_index] -= gradient_bias_3[output_index]

    def calculate_global_error(self, lib, symbols_lib):
        __calculate_global_error__(self, lib, symbols_lib)

    def save_model(self, name_file):
        arr = ['2layers',
               self.inputs_size,
               self.hidden_1_size,
               self.hidden_2_size,
               self.outputs_size]

        for weights in self.weights_1:
            for param in weights:
                arr.append(param)

        for weights in self.weights_2:
            for param in weights:
                arr.append(param)

        for weights in self.weights_3:
            for param in weights:
                arr.append(param)

        for bias in self.bias_1:
            arr.append(bias)
        for bias in self.bias_2:
            arr.append(bias)
        for bias in self.bias_3:
            arr.append(bias)

        output_text = ""

        for param in arr:
            output_text += str(param)
            output_text += " "

        with open(name_file, "w") as file:
            file.write(output_text)



