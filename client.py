import pygame
import random
import time
import socket
from network import Network
pygame.init()

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
        self.updateflag = False
        self.wait = False
        self.shooting = False
        self.shot = False #checks if bullet was shot
        self.facing = 2 #left 1, right 2, up 3, down 4
        self.color = (155, 155, 89)
        self.x = start[1]
        self.y = start[1]
        self.rect = n.p[0]
        self.player2 = None
        self.end = False
        #gun
    
        self.gun = [start[1]+10, start[1], (self.screen_size/20-(self.line_width+5))/2, (self.screen_size/20-(self.line_width+5))]
        self.bulletxdir = 1
        self.bulletydir = 1
        self.bulletx = -100
        self.bullety = -100
        self.one_shot = False
        self.bulletobj = pygame.Rect(-100, -100, (self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5)))
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
                    pygame.quit()
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
        if self.updateflag == True:
            self.player2 = self.player2.strip(')(').split(', ')
            x = int(self.player2[0])
            y = int(self.player2[1])
            xx = int(self.player2[2])
            yy= int(self.player2[3])
            f= int(self.player2[4])

            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, (self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5))))
            if f == 1:
                pygame.draw.rect(self.screen,(0,0,0), (x, y, (self.screen_size/20-(self.line_width+5))/2, (self.screen_size/20-(self.line_width+5))))
            if f == 2:
                pygame.draw.rect(self.screen,(0,0,0), (x+10, y, (self.screen_size/20-(self.line_width+5))/2, (self.screen_size/20-(self.line_width+5))))
            if f ==3:
                pygame.draw.rect(self.screen,(0,0,0), (x, y, (self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5))/2))
            if f == 4:
                pygame.draw.rect(self.screen,(0,0,0), (x, y+10, (self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5))/2))
            pygame.draw.rect(self.screen,(0,0,255), (xx, yy, (self.screen_size/20-(self.line_width+5)), (self.screen_size/20-(self.line_width+5))))
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
    #checks if there is only one player that needs to wait
    def checkplayers(self):
        
        if self.player2 == 'wait':
            self.wait = True
            
            self.updateflag = False
        elif self.player2 != None:
            
            self.wait = False
            self.updateflag = True
        if self.player2 == 'win':
            self.end = True
        if self.player2 =='lose':
            self.end = True
        
    #winlose
    def win(self):
        if self.end == True:
            font = pygame.font.Font('freesansbold.ttf', 64)
            if self.player2 == 'win':
                text = font.render('YOU WIN', True, (0,255,0), (0,0,255))
                textRect = text.get_rect()
                textRect.center = (500 / 2, 500 / 2)
                while True:
                    self.check_quit()
                    self.screen.fill((0, 0, 255))
                    self.screen.blit(text, textRect)
                    pygame.display.update()

            else:
                text = font.render('LOSER', True, (0,255,0), (0,0,255))
                textRect = text.get_rect()
                textRect.center = (500 / 2, 500 / 2)
                while True:
                    self.check_quit()
                    self.screen.fill((255, 0, 0))
                    self.screen.blit(text, textRect)
                    pygame.display.update()
                
    #main
    def main(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('WAITING', True, (0,255,0), (0,0,255))
        textRect = text.get_rect()
        textRect.center = (500 / 2, 500 / 2)
        while self.run:
            self.clock.tick(10)

            if self.wait == False:
                
                self.grid()
                self.check_quit()
                self.foodgen()
                self.move()
                self.bullet()
                self.player2 = n.send([self.x, self.y, self.bulletx, self.bullety, self.facing])
                self.checkplayers()
                self.win()
                self.update()  
            else:
                
                self.check_quit()
                self.screen.blit(text, textRect)
                pygame.display.update()
                self.player2 = n.send([self.x, self.y, self.bulletx, self.bullety, self.facing])
                self.checkplayers()
 
n = Network()
start = n.getP()
main = Main()
main.main()