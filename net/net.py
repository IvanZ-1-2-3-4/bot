import numpy as np

# Params
length = 5
hiddenLayerSize = 5
sizes = [81, hiddenLayerSize, hiddenLayerSize, hiddenLayerSize, 1]
weights = np.random.rand(length - 1, 5, 5) # w_l^jk

# Input activations
activations = []