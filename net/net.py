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
        self.layerSizes = u.initialiselayerSizes(self.M, self.length, self.hiddenLayerSize)
        # Initialise weights randomly
        self.weights = u.initialiseRandomWeights(self.layerSizes) # w_l^jk
        self.trainingData = u.randomInputs(self.layerSizes, self.n)

    # One iteration of training
    def train(self):
        for i in range(len(self.trainingData["values"])):
            activations = self.evaluateNet(self.trainingData["values"][i]) # evaluate net on current training example
            print(activations[self.length - 1])
            while True:
                pass

    def evaluateNet(self, trainingExample):
        activations = u.initialiseActivations(self.layerSizes, trainingExample)
        for l in range(1, self.length): # l = layer
            for k in range(self.layerSizes[l]): # k = neuron
                for j in range(self.layerSizes[l - 1]): # j = neurons in previous layer
                    print("l: {0}".format(l))
                    print("k: {0}".format(k))
                    print("j: {0}".format(j))
                    activations[l][k] = activations[l][k] + activations[l - 1][j] * self.weights[l][k][j] # NEEDS FIX
                    # Layer index is -1 for weights, as there are no weights for first layer
                activations[l][k] = u.sigmoid(activations[l][k])
        return activations

net = Net("needs to be changed", 16, 50, 12, 5, 5)

net.train()