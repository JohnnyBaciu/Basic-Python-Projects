import pygame
import random
import socket
from network import Network


class Player():
    def __init__(self, player, gun, bullet):
        self.player = eval(str(player).replace('<rect', '').replace('<', '').replace('>', ''))
        self.gun = eval(str(gun).replace('<rect', '').replace('<', '').replace('>', ''))
        self.bullet = eval(str(bullet).replace('<rect', '').replace('<', '').replace('>', ''))
        #self.plaer/gun/bullet (x, y, width, height)
class Main():
    def __init__(self):   
        #window size
        self.screen_size = 500
        #window
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        #run flag
        self.run = True
        #grid lines width
        self.line_width = 2
        #fps clock
        self.clock = pygame.time.Clock()
        #velocity
        self.velocity = 20
        #generate new food or not
        self.food_gen = True
        #food score
        self.score = 0
        #food coords
        self.randfoodx = random.randint(0, 24)
        self.randfoody= random.randint(0, 24)
        #player 
        self.shooting = False
        self.shot = False #checks if bullet was shot
        self.facing = 2 #left 1, right 2, up 3, down 4
        self.color = (155, 155, 89)
        self.x = self.line_width
        self.y = self.line_width
        self.rect = pygame.Rect(self.x, self.y, (self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5)))
        #gun
        self.gun = pygame.Rect(self.x+10, self.y,(self.screen_size/20-(self.line_width+5))/2, (self.screen_size/20-(self.line_width+5)))
        self.bulletxdir = 1
        self.bulletydir = 1
        self.bulletx = self.x
        self.bullety = self.y
        self.one_shot = False
        self.bulletobj = pygame.Rect(-100, -100 ,(self.screen_size/20-(self.line_width+5))/2, (self.screen_size/20-(self.line_width+5)))
    #draw grid
    def grid(self):
        self.screen.fill((255, 255,255))
        for x in range(0, 500, 20):                
            for y in range(0, 500, 20):
                rect1 = pygame.Rect(x,y, self.line_width, self.screen_size)
                rect2 = pygame.Rect(y,x, self.screen_size, self.line_width)
                pygame.draw.rect(self.screen, (0, 0, 0), rect1)
                pygame.draw.rect(self.screen, (0, 0, 0), rect2)
    #check if quit button is pressed
    def check_quit(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False 
    #move
    def move(self):
        Key = pygame.key.get_pressed()
        #up
        if Key[pygame.K_w] and self.y > 20 or Key[pygame.K_UP] and self.y > 20:
            self.y -= self.velocity
            self.gun = pygame.Rect(self.x, self.y,(self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5))/2)
            self.facing = 3
            pygame.time.delay(70)
        #right
        elif Key[pygame.K_d] and self.x <479 or Key[pygame.K_RIGHT] and self.x <479:
            self.x += self.velocity
            self.gun = pygame.Rect(self.x+10, self.y,(self.screen_size/20-(self.line_width+5))/2, (self.screen_size/20-(self.line_width+5)))
            self.facing = 2
            pygame.time.delay(70)
        #down
        elif Key[pygame.K_s] and self.y <479 or Key[pygame.K_DOWN] and self.y < 479:
            self.y += self.velocity
            self.gun = pygame.Rect(self.x, self.y+10,(self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5))/2)
            self.facing = 4
            pygame.time.delay(70)
        #left
        elif Key[pygame.K_a] and self.x > 20 or Key[pygame.K_LEFT] and self.x > 20:
            self.x -= self.velocity
            self.gun = pygame.Rect(self.x, self.y,(self.screen_size/20-(self.line_width+5))/2, (self.screen_size/20-(self.line_width+5)))
            self.facing = 1
            pygame.time.delay(70)
        
        elif Key[pygame.K_SPACE] and self.one_shot == False and self.score > 0:
            self.shot = True
            self.one_shot = True
            pygame.time.delay(70)
            self.score -= 1
        
        self.rect = pygame.Rect(self.x, self.y, (self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5)))
    #update
    def update(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0,0,0), self.gun)
        pygame.display.update()
    #make food and other
    def foodgen(self):
        if self.x == (self.randfoodx*20-18) and self.y == (self.randfoody*20-18):
            self.food_gen = True 
            self.score += 1
        if self.bulletx == (self.randfoodx*20-18) and self.bullety == (self.randfoody*20-18):
            self.food_gen = True 
            self.score += 1
        if self.food_gen == True:
            self.randfoodx = random.randint(1, 25)
            self.randfoody= random.randint(1, 25)
            self.food_gen = False
        
        pygame.draw.rect(self.screen, (0, 0, 0), ((self.randfoodx*20-18), (self.randfoody*20-18), (self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5))))
    #shoot bullet
    def bullet(self):
        if self.shot == True:
            self.bulletx = self.x
            self.bullety = self.y
            if self.facing == 1:
                self.bulletxdir = -1
                self.bulletydir = 0
            if self.facing == 2:
                self.bulletxdir = 1
                self.bulletydir = 0
            if self.facing == 3:
                self.bulletxdir = 0
                self.bulletydir = -1
            if self.facing == 4:
                self.bulletxdir = 0
                self.bulletydir = 1
            self.shooting = True
            self.shot = False
        if self.shooting  == True:
            if self.bulletxdir == -1 and self.bulletydir == 0:
                self.bulletx = self.bulletx - self.velocity
                self.bullety = self.bullety
            if self.bulletxdir == 1 and self.bulletydir == 0:
                self.bulletx = self.bulletx+self.velocity
                self.bullety = self.bullety
            if self.bulletxdir == 0 and self.bulletydir == -1:
                self.bulletx = self.bulletx
                self.bullety = self.bullety-self.velocity
            if self.bulletxdir == 0 and self.bulletydir == 1:
                self.bulletx = self.bulletx
                self.bullety = self.bullety+self.velocity
        if self.shooting == True and self.bulletx > -18 and self.bulletx < 502 and self.bullety > -18 and self.bullety <502:
            self.bulletobj = pygame.draw.rect(self.screen, (0, 0, 255), (self.bulletx, self.bullety, (self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5))))
        else:
            self.shooting = False
            self.shot = False
            self.one_shot = False
    #main
    def main(self, player, player2):
        while self.run:
            self.clock.tick(10)
            self.grid()
            self.check_quit()
            self.foodgen()
            self.move()
            self.bullet()
            self.update()  
            player = Player(self.rect, self.gun, self.bulletobj)
            #player2 = n.send(player)
            
#n = Network()
player = None
player2 = None
main = Main()
main.main(player, player2)
