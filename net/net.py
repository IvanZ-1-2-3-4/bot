"""
Indices should be labeled in the order: 
    1. layer - l
    2. neuron in layer - k
    3. neuron in previous layer - j
"""
import numpy as np
import utils as u

class Net:
    def __init__(self, trainingData, M, P, n, length, hiddenLayerSize):
        self.trainingData = trainingData
        self.M = M
        self.P = P
        self.n = n
        self.length = length
        self.hiddenLayerSize = hiddenLayerSize
        self.sizes = u.initialiseSizes(self.M, self.length, self.hiddenLayerSize)
        # Initialise weights randomly
        self.weights = np.random.rand(self.length - 1, 5, 5) # w_l^jk
        self.trainingData = u.randomInputs(self.sizes, self.n)

    # One iteration of training
    def train(self):
        for i in range(len(self.trainingData["values"])):
            activations = self.evaluateNet(self.trainingData["values"][i]) # evaluate net on current training example
            print(activations[self.length - 1])

    def evaluateNet(self, trainingExample):
        activations = u.initialiseActivations(self.sizes, trainingExample)
        for l in range(1, self.length): # l = layer
            for k in range(self.sizes[l]): # k = neuron
                for j in range(self.sizes[l - 1]): # j = neurons in previous layer
                    print("l: {0}".format(l))
                    print("k: {0}".format(k))
                    print("j: {0}".format(j))
                    activations[l][k] = activations[l][k] + activations[l - 1][j] * self.weights[l-2][k][j] # NEEDS FIX
                    # Layer index is -1 for weights, as there are no weights for first layer
                activations[l][k] = u.sigmoid(activations[l][k])
        return activations

net = Net("needs to be changed", 16, 50, 12, 5, 5)

net.train()