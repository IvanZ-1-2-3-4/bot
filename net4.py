'''
Indices should be labeled in the following order: THANKS NIELSEN
    1. layer - l
    2. neuron in layer - j
    3. neuron in previous layer - k
'''
import numpy as np
import utils as u
import pickle

M = 32
LENGTH = 3
HIDDEN_LAYER_SIZE = 16
LEARNING_RATE = 0.1

class ImpactNetV4:
    '''Now with options for cost and activation functions, and other juicy optimisations'''
    def __init__(
        self, M, learning_rate, length, hidden_layer_size, training_data=None, 
        activation_function_type='sigmoid', cost_function_type='cross-entropy', 
        weights=None, biases=None
    ):
        self.training_data = training_data
        if not self.training_data: print('NOTICE: No training data has been passed.')
        self.M = M # grids are of dimensions MxM
        self.learning_rate = learning_rate
        self.length = length # total number of layers
        self.last_layer_index = self.length - 1 # just so it's easier to interface between the number of layers and the way they're indexed in the arrays
        self.hidden_layer_size = hidden_layer_size
        self.layer_sizes = self.initialise_layer_sizes(self.M, self.length, self.hidden_layer_size)
        if not weights: self.weights = self.initialise_random_weights() # w_l^kj
        if not biases: self.biases = self.intialise_random_biases()
        self.activation_function_type = activation_function_type
        self.cost_function_type = cost_function_type
        self.training_data = training_data
        self.trained = False # If net has been trained before


    def train(self, logging=True, logging_partial=False, per_example_logging_callback=False, gradient_descent_logging_callback=False):
        '''Train the whole network on all training examples. Accepts an optional parameter to enable or 
        disable logging of progress. Logging may slow down process.'''

        # Evaluate network on training examples
        results = []
        for i in range(len(self.training_data)):
            results.append({
                'values': self.feedforward(self.training_data[i]['value']),
                'label': self.training_data[i]['label']
            }) # Evaluate net on current training example
        if logging: print('Evaluated training examples, beggining gradient descent')

        # Perform gradient descent on results
        result_counter = 0
        for result in results:
            self.gradient_descent(result, logging, logging_partial, result_counter, len(results))
            result_counter += 1
            if per_example_logging_callback: per_example_logging_callback(self, result)
        if logging: print(f'Training finished, final weights are:\n{self.weights}\nFinal biases are:\n{self.biases}')
        self.trained = True # Network has been trained!


    def gradient_descent(self, result, logging=True, logging_partial=False, result_counter=0, result_total=0):
        '''Perform GD and update weights based on one value of the evaluated network.'''

        if logging_partial: print(f'Performing gradient descent on result {result_counter}/{result_total}')

        dc_dz = self.backprop(result) # Perform backpropagation on the current results, get the derivatives of cost with respect to the weighted inputs of each neuron

        # For each neuron, adjust weights and biases according to the calculated derivatives
        a_result = result['values']['activations']
        for l in range(1, self.length):
            self.biases[l] = self.biases[l] - self.learning_rate * dc_dz[l] * self.biases[l]
            for j in range(len(self.weights[l])):
                dc_dw = dc_dz[l][j] * a_result[l-1]
                self.weights[l][j] = self.weights[l][j] - self.learning_rate * dc_dw


    def backprop(self, result):
        '''Perform backpropagation on single result, output the derivatives of the cost with respect to the weighted inputs to each neuron in the network.'''

        z_result = result['values']['weighted_inputs']
        a_result = result['values']['activations']

        dc_dz = self.intialise_network_values(a_result) # Derivatives of the cost with respect to the weighted inputs to each neuron

        L = self.last_layer_index # For clarity

        # Calculate cost of network, and calculate the partial derivative of the cost with respect to the weighted input of the final neuron
        cost = self.cost(a_result[L], result['label'])
        dc_dz[L][0] = cost['dc_da'] * self.activation_function(z_result[L])['derivative']

        # Backpropagate error in the final neuron through the network
        for l in range(L-1, 0, -1): # Between second to last layer, and second layer (no weights on first layer so no need to compute for it)
            dc_dz[l] = (
                np.matmul(np.transpose(self.weights[l+1]), dc_dz[l+1]) *  # Transposing the weight matrix 'inverts' the movement of values through the network: 
                self.activation_function(z_result[l])['derivative']       # instead of summing over the weights of each neuron in the lth layer (to obtain a value 
            )                                                             # for a neuron in the l+1th layer), we sum over the weights of neurons in the l+1th layer.
        return dc_dz


    def cost(self, value, expectation):
        # Expectation is either 0 or 1
        y = None
        if expectation == 'positive': y = 1
        elif expectation == 'negative': y = 0
        if self.cost_function_type == 'quadratic':
            return {
                'value': (y - value)**2,
                'dc_da': -2 * (y - value)
            }
        elif self.cost_function_type == 'cross-entropy':
            return {
                'value': y * np.log(value) + (1 - y) * np.log(1 - value),
                'dc_da': ((y / value) - ((1 - y) / (1 - value)))
            }
    

    def feedforward(self, training_example):
        activations = self.intialise_network_values(training_example) # Empty array of activation vectors for each layer
        weighted_inputs = self.intialise_network_values(training_example) # Empty array of weighted input vectors for each layer

        for l in range(1, self.length):
            weighted_inputs[l] = np.matmul(self.weights[l], activations[l-1]) + self.biases[l]
            activations[l] = self.activation_function(weighted_inputs[l])['value']

        return {
            'weighted_inputs': weighted_inputs,
            'activations': activations
        }

    # Only return the final result of the evaluation
    def evaluate(self, image): return self.feedforward(image)['activations'][self.last_layer_index][0]
        
    
    ######################### MISCELLANEOUS #########################
    def intialise_network_values(self, training_example):
        out = [np.array(training_example)]
        for i in range(1, len(self.layer_sizes)):
            # append array of zeros for each layer
            out.append(np.zeros(self.layer_sizes[i]))
        return out


    def initialise_layer_sizes(self, M, length, hidden_layer_size):
        '''Returns [M², hidden_layer_size,...length-2 times..., hidden_layer_size, 1]'''
        out = [M**2]
        for _i in range(length - 2):
            out.append(hidden_layer_size)
        out.append(1)
        return out


    def initialise_random_weights(self):
        '''Returns a 3 dimensional array, with coordinates I'll call l, j and k,   
        where l is the layer, j is the neuron in the layer, and k is the neuron in   
        the previous layer that the weight is connected to. Array at position l=0   
        is empty because it's the first layer and nothing connects to it.'''
        out = [None] # First layer is none
        for i in range(1, self.length):
            out.append(np.random.randn(self.layer_sizes[i], self.layer_sizes[i-1]))
        return out


    def intialise_random_biases(self):
        out = [None] # First layer is none
        for i in range(1, self.length):
            out.append(np.random.randn(self.layer_sizes[i]))
        return out
    

    def activation_function(self, x):
        if self.activation_function_type == 'sigmoid':
            s = 1.0 / (1.0 + np.exp(-x))
            return {
                'value': s,
                'derivative': s * (1.0 - s)
            }
        elif self.activation_function_type == 'relu':
            return {
                'value': x * (x > 0),
                'derivative': 1.0 * (x > 0)
            }
        if self.activation_function_type == 'identity':
            return {
                'value': x,
                'derivative': 1
            }
        


def create_default_net(
    M=M, 
    learning_rate=LEARNING_RATE, 
    length=LENGTH, 
    hidden_layer_size=HIDDEN_LAYER_SIZE,
    training_data=u.get_image_data(),
    activation_function_type='sigmoid',
    cost_function_type='cross-entropy',
    weights=None, biases=None
):
    return ImpactNetV4(
        M, 
        learning_rate, 
        length, 
        hidden_layer_size, 
        training_data, 
        activation_function_type,
        cost_function_type,
        weights, biases
    )

def fetch_trained_net(file):
    return pickle.load(open(file, 'rb'))

def make_trained_net():
    import pickle
    net = create_default_net()
    net.train()
    pickle.dump(net, open('net4_trained.pickle', 'wb'))
    return net

if __name__ == '__main__':
    net = create_default_net()
    net.train(True)
    # pickle.dump(net.weights, open('trained_netv2_weights.pickle', 'wb'))
    # pickle.dump(net, open('trained_netv2.pickle', 'wb'))