'''
Indices should be labeled in the following order: 
    1. layer - l
    2. neuron in layer - k
    3. neuron in previous layer - j
'''
import numpy as np
import utils as u

M = 32
P = 50
n = 21
length = 5
hidden_layer_size = 5
learning_rate = 1

class Net:
    '''Neural network that will make my life be again!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''
    def __init__(self, training_data, M, P, n, learning_rate, length, hidden_layer_size):
        self.training_data = training_data
        self.M = M # grids are of dimensions MxM
        self.P = P # proportion of grids on an image for it to be considered to be an impact font meme
        self.n = n # on average, how many grids per image (M*n ~ downscaled size of the image)
        self.learning_rate = learning_rate
        self.length = length # total number of layers
        self.hidden_layer_size = hidden_layer_size
        self.layer_sizes = u.initialise_layer_sizes(self.M, self.length, self.hidden_layer_size)
        self.weights = u.initialise_random_weights(self.layer_sizes) # w_l^jk
        # Initialise inputs randomly - will change once i have actual data
        self.training_data = u.random_inputs(self.layer_sizes, self.n)

    def train(self, logging=False):
        '''Train the whole network on all training examples. Accepts an optional parameter to enable or 
        disable logging of progress. Logging may slow down process.'''
        for i in range(len(self.training_data['values'])):
            activations = self.evaluateNet(self.training_data['values'][i]) # evaluate net on current training example
            print(activations[self.length - 1])

    def gradient_descent(self, result_activations):
        '''Perform GD and update weights based on one value of the evaluated network.'''
        for l in range(len(self.weights)):
            for k in range(len(self.weights[l])):
                for j in range(len(self.weights[l][k])):
                    der_w = self.get_partial_derivative_w(l, k, j) # partial derivative of cost with respect to the weight

    def get_partial_derivative_w(l, k, j):
        '''Get the partial derivative of cost with respect to the weight.'''
        for l in range()

    def evaluateNet(self, training_example):
        activations = u.intialise_activations(self.layer_sizes, training_example)
        for l in range(1, self.length): # l = layer
            for k in range(self.layer_sizes[l]): # k = neuron
                for j in range(self.layer_sizes[l - 1]): # j = neurons in previous layer
                    print(f'l: {l}')
                    print(f'k: {k}')
                    print(f'j: {j}')
                    activations[l][k] = activations[l][k] + activations[l - 1][j] * self.weights[l][k][j]
                activations[l][k] = u.sigmoid(activations[l][k])
        return activations

if __name__ == '__main__':
    myNet = Net('training_data - passed here as a 3d array', M, P, n, learning_rate, length, hidden_layer_size)
    myNet.train()