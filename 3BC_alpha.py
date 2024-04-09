""" April 8, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

    Focused on implementing fielders in correct positions, ultimately to move correctly in various defensive situations.

    Key step: implementing an 'arrondissement' map of 36 field locations to make it easier to determine where a ball is hit, and where defensive players should go 

    OKAY -- I'M GOING TO TRY BASING OBJECTS OFF PYGAME'S SPRITE METHOD, WHICH WILL TAKE A BIT OF RE-WORK, BUT SHOULD SIMPLIFY COLLISSION DETECTION AND OTHER THINGS.
    Will commit the current version before trying this 
   
    """

import pygame
from pygame.locals import *
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0

## Import modules
from man import Man

#### Initialize pygame and screen

pygame.init()
w = 3400   #3400 = optimal for my widescreen
h = 1350
screen = pygame.display.set_mode((w, h))
exit = False

# Game clock 
clock = pygame.time.Clock()
fps = 45

# Screen setup
colour_black = (0, 0, 0)
colour_white = (255, 255, 255)
colour_midGray = (120, 120, 120)

# Graphics setup
diamond = pygame.image.load("images/diamond_1.png")  

# Animation setup
x = w//4
y = 1100


#### Instantiate objects #### 

# Instantiate characters
baserunner = Man(screen, x, y, "baserunner")
fielder = Man(screen, x-50, y-200, "fielder")

# Instantiate bases 
# Rect = left, top, width, height

base_1 = pygame.Rect(1118, 1042, 25, 25)
base_2 = pygame.Rect(938, 868, 25, 25)
base_3 = pygame.Rect(758, 1042, 25, 25)
base_4 = pygame.Rect(938, 1220, 25, 25)
base_rubber = pygame.Rect(938, 1042, 25, 7)

# Instantiate 



# Movement toggles
left = False
right = False
north = False
south = False

### ***** MAIN LOOP ***** ###

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

    baserunner.move(left, right, north, south)
    fielder.move(left, right, north, south)


    pygame.draw.rect(screen, colour_black, base_1)
    pygame.draw.rect(screen, colour_black, base_2)
    pygame.draw.rect(screen, colour_black, base_3)
    pygame.draw.rect(screen, colour_black, base_4)
    pygame.draw.rect(screen, colour_midGray, base_rubber)

 

    pygame.display.update()
    