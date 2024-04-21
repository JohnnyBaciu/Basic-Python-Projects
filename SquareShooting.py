import pygame
import math
import random
pygame.init()
points = 0
startposx = [100, 300]
startposy = [100, 300]
targetmov = [1, -1, 1.12, -1.12]
font = pygame.font.Font('freesansbold.ttf', 32)
start = True
t = 0.1
o = 1.8
oy = 1.4
r = False
posob = False
window = pygame.display.set_mode((400, 400))
pos = []
def quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
def click():
    pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        return pos
randx = random.choice(startposx)
randy = random.choice(startposy)

        
pygame.draw.rect(window, (0,0,0), (randx-10, randy-10, 20, 20))
cloc = pygame.time.Clock()
while True:
    text = font.render(f'{points}', True, (0,199,0), (0,10,199))
    textRect = text.get_rect()
    cloc.tick(60)
    window.fill((10,40,255))
    window.blit(text, textRect)
    quit()
    pygame.draw.rect(window, (200,200,98), (175,175,50,50))
    if start == True:
     
        pygame.draw.rect(window, (0,0,0), (randx-10, randy-10, 20, 20))
        pygame.display.update()
        
    postemp = click()
    if t > 0.1 and r == False:
        
        pygame.draw.rect(window,(255,0,0), ((math.cos(math.radians(realang))*t+195),(math.sin(math.radians(realang*-1))*t+195), 10,10))
        if (math.cos(math.radians(realang))*t+195) < 0 or (math.cos(math.radians(realang))*t+195) > 400 or (math.sin(math.radians(realang*-1))*t+195) > 400 or (math.sin(math.radians(realang*-1))*t+195) < 0:
            t = 0.1
            r = True
    if postemp != None:
        pos = postemp
        t = 0.1
        r = False
        start = False
        posob = False

    
    if start == False:
        randx += o
        randy += oy
        if randy < 10 or randy > 390:
            oy *= -1
        if randx < 10 or randx > 390:
            o *= -1
    if randx -10 < 225 and randx + 10 > 175:
        if randy -10 < 225 and randy + 10 > 175:
            pygame.quit()
    
    if pos:
        
        x = (pos[0]-200)
        y = ((pos[1]-200)*-1)
        try:
            ang = abs(math.degrees(math.atan((y/x))))
        except:
            y=0.1
        realang = 0
        if x < 0 and y > 0:
            realang = 90 + (90-ang)
        if x < 0 and y < 0:
            realang = 180 + ang
        if x > 0 and y < 0:
            realang = 270 + (90-ang)
        if x > 0 and y > 0:
            realang = ang
        t+=6
        #print(math.cos(math.radians(realang))*(math.sqrt(x*x+y*y)), x) #has pythagoreoms theorom
        if  posob == False and int(math.cos(math.radians(realang))*t+215) < randx+25 and int(math.cos(math.radians(realang))*t+215) > randx-1 and int(math.sin(math.radians(realang*-1))*t+215) < randy+30 and int(math.sin(math.radians(realang*-1))*t+215) > randy-1:
            points += 1
            if start == False:
                randx = random.randrange(400)
                randy = random.randrange(400)

            while randx < 225 and randx > 175 and randy < 225 and randy > 175:
                randx = random.randrange(400)
                randy = random.randrange(400)
            while randx < 10 or randx > 390 or randy < 10 or randy > 390:
                randx = random.randrange(400)
                randy = random.randrange(400)
            o = o * random.choice(targetmov)
            oy = oy * random.choice(targetmov)
            
            posob = True
        
        pygame.draw.rect(window, (0,0,0), (randx-10, randy-10, 20, 20))
       # pygame.draw.line(window,(0,0,0),(200,200), pos)

    pygame.display.update()