import pygame
import time
import math
import threading
pygame.init()
it = 200
raditeration = 90
sinpoints = []
sinepoints2 = []
window_size = (1700, 1000)
window = pygame.display.set_mode(window_size)

def drawcircle():
    window.fill((70, 155, 70))
    pygame.draw.circle(window, (0,0,0), (200,200), 150, 5)
    pygame.draw.line(window, (0,0,0), (200, 50), (200, 350), 5)
    pygame.draw.line(window, (0,0,0), (50,200), (350,200), 5)
    for hour in range(1, 13):
        hour_angle = math.radians(hour * 30)
        hour_x = int(150 * math.sin(hour_angle)+200)
        hour_y = int(150 * math.cos(hour_angle)+200)
        pygame.draw.circle(window, (0,0,0), (hour_x, hour_y), 5)
        pygame.draw.line(window, (0,20,0), (200,200), (hour_x,hour_y), 1)

        
def quit():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
def drawrad(raditeration, it):
    x = 150 * (math.sin(math.radians(raditeration)))
    y = 150 * (math.cos(math.radians(raditeration)))
    
    pygame.draw.line(window, (0,0,0), (200, 200), (x+200,y+200 ), 5)
   # pygame.draw.line(window,(0,0,0), (x+200,y+200 ), (x+200, 200),5)
    pygame.draw.line(window,(0,0,0), (x+200,y+200 ), (it, y+200),5)
   # pygame.draw.line(window,(0,0,0), (x+200,y+200 ), (x+200, it),5)


    raditeration += 1
    sinpoints.append((it, y+200))
    sinepoints2.append((x+200, it))
    for point in sinpoints:
        pygame.draw.circle(window, (0,0,0), (point[0], point[1] ), 2)
   # for point in sinepoints2:
      #  pygame.draw.circle(window, (0,0,0), (point[0], point[1] ), 2)

    
    return raditeration

THread = threading.Thread(target=quit)
THread.start()
while True:
    drawcircle()
    raditeration = drawrad(raditeration, it)
    if raditeration == 360:
        raditeration = 0
    it+=2
    pygame.display.update()
