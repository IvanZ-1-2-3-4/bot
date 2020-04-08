"""
Contains utility functions
===========================

`random_inputs(layer_sizes, n)`  
`sigmoid(x)`  
`sigmoidPrime(x)`: derivative of sigmoid  
`intialise_activations(layer_sizes, training_example)`  
`initialise_layer_sizes(M, length, hidden_layer_size)`  
`initialise_random_weights(layer_sizes)`  
"""
import numpy as np

# Make random inputs to test network before I have the data
def random_inputs(layer_sizes, n):
    """Makes random inputs to test network before I have the data, returns {values: 2d float array,   
    labels: 2d string array, "positive" means has impact font, "negative means no impact font"}"""
    values = []
    labels = []
    for i in range(n): # Just setting the number of examples to be n-1 cause why not
        values.append([])
        labels.append([])
        for j in range (layer_sizes[0]):
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

def intialise_activations(layer_sizes, training_example):
    out = [training_example]
    for i in range(1, len(layer_sizes)):
        out.append(np.zeros(layer_sizes[i]))
    return out

def initialise_layer_sizes(M, length, hidden_layer_size):
    """Returns [M², hidden_layer_size,...length - 2 times..., hidden_layer_size, 1], length will """
    out = [M**2]
    for i in range(length - 2):
        out.append(hidden_layer_size)
    out.append(1)
    return out

def initialise_random_weights(layer_sizes):
    """Returns a 3 dimensional array, with coordinates I'll call l, k and j,   
    where l is the layer, k is the neuron in the layer, and j is the neuron in   
    the previous layer that the weight is connected to. Array at position l=0   
    is empty because it's the first layer."""
    out = [None] # first layer
    for i in range(1, len(layer_sizes)):
        out.append(np.random.randn(layer_sizes[i], layer_sizes[i - 1]))
    return out