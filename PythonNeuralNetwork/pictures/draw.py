import pygame
import sys
import json
import threading
import time
from PIL import Image

# Initialize Pygame
pygame.init()

# Set up the screen
cell_size = 15  # Size of each cell in the grid
width, height = 600, 600
grid_width, grid_height = 28, 28  # Define the grid dimensions
grid_size_x, grid_size_y = width // grid_width, height // grid_height
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drawing Pad")

# Fill the screen with white initially
screen.fill((255, 255, 255))

# Variables for drawing
drawing = False
last_pos = None

# Lock for threading
lock = threading.Lock()

def save_screen_to_json():
    global lock
    while True:
        lock.acquire()
        grid_data = []

        for grid_y in range(grid_height):
            for grid_x in range(grid_width):
                cell_data = 0
                sum_brightness = 0  # Sum of brightness values for pixels in the grid unit
                count = 0  # Count of pixels in the grid unit
                for y in range(grid_size_y):
                    for x in range(grid_size_x):
                        pixel_color = screen.get_at((grid_x * grid_size_x + x, grid_y * grid_size_y + y))[:3]
                        brightness = sum(pixel_color) // 3  # Average brightness (grayscale value)
                        sum_brightness += brightness
                        count += 1
                if count > 0:
                    average_brightness = sum_brightness // count
                    cell_data = average_brightness  # Analog value based on average brightness
                    if cell_data < 120:
                        cell_data = 0
                    elif cell_data is not 255:
                        cell_data *= 0.8
                        cell_data = round(cell_data)
                grid_data.append(cell_data)

        with open("extra/DRAWING_NN/screen_state.json", "w") as file:
            json.dump({"pixels": grid_data}, file)
        lock.release()
        time.sleep(0.1)

# Start the thread for continuously saving screen state
save_thread = threading.Thread(target=save_screen_to_json)
save_thread.daemon = True
save_thread.start()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Load grid data from JSON file
            with open("extra/DRAWING_NN/screen_state.json", "r") as file:
                grid_data = json.load(file)["pixels"]

            # Create image from grid data
            image = Image.new("L", (28, 28))  # Create a grayscale image
            pixels = image.load()
            for i, pixel_value in enumerate(grid_data):
                x = i % 28
                y = i // 28
                pixels[x, y] = pixel_value

            # Save image as PNG file
            image.save("extra/DRAWING_NN/drawing.png")
            print("Image saved as drawing.png")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                drawing = True
                last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                new_pos = event.pos
                pygame.draw.line(screen, (0, 0, 0), last_pos, new_pos, cell_size)  # Draw black lines
                last_pos = new_pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                screen.fill((255, 255, 255))  # Clear screen with white

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
