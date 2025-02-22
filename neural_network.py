import random, math

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



        for _ in range(hidden_1):
            self.bias_1.append(0.0)
        for _ in range(hidden_2):
            self.bias_2.append(0.0)
        for _ in range(outputs):
            self.bias_3.append(0.0)





        

