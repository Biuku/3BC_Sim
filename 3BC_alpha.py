""" April 12, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

Today, I want to build a function that draws a line from the tip of Home to the mouse position and displays the distance in feet. This will be an input to building the ball's flight.

"""

import pygame
from pygame.locals import *
import math

#print(pygame.font.get_fonts())

from man import Man
from setup import Setup


##### ***** INITIALIZE PYGAME ***** #####

pygame.init()
w = 2000 #3400 #= optimal for my widescreen
h = 1350
screen = pygame.display.set_mode((w, h))
setup = Setup()

# Game clock 
clock = pygame.time.Clock()
fps = 45

# Graphics setup
diamond = pygame.image.load("images/diamond_1.png")

# Game toggles
left = right = north = south = False
show_arrondissements = False
show_positions = False


##### ***** INITIALIZE COORDINATES AND OBJECTS ***** #####

## Get foundational coordinates | dicts
pos_boundaries = setup.get_boundaries()  # lf_corner, cf_wall, rf_corner, four_B_tip
base_centroids = setup.get_base_centroids() # one_B, two_B, three_B, four_B, rubber_P

## Rects for collision detection at the 4 bases | list  
base_rects = setup.make_bases(base_centroids) # Dict of base rects -- collision objects

## Get situational coordinates | dicts
pos_standard = setup.get_pos_standard(base_centroids) # Standard fielder pre-pitch coordinates: f1, f2, f3, f4, f5, f6, f7, f8, f9
pos_situations = setup.get_pos_situations(base_centroids)  

## Instantiate characters | dict
fielder_objects = setup.make_fielders(pos_standard, screen)  # f1, f2, f3, f4, f5, f6, f7, f8, f9


##### ***** FUNCTIONS ***** #####

### META FUNCTIONS -- used primarily during code-buid ###

## Create arrondissements 
def draw_arrondissements():
    
    # Draw edges of game play
    boundary_marker_size = 7
    base_marker_size = 2
    for boundary_pos in pos_boundaries.values():
        pygame.draw.circle(screen, 'black', boundary_pos, boundary_marker_size)
        
    # Draw centre of bases
    for base_centroid in base_centroids.values():
        pygame.draw.circle(screen, 'grey', base_centroid, base_marker_size) 
        
    for base in base_rects:
        pygame.draw.rect(screen, "black", base, 2)
    
    # Draw markers for the 9 standard defensive positions    
    for pos in pos_standard.values():        
        pygame.draw.circle(screen, 'black', pos, 8, 3)
    

## Draw situational positions       
def draw_positions():
      
    for key, pos_situation in pos_situations.items():
        pygame.draw.circle(screen, 'blue', pos_situation, 35, 2)
        
        text_fielder_id = setup.font14.render(key, True, 'black')  # Text, antialiasing, color
        text_fielder_id_rect = text_fielder_id.get_rect()
        text_fielder_id_rect.center = pos_situation
        
        screen.blit(text_fielder_id, text_fielder_id_rect)


## Measure distance from Home ##
measuring_tape = False

## Utility function to convert a line between two points into a distance in feet
def measure_distance_in_feet(start_pos, end_pos):
    
    ## First, what is the conversion factor? Average the pixels between 1B/3B and 2B/4B 
    pixels_to_feet = ( (355/127) + (362/127) ) / 2
    
    ## Next, convert two sets of coordinates to a linear distance using trigonometry
    distance_in_pixels = math.sqrt( ( end_pos[0] - start_pos[0] )**2  +  ( end_pos[1] - start_pos[1] )**2 )
    
    return distance_in_pixels / pixels_to_feet
    

def draw_measuring_tape():
    
    start_pos = pos_boundaries['four_B_tip']
    end_pos = pygame.mouse.get_pos()
    distance_in_feet = measure_distance_in_feet(start_pos, end_pos)
    
    ## Set up on-screen coordinates

    pos_str = "(" + str(end_pos[0]) + ", " + str(end_pos[1]) + ")"
    distance_str = str( int(distance_in_feet) ) + "'" 

    text_pos = setup.font15.render(pos_str, True, 'black')  # Text, antialiasing, color
    text_pos_rect = text_pos.get_rect()
    text_pos_rect.midleft = (end_pos[0]+30, end_pos[1]+10)

    text_dist = setup.font15.render(distance_str, True, 'grey') # Text, antialiasing, colour
    text_dist_rect = text_dist.get_rect()
    text_dist_rect.midleft = (end_pos[0]+30, end_pos[1]+30)
    
    if measuring_tape:
        pygame.draw.line(screen, 'grey', start_pos, end_pos, 2)
        screen.blit(text_pos, text_pos_rect)
        screen.blit(text_dist, text_dist_rect)


## CREATE A SINGLE TEST PLAY SITUATION
situation = False
situation_start = False

def situation_3(situation_start):

    # Place a ball in RF
    ball_pos = (1400, 400)
    pygame.draw.circle(screen, 'grey', ball_pos, 10)
    
    if situation_start:
        assignments = [ ('f1', 'backup_1_2B'),
                        ('f2', 'trailRunner_2_1B'),
                        ('f3', 'cover_3_1B'), 
                        ('f4', 'cutoff_4_2B'),  
                        ('f5', 'cover_5_3B'),
                        ('f6', 'cover_6_2B'),
                        ('f7', 'backup_7_2B'),
                       ]

        for assignment in assignments:
            fielder_id = assignment[0]
            fielder_goal = pos_situations[assignment[1]]
            
            fielder_objects[fielder_id].assign_goal(fielder_goal)      

        f8 = (ball_pos[0]+50, ball_pos[1]-120)
        fielder_objects['f8'].assign_goal(f8)           
        fielder_objects['f9'].assign_goal(ball_pos)
           
        return False # Turn off the situation initialization 
    

##### ***** MAIN LOOP ***** #####

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
                
            if event.key == K_p:
                show_positions = not(show_positions)
                
            if event.key == K_SPACE:
                situation = not(situation)
                situation_start = True
        
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
       
    ## Get mouse click -- not dependent on 'events', but grouped here 
    if pygame.mouse.get_pressed()[0]:
        measuring_tape= not(measuring_tape)
    

    #### Main actions ####
            
    ## Display markers / anchor points 
    if show_arrondissements:
        draw_arrondissements() ## This is what I call my idea for mapping field locations so Python can determine what kind of hit it was from where it went  
    
    if show_positions:
        draw_positions() ## 
        
    if measuring_tape:
        draw_measuring_tape()

    ## Update baseball plays 
    if situation:
        situation_start = situation_3(situation_start)
        
    

    ## Update and draw fielders
    for fielder in fielder_objects.values():
        fielder.detect_collisions(base_rects)
        fielder.goal_move()
        fielder.kb_move(left, right, north, south)
        fielder.draw()
   
    pygame.display.update()

