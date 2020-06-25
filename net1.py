'''
Indices should be labeled in the following order: 
    1. layer - l
    2. neuron in layer - k
    3. neuron in previous layer - j
'''
import numpy as np
import utils as u
import pickle

M = 32
P = 50
n = 21 # prety redundant
length = 3
hidden_layer_size = 16
learning_rate = 1

class ImpactNetV1:
    '''Version 1 with for loops.'''
    def __init__(self, M, learning_rate, length, hidden_layer_size, training_data=None):
        self.training_data = training_data
        if not training_data: print('NOTICE: No training data has been passed.')
        self.M = M # grids are of dimensions MxM
        self.learning_rate = learning_rate
        self.length = length # total number of layers
        self.last_layer_index = self.length - 1 # just so it's easier to interface between the quantity of layers and the way they're indexed in the arrays
        self.hidden_layer_size = hidden_layer_size
        self.layer_sizes = self.initialise_layer_sizes(self.M, self.length, self.hidden_layer_size)
        self.weights = self.initialise_random_weights(self.layer_sizes) # w_l^jk
        # Initialise inputs randomly - will change once I have actual data
        self.training_data = training_data

    def train(self, logging=False):
        '''Train the whole network on all training examples. Accepts an optional parameter to enable or 
        disable logging of progress. Logging may slow down process.'''
        results = []
        for i in range(len(self.training_data['values'])):
            results.append(self.feedforward(self.training_data['values'][i])) # evaluate net on current training example
        print('Evaluated training examples, beggining gradient descent')
        resultCounter = 0
        for result in results:
            self.gradient_descent(result, self.training_data['labels'][i], logging, resultCounter, len(results))
            resultCounter += 1
        if logging: print(f'Training finished, final weights are:\n{self.weights}')

    def gradient_descent(self, results, expectation, logging=False, resultCounter=0, resultTotal=0):
        '''Perform GD and update weights based on one value of the evaluated network.'''
        if logging: print(f'Performing gradient descent on result {resultCounter}/{resultTotal}')
        for l in range(1, len(self.weights)):
            for k in range(len(self.weights[l])):
                for j in range(len(self.weights[l][k])):
                    # for each weight
                    der_w = self.get_partial_derivative_w(l, k, j, results, expectation, logging) # partial derivative of cost with respect to the weight
                    self.weights[l][k][j] = self.weights[l][k][j] + self.weights[l][k][j] * self.learning_rate * -der_w
    
    def get_partial_derivative_w(self, l_w, k_w, j_w, results, expectation, logging=False):
        '''Get the partial derivative of cost with respect to the weight specified.'''
        # dCOST/da * da/dz * (sum of dz/da * ( sum of da/dz ... * da/dz * dz/dw)))))
        return (
            self.cost(results[self.last_layer_index][0], expectation)['derivative'] * # dCOST/da_L *
            self.backprop(self.last_layer_index, 0, l_w, k_w, j_w, results) # da_L/dw Start backprop at last neuron HOPEFULLY IT WORKS
        )

    def backprop(self, l, k, l_w, k_w, j_w, results):
        if l - l_w > 1:
            sum_derivatives_a_l_minus_1 = 0
            for j in range(self.layer_sizes[l-1]):
                # for every neuron in previous layer
                sum_derivatives_a_l_minus_1 = (
                    sum_derivatives_a_l_minus_1 + 
                    self.sigmoid_prime(self.sigmoid_inverse(results[l][k])) * # σ'(z_l) * 
                    self.weights[l][k][j] * # w_l^jk = da_l/da_l-1
                    self.backprop(l - 1, j, l_w, k_w, j_w, results) # * da_l-1/dw
                )
            return sum_derivatives_a_l_minus_1
        else:
            return (
                self.sigmoid_prime(self.sigmoid_inverse(results[l][k])) * 
                self.weights[l][k][k_w] * 
                self.sigmoid_prime(self.sigmoid_inverse(results[l-1][k_w])) * 
                results[l_w-1][j_w] 
            )

    def cost(self, result, expectation_in):
        # Expectation is either 0 or 1
        expectation = None
        if expectation_in == 'positive': expectation = 1
        elif expectation_in == 'negative': expectation = 0
        return {
            'value': (expectation - result)**2,
            'derivative': -2 * (expectation - result)
        }
    
    def feedforward(self, training_example):
        activations = self.intialise_activation_values(self.layer_sizes, training_example)
        for l in range(1, self.length): # l = layer
            for k in range(self.layer_sizes[l]): # k = neuron
                for j in range(self.layer_sizes[l-1]): # j = neurons in previous layer
                    activations[l][k] = (
                        activations[l][k] + 
                        activations[l-1][j] * 
                        self.weights[l][k][j]
                    )
                activations[l][k] = self.sigmoid(activations[l][k])
        return activations

    # Only return the final result of the evaluation
    def evaluate(self, training_example): return self.feedforward(training_example)[self.last_layer_index][0]
        
    
    ######################### MISCELLANEOUS #########################
    def intialise_activation_values(self, layer_sizes, training_example):
        out = [training_example]
        for i in range(1, len(layer_sizes)):
            # append array of zeros for each layer
            out.append(np.zeros(layer_sizes[i]))
        return out

    def initialise_layer_sizes(self, M, length, hidden_layer_size):
        '''Returns [M², hidden_layer_size,...length-2 times..., hidden_layer_size, 1]'''
        out = [M**2]
        for _i in range(length - 2):
            out.append(hidden_layer_size)
        out.append(1)
        return out

    def initialise_random_weights(self, layer_sizes):
        '''Returns a 3 dimensional array, with coordinates I'll call l, k and j,   
        where l is the layer, k is the neuron in the layer, and j is the neuron in   
        the previous layer that the weight is connected to. Array at position l=0   
        is empty because it's the first layer.'''
        out = [None] # first layer is none
        for i in range(1, len(layer_sizes)):
            out.append(np.random.randn(layer_sizes[i], layer_sizes[i-1]))
        return out
    
    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def sigmoid_prime(self, x):
        s = self.sigmoid(x)
        return s * (1.0 - s)
    
    def sigmoid_inverse(self, x):
        # used to get weighted input value from known activation value, could be optimised but HUUUEEEEEE
        if x == 1: x = 0.999
        return np.log(x / (1.0 - x))

def create_default_net():
    return ImpactNetV1(M, learning_rate, length, hidden_layer_size, u.get_image_data_old())

if __name__ == '__main__':
    net = ImpactNetV1(M, learning_rate, length, hidden_layer_size, u.get_image_data_old())
    net.train(True)
    pickle.dump(net.weights, open('trained_netv1_weights.pickle', 'wb'))
    pickle.dump(net, open('trained_netv1.pickle', 'wb'))
else:
    tn = ImpactNetV1(M, learning_rate, length, hidden_layer_size, u.random_inputs(u.initialise_layer_sizes(M, length, hidden_layer_size), n))
    print(f'Test network tn created with args: (M={M}, learning_rate={learning_rate}, length={length}, hidden_layer_size={hidden_layer_size}, training_data=RANDOM_INPUTS)')