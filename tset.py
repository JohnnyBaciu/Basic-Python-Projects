import numpy as np
import os
import json
import time
# Define the folder path where the .npy files are located
folder_path = 'extra/DRAWING_NN/data/'

# Create an empty list to store the file paths of .npy files
npy_files = []

# Iterate through all files in the folder
for file_name in os.listdir(folder_path):
    # Check if the file is a .npy file
    if file_name.endswith('.npy'):
        # Create the full file path and add it to the list
        file_path = os.path.join(folder_path, file_name)
        npy_files.append(file_path)

# Load each .npy file, invert the pixels, and assign labels
X_train = []
y_train = []

for file_path in npy_files:
    file_name = os.path.basename(file_path)
    label = None
    if 'drums.npy' in file_name:
        label = 0
    elif 'sun.npy' in file_name:
        label = 1
    elif 'laptop.npy' in file_name:
        label = 2
    elif 'anvil.npy' in file_name:
        label = 3
    elif 'baseball_bat.npy' in file_name:
        label = 4
    elif 'ladder.npy' in file_name:
        label = 5
    elif 'eyeglasses.npy' in file_name:
        label = 6
    elif 'grapes.npy' in file_name:
        label = 7
    elif 'book.npy' in file_name:
        label = 8
    elif 'dumbbell.npy' in file_name:
        label = 9

    if label is not None:
        data = np.load(file_path)
        data = data[:5000]
        inverted_data = 255 - data  # Invert the pixels
        X_train.extend(inverted_data)
        y_train.extend([label] * len(data))

# Convert lists to numpy arrays
X_train = np.array(X_train)
y_train = np.array(y_train)

# Initialize weights and biases using He initialization
def initialize_weights(input_size, hidden_size, output_size):
    W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)  # He initialization for W1
    b1 = np.zeros((1, hidden_size))
    W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)  # He initialization for W2
    b2 = np.zeros((1, output_size))
    return W1, b1, W2, b2

# Define the activation functions (ReLU for the hidden layer and softmax for the output layer)
def relu(x):
    return np.maximum(0, x)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# Define the forward propagation function
def forward_propagation(X, W1, b1, W2, b2):
    Z1 = np.dot(X, W1) + b1
    A1 = relu(Z1)
    Z2 = np.dot(A1, W2) + b2
    A2 = softmax(Z2)
    return A2, A1

# Define the training loop
def train(X, y, W1, b1, W2, b2, learning_rate=0.001, epochs=2000, batch_size=64):
    for epoch in range(epochs):
        # Shuffle the training data and split into batches
        indices = np.arange(len(X))
        np.random.shuffle(indices)
        X_shuffled = X[indices]
        y_shuffled = y[indices]

        num_batches = len(X) // batch_size
        for batch in range(num_batches):
            start = batch * batch_size
            end = (batch + 1) * batch_size
            X_batch = X_shuffled[start:end]
            y_batch = y_shuffled[start:end]

            # Forward propagation
            A2, A1 = forward_propagation(X_batch, W1, b1, W2, b2)
            # Compute gradients
            m = len(X_batch)
            dZ2 = A2.copy()
            dZ2[range(m), y_batch] -= 1
            dZ2 /= m
            dW2 = np.dot(A1.T, dZ2)
            db2 = np.sum(dZ2, axis=0, keepdims=True)
            dA1 = np.dot(dZ2, W2.T)
            dZ1 = dA1 * (A1 > 0)
            dW1 = np.dot(X_batch.T, dZ1)
            db1 = np.sum(dZ1, axis=0, keepdims=True)

            # Update weights and biases
            W2 -= learning_rate * dW2
            b2 -= learning_rate * db2
            W1 -= learning_rate * dW1
            b1 -= learning_rate * db1

        if epoch % 100 == 0:
            loss = compute_loss(X, y, W1, b1, W2, b2)
            print(f'Epoch {epoch}, Loss: {loss:.4f}')

    return W1, b1, W2, b2

# Compute loss (cross-entropy)
def compute_loss(X, y, W1, b1, W2, b2):
    A2, _ = forward_propagation(X, W1, b1, W2, b2)
    m = len(X)
    loss = -np.sum(np.log(A2[range(m), y])) / m
    return loss

# Initialize weights and biases
input_size = X_train.shape[1]
hidden_size = 512  # Increased hidden layer size
output_size = 10  # Number of classes
W1, b1, W2, b2 = initialize_weights(input_size, hidden_size, output_size)

# Train the neural network
start_time = time.time()
W1, b1, W2, b2 = train(X_train, y_train, W1, b1, W2, b2, learning_rate=0.001, epochs=1500, batch_size=128)
end_time = time.time()

print(f'Training time: {end_time - start_time:.2f} seconds')

# Save the trained parameters to a JSON file
params = {
    'W1': W1.tolist(),
    'b1': b1.tolist(),
    'W2': W2.tolist(),
    'b2': b2.tolist()
}

with open('extra/DRAWING_NN/updated_model_params.json', 'w') as json_file:
    json.dump(params, json_file)
