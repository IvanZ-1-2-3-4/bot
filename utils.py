'''
Contains utility functions
===========================

`random_inputs(layer_sizes, n)`  
`sigmoid(x)`  
`sigmoidPrime(x)`: derivative of sigmoid  
`intialise_activations(layer_sizes, training_example)`  
`initialise_layer_sizes(M, length, hidden_layer_size)`  
`initialise_random_weights(layer_sizes)`  
'''

import numpy as np
from skimage import io
import os
import pickle

# Make random inputs to test network before I have the data
def random_inputs(layer_sizes, n):
    '''Makes random inputs to test network before I have the data, returns {values: 2d float array,   
    labels: 2d string array, 'positive' means has impact font, 'negative means no impact font'}'''
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
                labels[i].append('positive')
            else:
                labels[i].append('negative')
    return {'values': values, 'labels': labels}  

def initialise_layer_sizes(M, length, hidden_layer_size):
    '''Returns [M², hidden_layer_size,...length-2 times..., hidden_layer_size, 1]'''
    out = [M**2]
    for _i in range(length - 2):
        out.append(hidden_layer_size)
    out.append(1)
    return out

def get_image_data():
    values = []
    labels = []
    positives = os.listdir('images/test_set/positives')
    negatives = os.listdir('images/test_set/negatives')
    positives_count = 0
    negatives_count = 0

    # Randomly distribute positive and negative examples
    while (not (positives_count == len(positives))) and (not (negatives_count == len(negatives))):
        if np.random.uniform() > 0.5:
            if not (positives_count == len(positives)):
                image = io.imread(f'images/test_set/positives/{positives[positives_count]}') # image as 2d array
                values.append(image.flatten()) # image as flattened 1d array
                labels.append('positive')
                positives_count += 1
            else:
                image = io.imread(f'images/test_set/negatives/{negatives[negatives_count]}')
                values.append(image.flatten())
                labels.append('negative')
                negatives_count += 1
        else:
            if not (negatives_count == len(negatives)):
                image = io.imread(f'images/test_set/negatives/{negatives[negatives_count]}')
                values.append(image.flatten())
                labels.append('negative')
                negatives_count += 1
            else:
                image = io.imread(f'images/test_set/positives/{positives[positives_count]}')
                values.append(image.flatten())
                labels.append('positive')
                positives_count += 1
    return {'values': np.float64(values), 'labels': labels}

if __name__ == '__main__':
    from skimage.viewer import ImageViewer
    viewer = ImageViewer(get_image_data()['values'][0])
    viewer.show()
    pass