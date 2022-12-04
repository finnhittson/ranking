import math
import numpy as np

def initialize_parameters():
    np.random.seed(10)
    W1 = np.random.rand(3, 25) - 0.5
    b1 = np.random.rand(3, 1) - 0.5

    W2 = np.random.rand(3, 3) - 0.5
    b2 = np.random.rand(3, 1) - 0.5

    return W1, b1, W2, b2

def encoder(y):
    encoded = []
    for true_value in y:
        encoded.append([0] * int(true_value) + [1] + [0] * (2 - int(true_value)))
    return np.array(encoded).T

def relu(Z):
    return np.maximum(Z, 0)

def relu_p(Z):
    return Z > 0

def softmax(Z):
    return np.exp(Z) / sum(np.exp(Z))

def forward_propagation(W1, b1, W2, b2, X):
    # input to hidden
    Z1 = W1.dot(X) - b1
    A1 = h(Z1)

    # hidden to output
    Z2 = W2.dot(A1) - b1
    A2 = softmax(Z2)
    
    return A1, A2

def h(n):
    #print(f"n: {n}")
    #print(f"normalized: {n / np.linalg.norm(n)}")
    #print(1 / (1 + np.exp(- n / np.linalg.norm(n))))
    #print()
    return 1 / (1 + np.exp(- n / np.linalg.norm(n)))



def sum_downstream(dL2, W2, A1):
    summed = []
    for idx, dL in enumerate(dL2):
        sum_me = []
        for w_k in W2[idx]:
            sum_me.append(dL * w_k / A1[idx])
        summed.append(sum(sum_me))
    return np.array(summed)

def backward_propagation(A1, A2, W1, b1, W2, b2, X, y):
    # output to hidden
    h_n_o = h(W2.dot(A1))
    dW2 = h_n_o * (1 - h_n_o) * (h_n_o - int(y) * np.ones((3,1))) * A1
    db2 = h_n_o * (1 - h_n_o) * (h_n_o - int(y) * np.ones((3,1))) 

    # hidden to input
    h_n_h = W1.dot(X)
    sum_ds = sum_downstream(dW2, W2, A1)
    
    dW1 = h_n_o * (1 - h_n_o) * sum_ds * X.T
    db1 = h_n_o * (1 - h_n_o) * sum_ds

    return dW1, db1, dW2, db2

def update_parameters(W1, dW1, b1, db1, W2, dW2, b2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1

    W2 = W2 - alpha * dW2
    b2 = b2 - alpha * db2
    
    return W1, b1, W2, b2

def compute_gradient(X, y, W1, b1, W2, b2, alpha):
    A1, A2 = forward_propagation(W1, b1, W2, b2, X)
    dW1, db1, dW2, db2 = backward_propagation(A1, A2, W1, b1, W2, b2, X, y)
    return update_parameters(W1, dW1, b1, db1, W2, dW2, b2, db2, alpha)

def get_predictions(A2):
    return np.argmax(A2.T, 1)