""" April 10, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

    April 10 -- re-organized my whole coordinate map system: 
        1. Boundaries -- OF foul poles, tip of home, etc.
        2. OF standard positions 
        3. INF bases + rubber
        
    Next, I want to convert player positions into steps rather than pixels, so I can position them relative to bases or other markers 
    using baseball logic. Then, I'll update the 9 defensive players' standard starting positions.
    
    Once all that is in place, it will start to get fun -- encoding various baseball situations, where each fielder goes, what each baserunner's last obtained base is, etc. 
    
    ***
    Got standard INF positioning in place ... took a lot of math because the diamond is rotated 45 degrees. Did the math in a spreadsheet to be easier to follow my steps, 
    but wouldn't be hard to bake that into the Python code so I can adjust players based on 'steps' (like, with your feet) rather than pixels. 
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


#### Coordinates system

## Boundaries
x_centre_line = 950

lf_corner = (103, 390)
cf_wall = (x_centre_line, 35)
rf_corner = (1780, 410)
four_B_tip = (x_centre_line, 1245)

## OF
mid_depth_OF = 550
LF = (550, mid_depth_OF)
CF = (x_centre_line, 350)
RF = (1350, mid_depth_OF)

## INF
# INF foundation
# base_size = 25

x_1B = 1130
x_3B = 768

y_2B = 880
y_4B = 1235
y_middle_line = 1055
y_rubber_P = y_middle_line - 5

# INF markers
one_B = (x_1B, y_middle_line)
two_B = (x_centre_line, y_2B)
three_B = (x_3B, y_middle_line)
four_B = (x_centre_line, y_4B) 
rubber_P = (x_centre_line, y_rubber_P)

base_coords = [one_B, two_B, three_B, four_B]


## Bases must be created here because they are collision objects
bases = []
base_size = 25
base_offset = base_size // 2

for base_coord in base_coords:
    # Rect = left, top, width, height
    base = pygame.Rect(base_coord[0]-base_offset, base_coord[1]-base_offset, base_size, base_size)
    bases.append(base)


#### Player standard positions

def draw_survey_markers():
    marker_size = 5

    # Game-play edges
    pygame.draw.circle(screen, 'black', lf_corner, marker_size) # LF corner
    pygame.draw.circle(screen, 'black', cf_wall, marker_size) # CF wall
    pygame.draw.circle(screen, 'black', rf_corner, marker_size) # RF corner
    pygame.draw.circle(screen, 'black', four_B_tip, marker_size//2) # Home plate tip
    
    # Base survey_markers (on centre)
     
    for base in base_coords:
        pygame.draw.circle(screen, 'black', base, marker_size) 


## Create OF arrondissements 
def draw_arrondissements():
    circle_size = 40 
    pygame.draw.circle(screen, 'grey', LF, circle_size) # LF
    pygame.draw.circle(screen, 'grey', CF, circle_size) # CF
    pygame.draw.circle(screen, 'grey', RF, circle_size) # RF

    # Draw the position letters for each position
    position = ["7", "8", "9"]
    coord = [LF, CF, RF]
    for i, pos in enumerate(position):
        text = arrondissements_font.render(pos, True, 'black')
        textRect = text.get_rect()    
        textRect.center = coord[i]
        screen.blit(text, textRect)


## Bases are squares capable of collisions with coord based on base survey markers)
def draw_bases():
    for base in bases:
        pygame.draw.rect(screen, "black", base, 2)
    
    
    """
    for base_coord in base_coords:
        base = pygame.Rect(base_coord[0]-base_offset, base_coord[1]-base_offset, base_size, base_size)
        pygame.draw.rect(screen, "black", base, 2)
    """


#### Calibration of steps-to-pixels conversion factor
""" I believe a standard walking step is 1'. From Home to 2B there are 127' = 63.5 steps; and also 355 pixels.
    So, there should be 5.6 pixels per step. I'm going to lay down some footprints to see if that looks right
    
"""
def draw_positions():
    y_footprint = y_4B
    step_size = 5.6
     
    step_circle_size = 3
    pos_circle_size = 8
    
    
    #Draw 3B standard position location
    """
    # Based on 2' per step
    f3_adjust= (12, -83)
    f4_adjust= (79, -40)
    f5_adjust = (-20, -75)
    f6_adjust= (-87, -32)
    """
    # Based on 3' per step
    f3_adjust= (15, -103)
    f4_adjust= (99, -49)
    f5_adjust = (-25, -94)
    f6_adjust= (-109, -40)
    
    
    fielders = [(f3_adjust, one_B), (f4_adjust, two_B), (f5_adjust, three_B), (f6_adjust, two_B)]
    
    for fielder in fielders:
        x_new = fielder[0][0] + fielder[1][0]
        y_new = fielder[0][1] + fielder[1][1]
        
        pygame.draw.circle(screen, 'black', (x_new, y_new), pos_circle_size, 3)
    

### Create fielders
# Animation setup
x = w//3 #850 
y = 1100

#### Instantiate objects #### 
# Instantiate characters
steps = 10

baserunner = Man(screen, x, y, "baserunner")
f1 = Man(screen, rubber_P[0]-5, rubber_P[1]-(2.5*steps), "fielder")
f2 = Man(screen, four_B[0]-5, four_B[1]+(3*steps), "fielder")
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
show_bases = False
show_positions = False


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

            ### Set up stuff 

            if event.key == K_a:
                show_arrondissements = not(show_arrondissements)
                
            if event.key == K_b:
                show_bases = not(show_bases)

            if event.key == K_p:
                show_positions = not(show_positions)

            # End set up stuff

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
        draw_survey_markers()
    
    if show_positions:
        draw_positions()
        
    if show_bases:
        draw_bases()

  
    for man in men:
        man.move(left, right, north, south)
        man.detect_collisions(bases)
 
    pygame.display.update()
    