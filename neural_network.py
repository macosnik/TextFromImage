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
        return_arr.append(round(2.718281828459045 ** i / e_sum, 3))

    return return_arr

class NeuralNetwork:
    def __init__(self, inputs, hidden_1, hidden_2, outputs):
        self.inputs = inputs
        self.hidden_1 = hidden_1
        self.hidden_2 = hidden_2
        self.outputs = outputs
        self.weights_1 = []
        self.weights_2 = []
        self.weights_3 = []
        self.bias_1 = []
        self.bias_2 = []
        self.bias_3 = []
        self.hidden_inputs1 = []
        self.hidden_inputs2 = []
        self.output_inputs = []

        for i in range(inputs):
            part = []
            for _ in range(hidden_1):
                part.append(round(random.uniform(-0.5, 0.5), 2))
            self.weights_1.append(part)

        for i in range(hidden_1):
            part = []
            for _ in range(hidden_2):
                part.append(round(random.uniform(-0.5, 0.5), 2))
            self.weights_1.append(part)

        for i in range(hidden_2):
            part = []
            for _ in range(outputs):
                part.append(round(random.uniform(-0.5, 0.5), 2))
            self.weights_1.append(part)

        for _ in range(hidden_1):
            self.bias_1.append(0.0)
        for _ in range(hidden_2):
            self.bias_2.append(0.0)
        for _ in range(outputs):
            self.bias_3.append(0.0)

    def forward(self, arr):
        self.hidden_inputs1 = []

        for neuron_index in range(self.hidden_1):
            weighted_sum = 0

            for input_index in range(self.inputs):
                weighted_sum += arr[input_index] * self.weights_1[input_index][neuron_index]

            weighted_sum += self.bias_1[neuron_index]
            self.hidden_inputs1.append(round(sigmoid(weighted_sum), 2))

        print(self.hidden_inputs1)

        




