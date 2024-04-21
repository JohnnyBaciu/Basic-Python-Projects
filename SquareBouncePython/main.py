import pygame
import random
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)
collisions = 0
text = font.render(f'{collisions}', True, (0,255,0), (0,0,255))
hihi = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
a = random.uniform(0.000, 9.234)
b = random.uniform(0.000, 9.234)
c = random.uniform(0.000, 9.234)
width = random.randint(500, 1000)
height = random.randint(500, 700)
positions = []
pixelsquare = pygame.image.load('C:\PythonProjects\SQAUREBOUNCE\purple-square-9.png')
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
cone = random.randint(0, 100)
ctwo = random.randint(0, 100)
cthree = random.randint(0, 100)
colorz = []
clientNumber = 0


class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xvel = random.uniform(4.0100, 8.9999999)
        self.yvel = random.uniform(4.0100, 8.9999999)

    def draw(self, win):
        text = font.render(f'Collisions: {collisions}', True, (0,255,0), (0,0,255))
        textRect = text.get_rect()
        textRect.center = (115, 20)
        global a, b, c
        global cone, ctwo, cthree
        positions.append((self.x+50, self.y+50))
        win.blit(text, textRect)
        win.blit(pixelsquare,(self.x, self.y))
        cone+=a
        ctwo+=b
        cthree+=c
        if cone > 245:
            a=a*-1
        if ctwo > 245:
            b=b*-1
        if cthree > 245:
           c=c*-1
            
        if cone < 1:
            a=a*-1
        if ctwo < 1:
            b=b*-1
        if cthree < 1:
            c=c*-1
        
        
        colorz.append((int(cone), int(ctwo), int(cthree)))
        for count, locations in enumerate(positions):
            try:
                pygame.draw.circle(win, colorz[count], locations, 7)
            
            except:
                pygame.draw.circle(win, colorz[count-5], locations, 7)
    def move(self):
        global collisions
        if self.x < 1 or self.x > width - 101:
            self.xvel = -self.xvel
            collisions +=1
            #self.xvel += random.randint(-1, 1)

        if self.y < 1 or self.y > height-101:
            self.yvel = -self.yvel
            collisions +=1
            #self.yvel += random.randint(-1, 1)

        self.x -= self.xvel
        self.y += self.yvel

        
        


def redrawWindow(win,player):
    win.fill(hihi)
    player.draw(win)
    pygame.display.update()


def main():
    run = True
    p = Player(50,50)
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p)

main()  
