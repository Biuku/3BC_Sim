import pygame
from pygame.locals import *
import random

pygame.init()
w = 3400   #3400 = optimal for my widescreen
h = 1350
screen = pygame.display.set_mode((w, h))

colour_black = (0, 0, 0)
colour_white = (255, 255, 255)
colour_midGray = (120, 120, 120)
colour_red = (255, 0, 0)
colour_magenta = (255, 0, 255)


colours = ["crimson", "chartreuse", "coral", "darkorange", "forestgreen", "lime", "navy"]

x = 800
y = 600
clock = pygame.time.Clock()
FPS = 60


rect_1 = pygame.Rect(200, 100, 150, 100)
rect_1.width = 400
rect_1.height = 150

###Creating a rect from an image
man = pygame.image.load("images/baserunners/man_left_1.png").convert_alpha()
rect_2 = man.get_rect()
rect_2.topleft = (200,200)
#rect_2.center = (200,200)



"""
class Square(pygame.sprite.Sprite):
    def __init__(self, col, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.x = x
        self.y = y 
        self.image = pygame.Surface((50, 50))
        self.image.fill(self.col)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    
    def update(self):
        self.rect.move_ip(0, 5)


square = Square("crimson", x, y)

squares = pygame.sprite.Group()
#squares.add(square)

print(squares)
"""

exit = False

while not exit:

    clock.tick(FPS)

    screen.fill(colour_white)

    pygame.draw.rect(screen, colour_magenta, rect_1, 4 )
    pygame.draw.rect(screen, (0, 255, 255), rect_2)

    # First you position the rect (invisible normally), then you blit the img to there
    screen.blit(man, rect_2)

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        rect_2.x -= 5        
    if key[pygame.K_d] == True:
        rect_2.x += 5
    if key[pygame.K_w] == True:
        rect_2.y -= 5
    if key[pygame.K_s] == True:
        rect_2.y += 5




    #squares.update()
    #squares.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            ## Get mouse coord
            pos = pygame.mouse.get_pos()

            square = Square(random.choice(colours), pos[0], pos[1])
            squares.add(square)
        """
    pygame.display.update()
