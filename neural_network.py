import random, math

def sigmoid(i):
    return 1 / (2.718281828459045 ** (- i) + 1)

def sigmoid_derivative(i):
    return (1 - i) * i



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

        for _ in range(inputs):
            for _ in range(hidden_1):
                self.weights_1.append(round(random.uniform(-0.5, 0.5), 2))
        for _ in range(hidden_1):
            for _ in range(hidden_2):
                self.weights_2.append(round(random.uniform(-0.5, 0.5), 2))
        for _ in range(hidden_2):
            for _ in range(outputs):
                self.weights_3.append(round(random.uniform(-0.5, 0.5), 2))

        for _ in range(hidden_1):
            self.bias_1.append(0.0)
        for _ in range(hidden_2):
            self.bias_2.append(0.0)
        for _ in range(outputs):
            self.bias_3.append(0.0)





        

