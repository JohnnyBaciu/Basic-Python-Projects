import pygame
import random
import time
import threading
window = pygame.display.set_mode((1000, 1000))
curr = 0
curg = 0
curb = 0
t = 0
b = 0
temp = True
def quit():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

quitThread = threading.Thread(target = quit)
quitThread.start()
while True:
    window.fill((0,0,0))
    for y in range(1,1000,4):
        for x in range(1,1000,4):
            temp = random.randint(0,30)
            if temp % 2 == 0:
                t = x
                xe = y
                ye = t
            else:
                xe = x
                ye = y
            if temp%4 == 0 or temp ==1:
                curr = random.randrange(30, 200)
                curg = random.randrange(30, 200)
                curb = random.randrange(30, 200)
                pygame.draw.rect(window, (curr, curg, curb), (xe, ye, 4, 4))
            else:
                pygame.draw.rect(window, (curr, curg, curb), (xe, ye, 4, 4))
            temp = random.randint(0,70)
            if temp == 4:
                curr = 0
                curg = 0
                curb = 0
                pygame.draw.rect(window, (b, b, b), (xe, ye, 4, 4))
    pygame.display.update()
