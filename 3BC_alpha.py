""" April 8, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

    Today, got started on the 'arrondissement map' with 4 bases + pitcher's rubber in place, and 3 OF positions -- standard OF positioning. The other locations can iterate off those centroids

    But major thing was drilling into Pygame 'rect's and collision detection. Successfully got it working -- my baserunner got now walks with a thin white outline (to be removed later), 
    but when he collides with a base that outline turns thick and red. 

    Getting my head around Pygame Rect's took some effort -- glad to have broken the back of it.

    Now, it should be trivial to place fielders in their positions, and to create a ball that can be caught, etc. 

    Once all that is in place, it will start to get fun -- encoding various baseball situations, where each fielder goes, what each baserunner's last obtained base is, etc. 

    """

import pygame
from pygame.locals import *
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0

## Import modules
from man import Man
#from arrondissements import Arrondissements

#### Initialize pygame and screen

pygame.init()
w = 3400 #= optimal for my widescreen
h = 1350
screen = pygame.display.set_mode((w, h))
exit = False

# Game clock 
clock = pygame.time.Clock()
fps = 45

# Screen setup
colour_black = (0, 0, 0)
colour_white = (255, 255, 255)
colour_darkGray = (60, 60, 60)
colour_midGray = (120, 120, 120)
colour_lightGray = (180, 180, 180)
colour_red = (255, 0, 0)
arrondissements_font = pygame.font.Font('freesansbold.ttf', 20)

# Graphics setup
diamond = pygame.image.load("images/diamond_1.png")  

## Instantiate bases 
    # Rect = left, top, width, height

centre_line_x = 938
middle_line_y = 1042
base_size = 25

base_1 = pygame.Rect(1118, middle_line_y, base_size, base_size)
base_2 = pygame.Rect(centre_line_x, 868, base_size, base_size)
base_3 = pygame.Rect(758, middle_line_y, base_size, base_size)
base_4 = pygame.Rect(centre_line_x, 1220, base_size, base_size)
pitchers_rubber = pygame.Rect(938, 1042, base_size, 7)

bases = [base_1, base_2, base_3, base_4]

one_B = (1118, middle_line_y)
two_B = (centre_line_x, 868)
three_B = (758, middle_line_y)
home_B = (centre_line_x, 1220)
rubber = (938, 1042)

mid_depth_OF = 550
LF = (550, mid_depth_OF)
CF = (938, 350)
RF = (1350, mid_depth_OF)


## Create OF arrondissements 
def draw_arrondissements():


    circle_size = 40 
    pygame.draw.circle(screen, colour_lightGray, LF, circle_size) # LF
    pygame.draw.circle(screen, colour_lightGray, CF, circle_size) # CF
    pygame.draw.circle(screen, colour_lightGray, RF, circle_size) # RF

    # Draw the position letters for each position
    position = ["7", "8", "9"]
    coord = [LF, CF, RF]
    for i, pos in enumerate(position):
        text = arrondissements_font.render(pos, True, colour_black)
        textRect = text.get_rect()    
        textRect.center = coord[i]
        screen.blit(text, textRect)


### Create fielders
# Animation setup
x = w//3 #850 
y = 1100

#### Instantiate objects #### 
# Instantiate characters
steps = 10

baserunner = Man(screen, x, y, "baserunner")
f1 = Man(screen, rubber[0]-5, rubber[1]-(2.5*steps), "fielder")
f2 = Man(screen, home_B[0]-5, home_B[1]+(3*steps), "fielder")
f3 = Man(screen, one_B[0]-(1.8*steps), one_B[1]-(7*steps), "fielder")
f4 = Man(screen, two_B[0]+(9*steps), two_B[1]-(.8*steps), "fielder")
f5 = Man(screen, three_B[0]+(2*steps), three_B[1]-(7*steps), "fielder")
f6 = Man(screen, two_B[0]-(12*steps), two_B[1]+(1*steps), "fielder")
f7 = Man(screen, LF[0], LF[1], "fielder")
f8 = Man(screen, CF[0], CF[1], "fielder")
f9 = Man(screen, RF[0], RF[1], "fielder")

men = [f1, f2, f3, f4, f5, f6, f7, f8, f9 ] 


## Movement toggles
left = False
right = False
north = False
south = False

# Show arrondissements toggle
show_arrondissements = False

#### ***** MAIN LOOP ***** ####


while not exit:
    
    clock.tick(fps)
    
    ## Draw background objects
    screen.fill(colour_white)
    screen.blit(diamond, (10, 10))

    ### Events ### 

    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            exit = True

        ## Runner movement events
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                exit = True

            if event.key == K_LEFT or event.key == K_KP4:
                left = True
            
            if event.key == K_RIGHT or event.key == K_KP6:
                right = True
                
            if event.key == K_UP or event.key == K_KP8:
                north = True
            
            if event.key == K_DOWN or event.key == K_KP2:
                south = True
                
            if event.key == K_KP7:
                north = True
                left = True       
                
            if event.key == K_KP9:
                north = True
                right = True
                                 
            if event.key == K_KP3:
                south = True
                right = True
                                
            if event.key == K_KP1:
                south = True
                left = True
                
            if event.key == K_a:
                show_arrondissements = not(show_arrondissements)
                  
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_KP4:
                left = False   
        
            if event.key == K_RIGHT or event.key == K_KP6:
                right = False
                
            if event.key == K_UP or event.key == K_KP8:
                north = False
            
            if event.key == K_DOWN or event.key == K_KP2:
                south = False
                
            if event.key == K_KP7:
                north = False
                left = False      
                
            if event.key == K_KP9:
                north = False
                right = False
                                 
            if event.key == K_KP3:
                south = False
                right = False   
                                 
            if event.key == K_KP1:
                south = False
                left = False

    if show_arrondissements:
        draw_arrondissements()
        for base in bases:
            pygame.draw.rect(screen, colour_black, base)
    
    for man in men:
        man.move(left, right, north, south)
        man.detect_collisions(bases)

    pygame.display.update()
    