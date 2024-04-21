import pygame
import math
pygame.init()
class Main():
    def __init__(self):
        self.window_size = (1000,1050)
        self.win = pygame.display.set_mode(self.window_size)
        self.font = pygame.font.Font('freesansbold.ttf', 100)

        self.squares_number = 2
        self.size = [60,140]
        self.bg_color = (80,90,100)
        self.text = self.font.render('0', True, (0,255,0), (0,0,255))

        self.color = [(58,0,90), (0,0,255)]
        self.squares = []
        self.mass = [500,10000]
        self.textRect = self.text.get_rect()
        self.ppooints = 0
        self.green = (0,255,0)
        self.velocity = []
        self.pos = [[0,0],[0,0]]
        self.draw()
        self.m2 = 0
        self.m1 = 0 
        self.v2i = 0
        self.hjk = [0,0]
        self.v1i = 0
    def draw(self):
        pygame.draw.rect(self.win, self.color[0], (0, self.window_size[0]-100, self.window_size[0], 100))
        for x in range(self.squares_number):
            self.squares.append(pygame.draw.rect(self.win, (255,0,0), (400*(x+1), (self.window_size[0]-self.size[x]-100), self.size[x], self.size[x])))
            self.pos[x][0] = 400*(x+1)
            self.pos[x][1] = (self.window_size[0]-self.size[x]-100)
            self.velocity.append(0)
            if x == 1:
                self.velocity[1] = -2
    def update(self):
        self.win.fill(self.bg_color)
        self.win.blit(self.text, self.textRect)
        pygame.draw.rect(self.win, (0,0,0), (0, self.window_size[0]-100, self.window_size[0], 100))

        for x in range(self.squares_number):                
            # Check if any square hit the wall
            if self.pos[x][0] <= 1:
                self.velocity[x] *= -1 # Reverse velocity to bounce off the wall
                self.ppooints +=1
                self.text = self.font.render(f'{self.ppooints}', True, self.green, (0,0,255))

            if self.pos[x][0] >= self.window_size[0]-self.size[x]:
                self.velocity[x] = -abs(self.velocity[x])  # Reverse velocity to bounce off the wall

                self.ppooints +=1

                self.text = self.font.render(f'{self.ppooints}', True, self.green, (0,0,255))
            self.pos[x][0] += self.velocity[x]
            self.hjk[x]+=self.velocity[x]/self.size[x]*3.14
            pygame.draw.ellipse(self.win, self.color[x], (self.pos[x][0], self.pos[x][1], self.size[x], self.size[x]))
            pygame.draw.ellipse(self.win, (0,255,0), (self.pos[x][0]+0.5*self.size[x]+math.cos(self.hjk[x])*self.size[x]/3-(self.size[x]/5)/2, self.pos[x][1]+0.5*self.size[x]+math.sin(self.hjk[x])*self.size[x]/3-(self.size[x]/5)/2, self.size[x]/5, self.size[x]/5))

        # Check for collision between squares
        for i in range(self.squares_number):
            for j in range(i+1, self.squares_number):  # Avoid redundant checks
                if self.check_collision(i, j):
                    self.ppooints +=1
                    self.text = self.font.render(f'{self.ppooints}', True, self.green, (0,0,255))
                    self.resolve_collision(i, j)
                    
            

    def check_collision(self, i, j):
        rect1 = pygame.Rect(self.pos[i][0], self.pos[i][1], self.size[i], self.size[i])
        rect2 = pygame.Rect(self.pos[j][0], self.pos[j][1], self.size[j], self.size[j])
        return rect1.colliderect(rect2)

    def resolve_collision(self, i, j):
        # Separate the colliding squares along the x-axis
        overlap_x = (self.pos[i][0] + self.size[i]) - self.pos[j][0]
        if overlap_x > 0:
            half_overlap_x = overlap_x / 2
            self.pos[0][0] -= half_overlap_x*2
            #self.pos[1][0] += half_overlap_x

    # Calculate final velocities
        self.calculate_final_velocities()
    def calculate_final_velocities(self):
        self.m2 = self.mass[1]
        self.m1 = self.mass[0]
        self.v2i = self.velocity[1]
        self.v1i = self.velocity[0]
        # Kinetic energy conservation equation
        self.v1f = (2 * self.m2 * self.v2i + (self.m1 - self.m2) * self.v1i) / (self.m1 + self.m2)
        self.v2f = (2 * self.m1 * self.v1i + (self.m2 - self.m1) * self.v2i) / (self.m1 + self.m2)

        # Output the results
       
        self.velocity[1] = self.v2f
        self.velocity[0] = self.v1f
        # Verify conservation of kinetic energy and momentum
        KE_initial = 0.5 * self.m1 * self.v1i**2 + 0.5 * self.m2 * self.v2i**2
        KE_final = 0.5 * self.m1 * self.v1f**2 + 0.5 * self.m2 * self.v2f**2

        p_initial = self.m1 * self.v1i + self.m2 * self.v2i
        p_final = self.m1 * self.v1f + self.m2 * self.v2f

    def main_loop(self):
        while True:
            #self.clock.tick(60)
            self.update()
            self.quit_function()
            pygame.display.update()
    def quit_function(self):
        quit_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_flag = True

        if quit_flag == True:
            pygame.quit()
            exit()

if __name__ == '__main__':
    main = Main()
    main.main_loop()
