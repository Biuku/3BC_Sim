""" April 10, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

"""

import pygame
from pygame.locals import *

from man import Man
from setup import Setup

#### Initialize pygame and screen

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

#### Coordinates system ####
pos_boundaries = setup.get_boundaries()
base_centroids = setup.get_base_centroids()
pos_standard = setup.get_pos_standard(base_centroids) ## Standard player position coordinates
pos_situations = setup.get_pos_situations(base_centroids)

base_rects = setup.make_bases(base_centroids) ## Instantiate base rect's -- collision objects

## Create arrondissements 
def draw_arrondissements():
    
    # Draw edges of game play
    marker_size = 5
    for boundary_pos in pos_boundaries.values():
        pygame.draw.circle(screen, 'black', boundary_pos, marker_size)
        
    # Draw centre of bases
    for base_centroid in base_centroids.values():
        pygame.draw.circle(screen, 'black', base_centroid, marker_size) 
        
    for pos_situation in pos_situations.values(): 
        pygame.draw.circle(screen, 'blue', pos_situation, 7, 2) 

## Rect's for collisions 
def draw_bases():
    for base in base_rects:
        pygame.draw.rect(screen, "black", base, 2)

## The 9 defensive positions    
def draw_positions():
    pos_circle_size = 8
    for pos in pos_standard.values():        
        pygame.draw.circle(screen, 'black', pos, pos_circle_size, 3)

### Instantiate characters
fielder_objects = setup.make_fielders(pos_standard, screen)  #'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9'
#baserunner = Man(screen, x, y, "baserunner")

## Movement toggles
left = right = north = south = False

## Show arrondissements toggle
show_arrondissements = False
show_bases = False
show_positions = False


""" CREATE A SINGLE TEST PLAY SITUATION """
situation = False
situation_start = False

def situation_3(situation_start):

    # PLace a ball in RF
    ball_pos = (1400, 400)
    pygame.draw.circle(screen, 'grey', ball_pos, 10)
    
    #
    if situation_start:
        assignments = [ ('f3', 'cover_3_1B'), ('f4', 'cutoff_4_2B'), ('f6', 'cover_6_2B')]

        for assignment in assignments:
            fielder_id = assignment[0]
            fielder_goal_id = assignment[1]
            fielder_goal = pos_situations[fielder_goal_id]
            
            fielder_objects[assignment[0]].assign_goal(pos_situations[assignment[1]])      

        f8 = (ball_pos[0]+50, ball_pos[1]-120)
        
        fielder_objects['f8'].assign_goal(f8)           
        fielder_objects['f9'].assign_goal(ball_pos)
           
        return False # Turn off the situation initialization 
    

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

    if show_arrondissements:
        draw_arrondissements()
    
    if show_positions:
        draw_positions()
        
    if show_bases:
        draw_bases()

    if situation:
        situation_start = situation_3(situation_start)

    for fielder in fielder_objects.values():
        fielder.detect_collisions(base_rects)
        fielder.goal_move()
        fielder.mouse_move(left, right, north, south)
   
    pygame.display.update()
