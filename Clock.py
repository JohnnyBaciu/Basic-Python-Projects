import pygame
import time
import math
import threading
pygame.init()

# Set up the clock display window
window_size = (400, 400)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Clock")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up the clock face
clock_face_radius = 150
clock_face_center = (200, 200)

# Set up the clock hands
hour_hand_length = 80
minute_hand_length = 120
second_hand_length = 140

# Set up the font for the time display
font = pygame.font.SysFont('arial', 30)

def draw_clock_face():
    # Draw the outer circle
    pygame.draw.circle(window, black, clock_face_center, clock_face_radius, 5)

    # Draw the hour tick marks
    for hour in range(1, 13):
        hour_angle = math.radians(hour * 30)
        hour_x = int(clock_face_center[0] + (clock_face_radius - 20) * math.sin(hour_angle))
        hour_y = int(clock_face_center[1] - (clock_face_radius - 20) * math.cos(hour_angle))
        pygame.draw.circle(window, black, (hour_x, hour_y), 5)

    # Draw the minute tick marks
    for minute in range(0, 60, 5):
        if minute % 15 != 0:
            minute_angle = math.radians(minute * 6)
            minute_x = int(clock_face_center[0] + (clock_face_radius - 10) * math.sin(minute_angle))
            minute_y = int(clock_face_center[1] - (clock_face_radius - 10) * math.cos(minute_angle))
            pygame.draw.circle(window, black, (minute_x, minute_y), 2)

    # Draw the center point
    pygame.draw.circle(window, black, clock_face_center, 10)
    
def draw_clock_hands(hour, minute, second):
    # Calculate the angles of the hands
    hour_angle = math.radians((hour % 12) * 30 + minute / 2)
    minute_angle = math.radians(minute * 6)
    second_angle = math.radians(second * 6)

    # Draw the hour hand
    hour_x = int(clock_face_center[0] + hour_hand_length * math.sin(hour_angle))
    hour_y = int(clock_face_center[1] - hour_hand_length * math.cos(hour_angle))
    pygame.draw.line(window, black, clock_face_center, (hour_x, hour_y), 10)

    # Draw the minute hand
    minute_x = int(clock_face_center[0] + minute_hand_length * math.sin(minute_angle))
    minute_y = int(clock_face_center[1] - minute_hand_length * math.cos(minute_angle))
    pygame.draw.line(window, black, clock_face_center, (minute_x, minute_y), 5)

    # Draw the second hand
    second_x = int(clock_face_center[0] + second_hand_length * math.sin(second_angle))
    second_y = int(clock_face_center[1] - second_hand_length * math.cos(second_angle))
    pygame.draw.line(window, white, clock_face_center, (second_x, second_y), 1)
 
def draw_time(hour, minute, second):
    # Convert the time to a string
    time_string = '{:02d}:{:02d}:{:02d}'.format(hour, minute, second)
    
    # Render the time as text
    text = font
def quit():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

hour = 0
minute = 0
second = 0
THread = threading.Thread(target=quit)
THread.start()
clocke = pygame.time.Clock()
while True == True:
    window.fill((255, 65, 144))
    draw_clock_face()
    draw_clock_hands(hour, minute, second)
    draw_time(hour, minute, second)
    pygame.display.update()
    #time.sleep(1)
    
    second+=1
    if second == 60:
        second = 0
        minute +=1
    if minute == 60:
        minute = 0
        hour +=1