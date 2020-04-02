import numpy as np

# Make random inputs to test network before I have the data
def randomInputs(sizes, n):
    """ Makes random inputs to test network before I have the data, returns {values: 2d float array, 
    labels: 2d string array, "positive" means has impact font, "negative means no impact font"}"""
    values = []
    labels = []
    for i in range(n): # Just setting the number of examples to be n-1 cause why not
        values.append([])
        labels.append([])
        for j in range (sizes[0]):
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

def initialiseActivations(sizes, trainingExample):
    out = [trainingExample]
    for i in range(1, len(sizes)):
        print(np.zeros(sizes[i]))
        out.append(np.zeros(sizes[i]))
    return out

def initialiseSizes(M, length, hiddenLayerSize):
    """Returns [M², hiddenLayerSize,...length - 2 times..., hiddenLayerSize, 1], length will """
    out = [M**2]
    for i in range(length - 2):
        out.append(hiddenLayerSize)
    out.append(1)
    return out

randomInputs(initialiseSizes(16, 5, 5), 12)