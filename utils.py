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

def get_image_data_old(image_folder_path='images/test_set'):
    '''Returns data in the form of an array of dictionaries with components "value" and "label", 
    where "value" is the 1d numpy array representing the image, and the label can take one of the
    two values: "positive" or "negative". There is a uniform distribution of negative and positive
    examples throughout the data array.'''
    from skimage.exposure import adjust_gamma
    import os
    from skimage import io

    labels = []
    values = []
    positives = os.listdir(f'{image_folder_path}/positives')
    negatives = os.listdir(f'{image_folder_path}/negatives')
    positives_count = 0
    negatives_count = 0

    # Randomly distribute positive and negative examples
    while (not (positives_count == len(positives))) and (not (negatives_count == len(negatives))):
        if np.random.uniform() > 0.5:
            if not (positives_count == len(positives)):
                image = io.imread(f'images/test_set/positives/{positives[positives_count]}') # image as 2d array
                image = image.flatten() # image as flattened 1d array
                values.append(image)
                labels.append('positive')
                positives_count += 1
            else:
                image = io.imread(f'images/test_set/negatives/{negatives[negatives_count]}')
                image = image.flatten() # image as flattened 1d array
                values.append(image)
                labels.append('negative')
                negatives_count += 1
        else:
            if not (negatives_count == len(negatives)):
                image = io.imread(f'images/test_set/negatives/{negatives[negatives_count]}')
                image = image.flatten() # image as flattened 1d array
                values.append(image)
                labels.append('negative')
                negatives_count += 1
            else:
                image = io.imread(f'images/test_set/positives/{positives[positives_count]}')
                image = image.flatten() # image as flattened 1d array
                values.append(image)
                labels.append('positive')
                positives_count += 1
    return {'values': values, 'labels': labels}

def get_image_data(gamma='regular', image_folder_path='images/test_set'):
    '''Returns data in the form of an array of dictionaries with components "value" and "label", 
    where "value" is the 1d numpy array representing the image, and the label can take one of the
    two values: "positive" or "negative". There is a uniform distribution of negative and positive
    examples throughout the data array.'''
    from skimage.exposure import adjust_gamma
    import os
    from skimage import io

    if isinstance(gamma, str):
        if gamma == 'regular': gamma = 1
        elif gamma == 'medium': gamma = 3
        elif gamma == 'high': gamma = 6
        elif gamma == 'very high': gamma = 10

    data = []
    positives = os.listdir(f'{image_folder_path}/positives')
    negatives = os.listdir(f'{image_folder_path}/negatives')
    positives_count = 0
    negatives_count = 0

    # Randomly distribute positive and negative examples
    while (not (positives_count == len(positives))) and (not (negatives_count == len(negatives))):
        if np.random.uniform() > 0.5:
            if not (positives_count == len(positives)):
                image = io.imread(f'images/test_set/positives/{positives[positives_count]}') # image as 2d array
                image = adjust_gamma(image, gamma)
                image = image.flatten() # image as flattened 1d array
                data.append({
                    'value': image,
                    'label': 'positive'
                })
                positives_count += 1
            else:
                image = io.imread(f'images/test_set/negatives/{negatives[negatives_count]}')
                image = adjust_gamma(image, gamma)
                image = image.flatten() # image as flattened 1d array
                data.append({
                    'value': image,
                    'label': 'negative'
                })
                negatives_count += 1
        else:
            if not (negatives_count == len(negatives)):
                image = io.imread(f'images/test_set/negatives/{negatives[negatives_count]}')
                image = adjust_gamma(image, gamma)
                image = image.flatten() # image as flattened 1d array
                data.append({
                    'value': image,
                    'label': 'negative'
                })
                negatives_count += 1
            else:
                image = io.imread(f'images/test_set/positives/{positives[positives_count]}')
                image = adjust_gamma(image, gamma)
                image = image.flatten() # image as flattened 1d array
                data.append({
                    'value': image,
                    'label': 'positive'
                })
                positives_count += 1
    return data

if __name__ == '__main__':
    from skimage.viewer import ImageViewer
    viewer = ImageViewer(get_image_data()['values'][0])
    viewer.show()
    pass