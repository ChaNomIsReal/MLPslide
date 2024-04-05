# -*- coding: utf-8 -*-
"""สำเนาของ mlp_bp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GMM1gRXLbMf5gYihMW9yD1-jRErfu4-W
"""

import numpy as np

np.random.seed(3) # To make repeatable
LEARNING_RATE = 0.1
index_list = [0, 1, 2, 3] # Used to randomize order

# Define training examples.
x_train = [np.array([1.0, -1.0, -1.0]),
           np.array([1.0, -1.0, 1.0]),
           np.array([1.0, 1.0, -1.0]),
           np.array([1.0, 1.0, 1.0])]
y_train = [0.0, 1.0, 1.0, 0.0] # Output (ground truth)

print(type(x_train))

def neuron_w(input_count):
    weights = np.zeros( input_count+1)
    for i in range(0, (input_count)):
        weights[i] = np.random.uniform(-1.0, 1.0)
    return weights

"""n_w_o  weight of output layer 1x3  (bias, w1, w2)
n_w_h1 weight of hidden layer (2, 3)
"""

n_w_o = [neuron_w(2)]
n_w_h1 = [neuron_w(2), neuron_w(2)]
n_w_h2 = [neuron_w(1), neuron_w(1)]
n_yo = [0]
n_yh1 = [0,0,0,0]
n_yh2 = [0,0]
n_grad_o = [0]
n_grad_hd1 =  [0, 0]

print(n_w_o)
print(type(n_w_o))

print(n_w_h1)
print(n_w_h2)

def show_learning():
    print('Current weights:')
    for i, w in enumerate(n_w_o):
        print('Output neuron ', i,  ': w0 =', '%5.2f' % w[0],
              ', w1 =', '%5.2f' % w[1], ', w2 =',
              '%5.2f' % w[2])
    for i, w in enumerate(n_w_h1):
        print('Hidden 1 neuron ', i,  ': w0 =', '%5.2f' % w[0],
              ', w1 =', '%5.2f' % w[1], ', w2 =',
              '%5.2f' % w[2])
    for i, w in enumerate(n_w_h2):
        print('Hidden 2 neuron ', i,  ': w0 =', '%5.2f' % w[0],
              ', w1 =', '%5.2f' % w[1])
    print('----------------')

def forward_pass(x):
    global n_yo, n_yh1,n_yh2
    n_yh1[0] = np.tanh(np.dot(n_w_h1[0], n_w_h1[0])) # hidden w11
    n_yh1[1] = np.tanh(np.dot(n_w_h1[0], n_w_h1[1])) # hidden w12
    n_yh1[2] = np.tanh(np.dot(n_w_h1[1] ,n_w_h1[0])) # hidden w21
    n_yh1[3] = np.tanh(np.dot(n_w_h1[1] ,n_w_h1[1] )) # hidden w22
    n_yh2[0] = np.tanh(np.dot(n_yh1[0],n_yh1[1] )) # hidden w11
    n_yh2[1] = np.tanh(np.dot(n_yh1[2], n_yh1[3])) # hidden w21
    n2_inputs = np.array([1.0, n_yh2[0], n_yh2[1]])
    zo = np.dot(n_w_o, n2_inputs)
    n_yo = 1.0 / (1.0 + np.exp(- zo))  #sigmoid

def backward_pass(y_truth):
    global n_grad_o, n_grad_hd1
    error = -(y_truth - n_yo) # Derivative of loss-func
    derivative_sigmoid  = n_yo * (1.0 - n_yo) # Logistic derivative
    n_grad_o = error * derivative_sigmoid
    derivative_tanh = 1.0 - n_yh2[0]**2 # tanh derivative
    n_grad_hd1[0] = n_w_o[0][1] * n_grad_o * derivative_tanh
    derivative_tanh = 1.0 - n_yh2[1]**2 # tanh derivative
    n_grad_hd1[1] = n_w_o[0][2] * n_grad_o * derivative_tanh
    print('n_grad_o:', n_grad_o)
    print('n_grad_hd1:', n_grad_hd1[0], '   ', n_grad_hd1[1])

def adjust_weights(x):
    global n_w_o ,  n_w_h1, n_w_h2
    n2_inputs = np.array([1.0, n_yh2[0], n_yh2[1]]) # 1.0 is bias
    n_w_o -= (n2_inputs * LEARNING_RATE * n_grad_o)
    n_w_h1[0] -= (x * LEARNING_RATE * n_grad_hd1[0])
    n_w_h1[1] -= (x * LEARNING_RATE * n_grad_hd1[1])

# Network training loop.
all_correct = False
MAX_EPOCH = 50
for x in range(MAX_EPOCH):
    print('epoch: ', x)
    all_correct = True
    np.random.shuffle(index_list) # Randomize order
    for i in index_list: # Train on all examples
        forward_pass(x_train[i])
        backward_pass(y_train[i])
        adjust_weights(x_train[i])
        show_learning() # Show updated weights
    for i in range(len(x_train)): # Check if converged
        forward_pass(x_train[i])
        print('x1 =', '%4.1f' % x_train[i][1], ', x2 =', '%4.1f' % x_train[i][2],
              'y_train =', '%4.1f' % y_train[i], 'y =', '%.4f' % n_yo)
        if(((y_train[i] < 0.5) and (n_yo >= 0.5))
                or ((y_train[i] >= 0.5) and (n_yo < 0.5))):
            all_correct = False

