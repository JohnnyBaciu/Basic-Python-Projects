from PIL import Image, ImageOps, ImageEnhance
import os

def check_majority_white(image):
    # Convert the image to grayscale
    grayscale_image = ImageOps.grayscale(image)
    
    # Get the pixel data as a list
    pixels = list(grayscale_image.getdata())
    
    # Count the number of bright pixels (assuming bright is 255 in grayscale)
    bright_pixels = sum(1 for pixel in pixels if pixel > 180)  # Adjust threshold as needed
    
    # Check if the majority of pixels are bright
    if bright_pixels > len(pixels) * 0.4:
        return True  # Majority of pixels are bright
    else:
        return False  # Majority of pixels are not bright (inverted case)

def convert_to_black_and_white(input_image_path, output_image_path):
    # Open the image
    image = Image.open(input_image_path)
    
    # Check if the majority of pixels are bright
    if check_majority_white(image):
        # Invert the image
        inverted_image = ImageOps.invert(image)
        inverted_image = inverted_image.convert("L")  # Convert to grayscale
        threshold = 128  # Threshold value (adjust as needed)
        thresholded_image = inverted_image.point(lambda p: 0 if p < threshold else 255, '1')  # Apply thresholding
        thresholded_image.save(output_image_path, 'PNG')
    else:
        # Save the image as PNG format (no inversion needed)
        image.save(output_image_path, 'PNG')

def resize_to_28x28(input_image_path, output_image_path):
    # Open the image
    image = Image.open(input_image_path)
    
    # Crop the image to a square with an aspect ratio of 1:1
    width, height = image.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2
    cropped_image = image.crop((left, top, right, bottom))
    
    # Save the cropped image to a temporary path for processing
    temp_path = os.path.splitext(output_image_path)[0] + '_temp.png'
    cropped_image.save(temp_path, 'PNG')  # Save as PNG format
    if cropped_image.mode != 'RGB':
        cropped_image = cropped_image.convert('RGB')
    # Enhance contrast and exposure
    enhanced_image = ImageEnhance.Brightness(cropped_image).enhance(1.2)  # Increase exposure by a factor of 1.2
    enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(1.7)  # Increase contrast by a factor of 1.5
    threshold = 123  # Threshold value (adjust as needed)
    enhanced_image = enhanced_image.point(lambda p: p-p*0.7 if p <= threshold else p+p*0.7)
    # Resize the enhanced image to 28x28 pixels
    resized_image = enhanced_image.resize((28, 28))
    resized_image = resized_image.convert("L")  # Convert to grayscale
    tthreshold = 200  # Threshold value (adjust as needed)
    resized_image = resized_image.point(lambda p: p+p*0.7 if p >= tthreshold else p-p*0.7)
    resized_image.save(output_image_path, 'PNG')

    # Remove the temporary cropped image file
    os.remove(temp_path)

# Example usage
labels = []
folder = 'extra/numbers/'
# First, perform the initial cropping and save to a temporary path
for filename in os.listdir(folder):
    label = int(filename.split('_')[0])  # Extract label from filename
    labels.append(str(label))
for filename in range(len(os.listdir(folder))):
    input_image_path = folder + os.listdir(folder)[filename]  # Replace with the path to your input image
    output_image_path = folder +os.listdir(folder)[filename].split('.')[0] +'_id1.png'  # Replace with the desired output path and filename    
    resize_to_28x28(input_image_path, output_image_path)
    print(input_image_path, output_image_path)
     #Then, convert the cropped and resized image to black and white and save to the output path
    convert_to_black_and_white(output_image_path, output_image_path)
