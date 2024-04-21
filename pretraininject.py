import numpy as np
import mnist
import os
import json
from PIL import Image
import cv2
# Load MNIST data
X_train_mnist = mnist.train_images()
y_train_mnist = mnist.train_labels()
X_raw = mnist.train_images()
y_raw = mnist.train_labels()
X_raw = X_raw.reshape(-1, 28*28) / 255.0

folder_path = 'extra/numbers'
def load_images_from_folder(folder):
    images = []
    labels = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            # Load the image using PIL and resize it to 28x28 pixels
            img = Image.open(os.path.join(folder, filename))
            img = img.convert('L')  # Convert to grayscale if needed
            img = img.resize((28, 28))
            img_array = np.array(img)

            # Flatten the image and normalize pixel values
            img_array = img_array.reshape(-1) / 255.0

            # Append the image array to the list of images
            images.append(img_array)

            # Extract the label from the filename (assuming filename format: label_image.jpg)
            label = int(filename.split('_')[0])  # Extract label from filename
            labels.append(label)

    return np.array(images), np.array(labels)
# Variable to control noise level (standard deviation of Gaussian noise)
noise_std_dev = 0.7  # Initial value, you can adjust this

# Initialize a list to store preprocessed images
preprocessed_images = []

# Loop through each image in the MNIST training dataset
for i in range(len(X_train_mnist)):
    # Get the original image and its corresponding label
    original_image = X_train_mnist[i]

    # Randomly select rotation direction (clockwise or counterclockwise)
    rotation_direction = np.random.choice([-1, 1])  # -1 for counterclockwise, 1 for clockwise
    angle = rotation_direction * np.random.uniform(1, 40)  # Random angle between 1 and 10 degrees

    # Rotate the image around the center
    rows, cols = original_image.shape
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    rotated_image = cv2.warpAffine(original_image, rotation_matrix, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=0)

    # Add Gaussian noise to the rotated image
    noise = np.random.normal(0, noise_std_dev, rotated_image.shape).astype(np.uint8)
    noisy_rotated_image = cv2.add(rotated_image, noise)

    # Append the preprocessed image to the list
    preprocessed_images.append(noisy_rotated_image)

# Convert the list of preprocessed images to a NumPy array
X_train_preprocessed = np.array(preprocessed_images)

# Reshape the preprocessed images and normalize pixel values
X_train_preprocessed = X_train_preprocessed.reshape(-1, 28*28) / 255.0

# Save X_train_preprocessed as a matrix (e.g., in a JSON file or NumPy .npy file) for use in training
np.save('extra/X_train_preprocessed.npy', X_train_preprocessed)

# Save the first formatted image as a JPEG
scaled_image = (255 * X_train_preprocessed[0]).astype(np.uint8)
scaled_image = scaled_image.reshape(28, 28)
cv2.imwrite('extra/doublecheck.jpg', scaled_image)
print('First formatted image saved as doublecheck.jpg')

# Ensure y_train_mnist has the correct shape and type
y_train_mnist = y_train_mnist.astype(np.int32)

X_custom, y_custom = load_images_from_folder(folder_path)

X_train = np.concatenate((X_train_preprocessed, X_custom), axis=0)
y_train = np.concatenate((y_train_mnist, y_custom), axis=0)
X_train = np.concatenate((X_train, X_raw), axis=0)
y_train = np.concatenate((y_train, y_raw), axis=0)
X_train2 = mnist.test_images()
Y_train2 = mnist.test_labels()
Y_train2 = Y_train2.astype(np.int32)
X_train2 = X_train2.reshape(-1, 28*28) / 255.0

X_train = np.concatenate((X_train, X_train2), axis=0)
y_train = np.concatenate((y_train, Y_train2), axis=0)
np.random.seed(0)
input_size = 784  # 28x28 pixels flattened
hidden_size = 128  # Number of neurons in the hidden layer
output_size = 10  # Number of output classes (digits 0-9)

y_train = y_train.astype(np.int32)
print(len(X_train))
print('X_train shape:', X_train.shape)
print('y_train shape:', y_train.shape)

W1 = np.random.randn(input_size, hidden_size) * 0.01
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size) * 0.01
b2 = np.zeros((1, output_size))

# Define the activation functions (ReLU for the hidden layer and softmax for the output layer)
def relu(x):
    return np.maximum(0, x)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# Define the forward propagation function
def forward_propagation(X):
    Z1 = np.dot(X, W1) + b1
    A1 = relu(Z1)
    Z2 = np.dot(A1, W2) + b2
    A2 = softmax(Z2)
    return A2, A1

# Define the training loop
def train(X, y, W1, b1, W2, b2, learning_rate=0.01, epochs=100, batch_size=32):
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
            A2, A1 = forward_propagation(X_batch)
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

        if epoch % 2 == 0:
            h = compute_loss(X, y)
            print(f'Epoch {epoch}, Loss: {h}')
            

    return W1, b1, W2, b2

# Compute loss (cross-entropy)
def compute_loss(X, y):
    A2, _ = forward_propagation(X)
    m = len(X)
    loss = -np.sum(np.log(A2[range(m), y])) / m
    return loss

W1, b1, W2, b2 = train(X_train, y_train, W1, b1, W2, b2)

# After training, save the trained weights and biases to a JSON file
params = {
    'W1': W1.tolist(),
    'b1': b1.tolist(),
    'W2': W2.tolist(),
    'b2': b2.tolist()
}

with open('extra/model_params3.json', 'w') as json_file:
    json.dump(params, json_file)
