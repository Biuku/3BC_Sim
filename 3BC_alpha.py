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


pygame.init()
w = 3400   #3400 = optimal for my widescreen
h = 1350
screen = pygame.display.set_mode((w, h))
exit = False

## Clock 
clock = pygame.time.Clock()
fps = 45

#### Screen setup
colour_bk = (255, 255, 255)

#### Graphics setup
diamond = pygame.image.load("images/diamond_1.png")  

### Animation setup

## Load animation frames

# L and R = running left and right 
man_L1 = pygame.image.load("images/man_left_1.png")  
man_L2 = pygame.image.load("images/man_left_2.png") 
man_L3 = pygame.image.load("images/man_left_3.png") 

man_R1 = pygame.image.load("images/man_right_1.png")
man_R2 = pygame.image.load("images/man_right_2.png") 
man_R3 = pygame.image.load("images/man_right_3.png")

# N = North (and also South) -- i.e., toward top / bottom of screen
man_N1 = pygame.image.load("images/man_north_1.png")
man_N2 = pygame.image.load("images/man_north_2.png")
man_N3 = pygame.image.load("images/man_north_3.png")
man_N4 = pygame.image.load("images/man_north_4.png")


## Build 'itertools > cycle' iterators of each frame in an animation to streamline cycling through last to first frame
man_frames_L = cycle([man_L1, man_L1, man_L2, man_L2, man_L3, man_L3]) ## Doubling up frames to better match animation to locomotion without reducing fps to ridiculous level
man_frames_R = cycle([man_R1, man_R1, man_R2, man_R2, man_R3, man_R3])
man_frames_N = cycle([man_N1, man_N1, man_N2, man_N2, man_N3, man_N3, man_N4, man_N4])

## Control the Loadrunner frame rate 
man_frameRate = 0 # Time in miliseconds | 1000 miliseconds = 1 second | 65 seems right for a human runner going full speed
man_curr_frame = next(man_frames_L)

### Movement 
# Movement toggles
left = False
right = False
north = False
south = False
northWest = False
northEast = False
southEast = False
southWest = False

# Man X position
man_x = w//4 +40 # start position
man_y = 1150
man_speed_x = 4/3 # Speed of lateral locomotion -- pixels of movement per frame
man_speed_y = 4/3
man_diagonal_factor = 0.744 ## Diagonal motion is 1.35x faster than North-South or lateral motion. No idea why, but this should equalize that.

""" ***** MAIN LOOP ***** """

while not exit:
    
    clock.tick(fps)
    
 
    screen.fill(colour_bk)
    
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
                northWest = True          
                
            if event.key == K_KP9:
                northEast = True   
                                 
            if event.key == K_KP3:
                southEast = True    
                                
            if event.key == K_KP1:
                southWest = True  
                  
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
                northWest = False          
                
            if event.key == K_KP9:
                northEast = False   
                                 
            if event.key == K_KP3:
                southEast = False    
                                
            if event.key == K_KP1:
                southWest = False  
    

    """03 -- Move the loadrunner L and R with animation"""    
    if left:
        man_curr_frame = next(man_frames_L)
        man_x -= man_speed_x

    if right:   
        man_curr_frame = next(man_frames_R)
        man_x += man_speed_x
            
    if north:   
        man_curr_frame = next(man_frames_N)
        man_y -= man_speed_y
            
    if south:        
        man_curr_frame = next(man_frames_N)
        man_y += man_speed_y

            
    if northWest:
        man_curr_frame = next(man_frames_L)
        man_y -= man_speed_y * man_diagonal_factor
        man_x -= man_speed_x * man_diagonal_factor
            
            
    if northEast:        
        man_curr_frame = next(man_frames_R)
        man_y -= man_speed_y * man_diagonal_factor
        man_x += man_speed_x * man_diagonal_factor
            
    if southEast:        
        man_curr_frame = next(man_frames_R)
        man_y += man_speed_y * man_diagonal_factor
        man_x += man_speed_x * man_diagonal_factor

    if southWest:        
        man_curr_frame = next(man_frames_L)
        man_y += man_speed_y * man_diagonal_factor
        man_x -= man_speed_x * man_diagonal_factor


    #### Draw sprites    
    screen.blit(diamond, (10, 10))
    screen.blit(man_curr_frame, (int(man_x), int(man_y)))
                
    pygame.display.update()
    