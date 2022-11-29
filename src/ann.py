import math

def initialize_parameters():
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
    Z1 = W1.dot(X) + b1
    A1 = relu(Z1)
    
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)
    
    return Z1, A1, Z2, A2

def backward_propagation(A1, A2, W2, Z1, Z2, X, y, m):
    dZ2 = A2 - encoder(y)
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = np.expand_dims(1 / m * np.sum(dZ2, axis=1), axis = 1)
    
    dZ1 = W2.dot(dZ2) * relu_p(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = np.expand_dims(1 / m * np.sum(dZ1, axis=1), axis = 1)
    
    return dW1, db1, dW2, db2

def update_parameters(W1, dW1, b1, db1, W2, dW2, b2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1

    W2 = W2 - alpha * dW2
    b2 = b2 - alpha * db2
    
    return W1, b1, W2, b2

def gradient_descent(X, y, iterations, alpha, m):
    Z1, A1, Z2, A2 = forward_propagation(W1, b1, W2, b2, X)
    dW1, db1, dW2, db2 = backward_propagation(A1, A2, W2, Z1, Z2, X, y, m)
    W1, b1, W2, b2 = update_parameters(W1, dW1, b1, db1, W2, dW2, b2, db2, alpha)
    return W1, b1, W2, b2