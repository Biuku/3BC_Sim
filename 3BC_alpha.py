""" April 7, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

    Below starting point is the final version of 01. preAlpha > _03_animeTest.py, which was a POC of a running player on a field,
    calibrated so the runner traverses the field at about the speed of a high school baseball player. Achieving this is the gate 
    for moving from POC to Alpha.  
    The next steps (the first Alpha steps):
        - Refactor this streamlined POC code -- all in one program -- to OOP with modules
        - Begin using Git / Github
        - Add 9 defensive players and roles/actions in about 21 defensive situations. Confirm PyGame can manage these animations etc. without lagging
        (or, look into threading)
    """

import pygame
from pygame.locals import *
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0

## Modules
from man import Man

pygame.init()
w = 3400   #3400 = optimal for my widescreen
h = 1350
screen = pygame.display.set_mode((w, h))
exit = False

### Clock 
clock = pygame.time.Clock()
fps = 45

### Screen setup
colour_bk = (255, 255, 255)

### Graphics setup
diamond = pygame.image.load("images/diamond_1.png")  

### Animation setup
x = 200
y = 200

men = []

for i in range(0, 1000, 50):
    _man = Man(screen, x+i, y+(i//2))
    men.append(_man)

#man1 = Man(screen, x, y)
#man2 = Man(screen, x-50, y-200)

# Movement toggles
left = False
right = False
north = False
south = False

### ***** MAIN LOOP ***** ###

while not exit:
    
    clock.tick(fps)
    
    ## Draw background objects
    screen.fill(colour_bk)
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

    #man1.move(left, right, north, south)
    #man2.move(left, right, north, south)

    for _man in men:
        _man.move(left, right, north, south)

    pygame.display.update()
    