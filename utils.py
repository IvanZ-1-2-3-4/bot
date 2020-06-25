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

def get_image_data(gamma='regular', image_folder_path='images/test_set', shape='1d'):
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
                if shape == '1d': image = image.flatten() # image as flattened 1d array
                data.append({
                    'value': image,
                    'label': 'positive'
                })
                positives_count += 1
            else:
                image = io.imread(f'images/test_set/negatives/{negatives[negatives_count]}')
                image = adjust_gamma(image, gamma)
                if shape == '1d': image = image.flatten() # image as flattened 1d array
                data.append({
                    'value': image,
                    'label': 'negative'
                })
                negatives_count += 1
        else:
            if not (negatives_count == len(negatives)):
                image = io.imread(f'images/test_set/negatives/{negatives[negatives_count]}')
                image = adjust_gamma(image, gamma)
                if shape == '1d': image = image.flatten() # image as flattened 1d array
                data.append({
                    'value': image,
                    'label': 'negative'
                })
                negatives_count += 1
            else:
                image = io.imread(f'images/test_set/positives/{positives[positives_count]}')
                image = adjust_gamma(image, gamma)
                if shape == '1d': image = image.flatten() # image as flattened 1d array
                data.append({
                    'value': image,
                    'label': 'positive'
                })
                positives_count += 1
    return data

def process_for_impact_font(
    image,
    relative_radius_to_be_searched = 0.2, # On average, the proportion of the image around each pixel I want to search and alter.
    n=15, q=4, # The smoother the function gets (as q gets smaller), the huger p gets. q=4 seems to be a good middle ground, when p~10 000.
    f=None # Function that exaggerates higher pixel values.
):
    '''Increases brightness of image around areas with impact font, i.e. high contrast, black and white, 
    and lowers brightness of areas not likely to be impact font, i.e., color, low contrast.'''

    if f is None: 
        p = 10**n / (255*3)**q
        f = lambda x: p*x**q # By default a geometric function of the from px^q. Is necessarily equal to 10^n at x=765=255*3.

    w = image.shape[0] # Width
    l = image.shape[1] # Length


    r = int(relative_radius_to_be_searched * (w + l) / 2) # Radius is proportional to average of height and width.

    for row in range(len(image)):
        for col in range(len(image[row])):
            region = image[
                max(0, row - r) : min(w - 1, row + r), # Ensures that indices are within range.
                max(0, col - r) : min(l - 1, col + r)
            ]
            whiteness_and_acutance = get_acutance(region, f) + get_whiteness(region, f) # Measure of impact-font-ness.
            image[row][col] *= int(1 + get_acutance(region, f) / 255)
            print(f'row: {row} col: {col} ac: {get_acutance(region, f)}')
            show(region)
    return image



def get_acutance_by_1px_gradients(image, f_plain=np.exp): # Overall measure of sharpness of image
    '''oooooh ffancy word'''
    f = lambda x: f_plain(abs(x)) # Always take the absolute value of the difference
    max_accutance = lambda m: 6*(m**2)-(10*m)+4 # The highest possible accutance of an image
    acutance = 0
    w = image.shape[0]
    l = image.shape[1]
    for row in range(len(image)):
        for col in range(len(image[row])): # For each pixel
            local_acutance = 0
            # max_acutance = 1
            ref = int(np.sum(image[row][col])) # Magnitude of value current pixel, reference value
            ### ################################################################################################## ###
            for i in [row-1, row, row+1]:
                for j in [col-1, col, col+1]:                                                                      ###
                    if not (
                        (i < 0) or (i > w - 1) or                                                                  ###
                        (j < 0) or (j > l - 1) or 
                        (i == row and j == col)                                                                    ###
                    ):
            ### These for loops and if statement go through all the row, col coordinates of the neighboring pixels ###
                        local_acutance += f(ref - int(np.sum(image[i][j])))
                        # max_acutance += f(765)
            acutance += local_acutance
    return acutance / (w * l) # Average local acutance around each pixel

def get_whiteness(image, f_plain=np.exp):
    f = lambda x: abs(f_plain(x)) # Always take the absolute value of the difference
    whiteness = 0
    for row in image:
        for pixel in row: # For each pixel
            total = 0
            for value in pixel: total += f(value)
            whiteness += total * 100 / f(255 * 3) * 3 # Normalize to range between 0 - 100
    return whiteness / image.shape[0] * image.shape[1] # Normalize to range between 0 - 100

def foreachin(arr, callback, depth=0):
    '''Iterate over the elements of an iterable entity and perform call the callback with the element as the argument. If 
    the elements of the iterable are iterables and a depth greater than 0 is specified, iterate over depth number of sub-iterables.'''
    try:
        if depth == 0:
            prev = None
            for i in len(arr): 
                if not i == len(arr): prev = callback(arr[i], prev)
                else: return callback(arr[i], prev)
        else:
            for i in arr:
                for j in i:
                    foreachin(j, callback, depth - 1)
    except TypeError:
        TypeError('Depth specified was beyond the shape of array.')
        return False

def get_images(gamma='regular', image_folder_path='images/net_images_whole', shape='2d'):
    '''Load plain images from folder.'''
    from skimage.exposure import adjust_gamma
    import os
    from skimage import io

    if isinstance(gamma, str):
        if gamma == 'regular': gamma = 1
        elif gamma == 'medium': gamma = 3
        elif gamma == 'high': gamma = 6
        elif gamma == 'very high': gamma = 10

    images = []
    image_paths = os.listdir(image_folder_path)
    
    for image_path in image_paths:
        image = io.imread(f'{image_folder_path}/{image_path}')
        image = adjust_gamma(image, gamma)
        if shape == '1d': image = image.flatten()
        images.append(image)
        
    return images

def detect_edges(img):
    from skimage import io
    from skimage import color

    n = 1
    t = 50
    r = 1
    w = img.shape[0]; l = img.shape[1]
    img_gray = color.gray2rgb(color.rgb2gray(img))

    for row in range(len(img)):
        for col in range(len(img[row])):
            region = img[
                max(0, row - r) : min(w - 1, row + r), # Ensures that indices are within range.
                max(0, col - r) : min(l - 1, col + r)
            ]
            count = 0
            for arr in region:
                for elem in arr:
                    if (
                        int(np.sum(elem)) > (int(np.sum(img[row][col])) + t) or
                        int(np.sum(elem)) < (int(np.sum(img[row][col])) - t)
                    ): count += 1
            if count > n: img_gray[row][col] = [0, 255, 0]
    return img_gray

def show(img): 
    from skimage.viewer import ImageViewer
    ImageViewer(img).show()

if __name__ == '__main__':
    from skimage import io
    from skimage.viewer import ImageViewer as V
    # show(detect_edges(io.imread('images/net_images_whole/389.png')))
    img = io.imread('images/net_images_whole/355.png')
    img = np.array([
        [[0,0,0],[255,255,255],[0,0,0],[255,255,255],[0,0,0],[255,255,255]],
        [[255,255,255],[0,0,0],[255,255,255],[0,0,0],[255,255,255],[0,0,0]],
        [[0,0,0],[255,255,255],[0,0,0],[255,255,255],[0,0,0],[255,255,255]],
        [[255,255,255],[0,0,0],[255,255,255],[0,0,0],[255,255,255],[0,0,0]]
    ])
    # show(process_for_impact_font(img))
    n=7; q=7; p = (10**n) / ((255*3)**q)
    f = lambda x: p*(x**q)
    print(get_acutance(img, f))
    # print(get_acutance(img[20:100, 0:20], f))
    # print(get_acutance(img[0:20, 20:100], f))
    pass