"""
Contains utility functions
===========================

`randomInputs(layerSizes, n)`  
`sigmoid(x)`  
`sigmoidPrime(x)`: derivative of sigmoid  
`initialiseActivations(layerSizes, trainingExample)`  
`initialiselayerSizes(M, length, hiddenLayerSize)`  
`initialiseRandomWeights(layerSizes)`  
"""
import numpy as np

# Make random inputs to test network before I have the data
def randomInputs(layerSizes, n):
    """Makes random inputs to test network before I have the data, returns {values: 2d float array,   
    labels: 2d string array, "positive" means has impact font, "negative means no impact font"}"""
    values = []
    labels = []
    for i in range(n): # Just setting the number of examples to be n-1 cause why not
        values.append([])
        labels.append([])
        for j in range (layerSizes[0]):
            # Append random new value
            values[i].append(np.random.randn())
            # Append random new label for the value
            if np.random.rand() > 0.5:
                labels[i].append("positive")
            else:
                labels[i].append("negative")
    return {"values": values, "labels": labels}  

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoidPrime(x):
    s = sigmoid(x)
    return s * (1 - s)

def initialiseActivations(layerSizes, trainingExample):
    out = [trainingExample]
    for i in range(1, len(layerSizes)):
        out.append(np.zeros(layerSizes[i]))
    return out

def initialiselayerSizes(M, length, hiddenLayerSize):
    """Returns [M², hiddenLayerSize,...length - 2 times..., hiddenLayerSize, 1], length will """
    out = [M**2]
    for i in range(length - 2):
        out.append(hiddenLayerSize)
    out.append(1)
    return out

def initialiseRandomWeights(layerSizes):
    """Returns a 3 dimensional array, with coordinates I'll call l, k and j,   
    where l is the layer, k is the neuron in the layer, and j is the neuron in   
    the previous layer that the weight is connected to. Array at position l=0   
    is empty because it's the first layer."""
    out = [None] # first layer
    for i in range(1, len(layerSizes)):
        out.append(np.random.randn(layerSizes[i], layerSizes[i - 1]))
    return out