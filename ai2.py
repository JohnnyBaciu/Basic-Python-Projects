import mnist
import numpy as np
import json

# Load saved weights and biases from JSON file
with open("C:/PythonProjects/extra/NUMBER_NN/model_params3.json", 'r') as json_file:
    params = json.load(json_file)

def forward_propagation(X):
    # Compute activations for the hidden layer
    Z1 = np.dot(X, W1_loaded) + b1_loaded
    A1 = np.maximum(0, Z1)  # ReLU activation
        
    # Compute activations for the output layer
    Z2 = np.dot(A1, W2_loaded) + b2_loaded
    A2 = np.exp(Z2 - np.max(Z2, axis=1, keepdims=True)) / np.sum(np.exp(Z2 - np.max(Z2, axis=1, keepdims=True)), axis=1, keepdims=True)  # Softmax activation
        
    return A2

W1_loaded = np.array(params['W1'])
b1_loaded = np.array(params['b1'])
W2_loaded = np.array(params['W2'])
b2_loaded = np.array(params['b2'])

X_train = mnist.test_images()
Y_train = mnist.test_labels()
Y_train = Y_train.astype(np.int32)
X_train = X_train.reshape(-1, 28*28) / 255.0

sum_correct = 0
total_samples = 0
confidence_values = []  # List to store confidence values for each prediction

for count, image in enumerate(X_train):
    # Perform forward propagation to get predictions
    predictions = forward_propagation(image)
    predicted_class = np.argmax(predictions)
    confidence = predictions[0][predicted_class] * 100  # Confidence value as a percentage
    
    # Display the prediction and confidence
    print(f'Number: {count+1}')
    print(f'Predicted Digit Class: {predicted_class}')
    print(f'Actual Digit Class: {Y_train[count]}')
    print(f'Confidence: {confidence:.2f}%')  # Display confidence as a percentage with 2 decimal places
    
    # Calculate accuracy
    if predicted_class == Y_train[count]:
        sum_correct += 1
    total_samples += 1
    
    # Store confidence value
    confidence_values.append(confidence)

# Calculate accuracy
accuracy = (sum_correct / total_samples) * 100
print(f'Accuracy: {accuracy:.2f}%')  # Display accuracy as a percentage with 2 decimal places

# Calculate average confidence across all predictions
average_confidence = np.mean(confidence_values)
print(f'Average Confidence: {average_confidence:.2f}%')  # Display average confidence as a percentage with 2 decimal places
