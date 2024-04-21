import pygame
pygame.init()
class Main():
    def __init__(self):
        self.window_width = 500
        self.window_height = 500
        self.window = pygame.display.set_mode((500, 500))
        self.loop_flag = True
        self.x = self.window_width/5
        self.y = self.window_width/5
        self.player = pygame.Rect((self.x, self.y, self.window_width/5, self.window_height/5))
        self.color = (255, 255, 255)
        self.vel = 4
        self.coordupdate = 0
        self.coordupdate2 = 0
        self.clock = pygame.time.Clock()
        self.gravacc = 0 
        self.gravaccc = 0
        self.ob = 325
        self.up = False
        self.c2 = 1
        self.down = 4.4
        self.h = 0.3
        self.rise = 0.0001
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.green=(0,255,0)
        self.blue = (0,0,255)
        self.text = self.font.render('0', True, self.green, self.blue)
        self.textRect = self.text.get_rect()
        self.obstacle = pygame.Rect((self.ob, 490, 10, 10))
        self.ppooints = 0
    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_flag = False
    def update(self):
        self.window.fill((144,32, 14))
        self.window.blit(self.text, self.textRect)
        self.player = pygame.Rect(((self.x - self.coordupdate), self.y, (self.window_width/5), (self.window_height/5)))
        self.obstacle = pygame.Rect((self.ob- self.coordupdate2, 490, 10, 10))
                        
        pygame.draw.rect(self.window, self.color, self.player)
        pygame.draw.rect(self.window, self.color, self.obstacle)
        pygame.display.update()
    def move(self):
        Key = pygame.key.get_pressed()
        if Key[pygame.K_a] and self.x > self.window_width-self.window_width:
            if self.y < 405:
                self.x -= self.vel/1.7
            else:
                self.x -= self.vel
            pygame.time.delay(10)
        if Key[pygame.K_d] and self.x < self.window_width - self.window_width/5+ self.coordupdate:
            if self.y < 405:
                self.x += self.vel/1.7
            else:
                self.x += self.vel
                pygame.time.delay(10)
        
        if Key[pygame.K_w] and self.up == False and self.y >399 and self.y <499:
            self.up = True
            pygame.time.delay(10)
      
        
        self.player = pygame.Rect((self.x, self.y, (self.window_width/5), (self.window_height/5)))

    def gravity(self):
        if self.y < 400:
            self.gravaccc = 3 + self.gravacc
            self.y += self.gravaccc
            
            self.gravacc += 0.01
            self.gravaccc = 3 + self.gravacc
        
        if self.y > 399:
            self.gravacc = 0
            self.gravaccc = 0
    def end_game(self):
        if self.x-self.coordupdate < -99:
            self.loop_flag = False
        self.player = pygame.Rect((self.x, self.y, (self.window_width/5), (self.window_height/5)))
        if (self.ob-self.coordupdate2) > (self.x-self.coordupdate) and (self.ob-self.coordupdate2+10) < (self.x-self.coordupdate + 100): 
            if self.y > 399:
                self.loop_flag = False
    def move_window(self):
        self.coordupdate +=1
        self.coordupdate2 +=self.c2
    def obrep(self):
        if self.ob-self.coordupdate2 < -10:
            self.c2 += self.h
            
            self.ob += 536
            self.ppooints += 1
            self.text = self.font.render(f'{self.ppooints}', True, self.green, self.blue)
            self.obstacle = pygame.Rect((self.ob, 490, 10, 10))
            
    def upp(self):
        self.y -= self.down - self.rise
        if self.gravaccc > 4.4:
            self.up = False
            self.down = 4.4
            self.rise = 0
            
        self.down -= 0.009
        self.rise = self.rise*self.rise 
        self.player = pygame.Rect((self.x, self.y, (self.window_width/5), (self.window_height/5)))
    def main_loop(self):
        self.window.blit(self.text, self.textRect)
        while self.loop_flag:
            self.clock.tick(60)
            self.check_quit()
            self.move()
            if self.up == True:
                self.upp()
            self.gravity()
            self.move_window()
            self.obrep()
            self.update()
            self.end_game()
            
if __name__ == '__main__':
    main = Main()
    main.main_loop()
    # 
