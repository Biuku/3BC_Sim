""" April 10, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

"""

import pygame
from pygame.locals import *
import numpy as np
from man import Man


#### Initialize pygame and screen

pygame.init()
w = 3400 #= optimal for my widescreen
h = 1350
screen = pygame.display.set_mode((w, h))

# Game clock 
clock = pygame.time.Clock()
fps = 45

# Screen setup
arrondissements_font = pygame.font.Font('freesansbold.ttf', 20)

# Graphics setup
diamond = pygame.image.load("images/diamond_1.png")  


#### Coordinates system

#### Calibration of steps-to-pixels conversion factor
def steps_to_pos(old_coord, steps, steps_posNeg):
    pixels_per_step = 7
    
    over_a = np.sqrt( (steps[0] **2)/2 )
    back_a = np.sqrt( (steps[1] **2)/2 )
    
    adjust = np.array([ [over_a, over_a], [back_a, back_a]])
    
    all_xy = adjust * steps_posNeg
    
    #sum x's and y's
    x = np.sum(all_xy[:, 0])
    y = np.sum(all_xy[:, 1])
    
    #convert to pixels
    adjust = np.array([ x, y]) * pixels_per_step
    
    # return absolute pos 
    return old_coord + adjust


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

# New dict's
pos_boundaries = {  "lf_corner": (103, 390), 
                    "cf_wall": (x_centre_line, 35), 
                    "rf_corner": (1780, 410), 
                    "four_B_tip": (x_centre_line, 1245)
                    }

mid_depth_OF = 550
"""
pos_standard_of = { "LF": (550, mid_depth_OF),
                   "CF": (x_centre_line, 350),
                    "RF": (1350, mid_depth_OF)
                    }
"""

## INF
# Base centroids

y_middle_line = 1055

pos_base_centroids = {  "one_B": (1130, y_middle_line),      
                        "two_B": (x_centre_line, 880),
                        "three_B": (768, y_middle_line),
                        "four_B": (x_centre_line, 1235), 
                    }
pos_rubber_P = (x_centre_line, y_middle_line - 5)


### Define standard INF positions using "footsteps" off bases

# Manually update dict. First tuple = "over" and "back". second item controls left-right, up-down of the steps as views on diamond in pygame
inf_steps_adjust = {"f3": [(9, 12),   [(-1, -1), (1, -1)],  "one_B" ],
                    "f4": [(-5, 12),  [(1, 1), (1, -1)],    "two_B"],
                    "f5": [(7, 12),   [(1, -1), (-1, -1)],  "three_B"], 
                    "f6": [(-7, 15),  [(-1, 1), (-1, -1)],  "two_B"], 
                }

## This is the location of standard player coordinates
pos_standard = {}

for key, value in inf_steps_adjust.items():
    steps = value[0]
    steps_posNeg = np.array(value[1])
    
    base_id = value[2]    
    old_coord = pos_base_centroids[base_id]
     
    new_coord = steps_to_pos(old_coord, steps, steps_posNeg)
    
    pos_standard[key] = new_coord

pos_standard['f1'] = (pos_rubber_P)
pos_standard['f2'] = pos_base_centroids['four_B']
pos_standard['f7'] = LF
pos_standard['f8'] = CF
pos_standard['f9'] = RF

for pos in pos_standard.items():
    print(pos)


               
## Instantiate base rect's -- collision objects
base_size = 25
base_offset = base_size // 2
base_rects = []

for base_centroid in pos_base_centroids.values():
    # Rect = left, top, width, height
    base = pygame.Rect(base_centroid[0]-base_offset, base_centroid[1]-base_offset, base_size, base_size)
    base_rects.append(base)


## Create arrondissements 
def draw_arrondissements():
    
    # Draw survey markers for game-play edges
    marker_size = 5

    pygame.draw.circle(screen, 'black', lf_corner, marker_size) # LF corner
    pygame.draw.circle(screen, 'black', cf_wall, marker_size) # CF wall
    pygame.draw.circle(screen, 'black', rf_corner, marker_size) # RF corner
    pygame.draw.circle(screen, 'black', four_B_tip, marker_size//2) # Home plate tip
    
    # Base survey_markers (on centre)
    for base_centroid in pos_base_centroids.values():
        pygame.draw.circle(screen, 'black', base_centroid, marker_size) 
    
    # OF arrondissements
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
    for base in base_rects:
        pygame.draw.rect(screen, "black", base, 2)
    

def draw_positions():
    pos_circle_size = 8
    
    for pos in pos_standard.values():
        pygame.draw.circle(screen, 'black', pos, pos_circle_size, 3)
    

### Create fielders
# Animation setup
x = w//3 #850 
y = 1100

#### Instantiate objects #### 
### Instantiate characters

def create_fielders():
    fielder_ids = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9']

    fielder_objects = {}
    for fielder_id in fielder_ids:
        
        pos = pos_standard[fielder_id]
        fielder_objects[fielder_id] = Man(screen, pos, "fielder")
        
    return fielder_objects

fielder_objects = create_fielders()
#baserunner = Man(screen, x, y, "baserunner")


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

exit = False

while not exit:
    
    clock.tick(fps)
    
    ## Draw background objects
    screen.fill('white')
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

    
    if show_positions:
        draw_positions()
        
    if show_bases:
        draw_bases()

    for fielder in fielder_objects.values():
        fielder.move(left, right, north, south)
        fielder.detect_collisions(base_rects)
 
    pygame.display.update()
