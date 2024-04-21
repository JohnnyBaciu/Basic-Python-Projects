import numpy as np
import os
import json
from PIL import Image

def guess():
    # Load the model parameters from the JSON file
    with open('model_params4.json', 'r') as json_file:
        params = json.load(json_file)

    W1 = np.array(params['W1'])
    b1 = np.array(params['b1'])
    W2 = np.array(params['W2'])
    b2 = np.array(params['b2'])

    # Define the activation functions (ReLU for the hidden layer and softmax for the output layer)
    def relu(x):
        return np.maximum(0, x)

    def softmax(x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    # Define the forward propagation function using the loaded parameters
    def forward_propagation(X):
        Z1 = np.dot(X, W1) + b1
        A1 = relu(Z1)
        Z2 = np.dot(A1, W2) + b2
        A2 = softmax(Z2)
        return A2, A1

   
    

   
    image_path = "image.png"
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image = image.resize((28, 28))  # Resize to 28x28 pixels
    image_array = abs(np.array(image)-255)  # Normalize pixel values
     # Flatten the image and reshape for forward propagation
    image_flattened = image_array.flatten()
    image_input = image_flattened.reshape(1, -1)  # Reshape to a 1x784 array
    # Perform forward propagation on the chosen image
    output, _ = forward_propagation(image_input)

    # Get the predicted class (assuming output is a one-hot encoded vector)
    predicted_class = np.argmax(output)

    # Get the confidence rates for each class
    confidence_rates = output.squeeze()
    
    if predicted_class == 0:
        predicted_class = 'drums'
    if predicted_class == 0:
        predicted_class = 'sun'
    if predicted_class == 0:
        predicted_class = 'laptop'
    if predicted_class == 0:
        predicted_class = 'anvil'
    if predicted_class == 0:
        predicted_class = 'baseball bat'
    if predicted_class == 0:
        predicted_class = 'ladder'
    if predicted_class == 0:
        predicted_class = 'eyeglasses'
    if predicted_class == 0:
        predicted_class = 'grapes'
    if predicted_class == 0:
        predicted_class = 'book'
    if predicted_class == 0:
        predicted_class = 'dumbell'
    return predicted_class
    
