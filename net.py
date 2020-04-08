"""
Indices should be labeled in the order: 
    1. layer - l
    2. neuron in layer - k
    3. neuron in previous layer - j
"""
import numpy as np
import utils as u

M = 50
P = 50
n = 12
length = 5
hidden_layer_size = 5

class Net:
    def __init__(self, training_data, M, P, n, length, hidden_layer_size):
        self.training_data = training_data
        self.M = M
        self.P = P
        self.n = n
        self.length = length
        self.hidden_layer_size = hidden_layer_size
        self.layer_sizes = u.initialise_layer_sizes(self.M, self.length, self.hidden_layer_size)
        # Initialise weights randomly - will change once i have actual data
        self.weights = u.initialise_random_weights(self.layer_sizes) # w_l^jk
        self.training_data = u.random_inputs(self.layer_sizes, self.n)

    # One iteration of training
    def train(self):
        for i in range(len(self.training_data["values"])):
            activations = self.evaluateNet(self.training_data["values"][i]) # evaluate net on current training example
            print(activations[self.length - 1])

    def evaluateNet(self, training_example):
        activations = u.intialise_activations(self.layer_sizes, training_example)
        for l in range(1, self.length): # l = layer
            for k in range(self.layer_sizes[l]): # k = neuron
                for j in range(self.layer_sizes[l - 1]): # j = neurons in previous layer
                    print("l: {0}".format(l))
                    print("k: {0}".format(k))
                    print("j: {0}".format(j))
                    activations[l][k] = activations[l][k] + activations[l - 1][j] * self.weights[l][k][j]
                activations[l][k] = u.sigmoid(activations[l][k])
        return activations

myNet = Net("training_data - will be passed here, but the system for that is not yet created", M, P, n, length, hidden_layer_size)

#myNet.train()