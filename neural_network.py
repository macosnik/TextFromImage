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

class TwoLayersNeuralNetwork:
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
        self.hidden_outputs1 = []
        self.hidden_inputs2 = []
        self.hidden_outputs2 = []
        self.output_inputs = []
        self.output = []

        for i in range(inputs):
            part = []
            for _ in range(hidden_1):
                part.append(random.uniform(-0.5, 0.5))
            self.weights_1.append(part)

        for i in range(hidden_1):
            part = []
            for _ in range(hidden_2):
                part.append(random.uniform(-0.5, 0.5))
            self.weights_2.append(part)

        for i in range(hidden_2):
            part = []
            for _ in range(outputs):
                part.append(random.uniform(-0.5, 0.5))
            self.weights_3.append(part)

        for _ in range(hidden_1):
            self.bias_1.append(0.0)
        for _ in range(hidden_2):
            self.bias_2.append(0.0)
        for _ in range(outputs):
            self.bias_3.append(0.0)

    def predict(self, arr):
        self.hidden_inputs1 = []

        for neuron_index in range(self.hidden_1):
            weighted_sum = 0

            for input_index in range(self.inputs):
                weighted_sum += arr[input_index] * self.weights_1[input_index][neuron_index]

            weighted_sum += self.bias_1[neuron_index]
            self.hidden_inputs1.append(weighted_sum)

        for value in self.hidden_inputs1:
            self.hidden_outputs1.append(sigmoid(value))

        self.hidden_inputs2 = []

        for neuron_index in range(self.hidden_2):
            weighted_sum = 0

            for input_index in range(self.hidden_1):
                weighted_sum += self.hidden_outputs1[input_index] * self.weights_2[input_index][neuron_index]

            weighted_sum += self.bias_2[neuron_index]
            self.hidden_inputs2.append(weighted_sum)

        for value in self.hidden_inputs2:
            self.hidden_outputs2.append(sigmoid(value))
        
        self.output_inputs = []

        for neuron_index in range(self.outputs):
            weighted_sum = 0

            for input_index in range(self.hidden_2):
                weighted_sum += self.hidden_outputs2[input_index] * self.weights_3[input_index][neuron_index]

            weighted_sum += self.bias_3[neuron_index]
            self.output_inputs.append(weighted_sum)

        self.outputs = exit_nums(self.output_inputs)

        print()
        print(self.hidden_inputs1)
        print(self.hidden_outputs1)
        print()
        print(self.hidden_inputs2)
        print(self.hidden_outputs2)
        print()
        print(self.output_inputs)
        print(self.outputs)


