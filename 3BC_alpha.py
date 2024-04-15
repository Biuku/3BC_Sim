""" April 14, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

Today, I want to build a function that draws a line from the tip of Home to the mouse position and displays the distance in feet. This will be an input to building the ball's flight.

"""

import pygame
from pygame.locals import *
import math

from setup import Setup

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(1, 30) # Opens Pygame to top-left of monitor

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

## Game toggles
left = right = north = south = False
baserunner_advance = False
situation_start = False

# Meta / development toggles
show_arrondissements = False
show_positions = False
measuring_tape = False
num_keys = [False] * 10 ## Keep track of multiple num keys pressed above the kb

##### ***** INITIALIZE COORDINATES AND OBJECTS ***** #####

## Get foundational coordinates | dicts
pos_boundaries = setup.get_boundaries()  # lf_corner, cf_wall, rf_corner, four_B_tip
base_centroids = setup.base_centroids  # one_B, two_B, three_B, four_B, rubber_P

## Rects for collision detection at the 4 bases | list  
base_rects = setup.make_bases(base_centroids) # Dict of base rects -- collision objects

## Get situational coordinates | dicts
pos_standard = setup.get_pos_standard(base_centroids) # Standard fielder pre-pitch coordinates: f1, f2, f3, f4, f5, f6, f7, f8, f9
pos_coverage = setup.get_pos_coverage(base_centroids)
defensive_plays = setup.get_defensive_plays(pos_coverage)
curr_situation = 0

## Instantiate characters | dict
fielder_objects = setup.make_fielders(pos_standard, screen)  # f1, f2, f3, f4, f5, f6, f7, f8, f9
baserunner = setup.make_baserunners(screen)
ball_pos = (10, 10)

##### ***** FUNCTIONS ***** #####

def draw_text(string_, colour, coord, font, justification):
    
    text = font.render(string_, True, colour)
    text_rect = text.get_rect()
# 
    text_rect.topleft = coord
  
    if justification == 2: 
        text_rect.center = coord
        
    screen.blit(text, text_rect)
    

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
        
    for base in base_rects.values():
        pygame.draw.rect(screen, "black", base, 2)
    
    # Draw markers for the 9 standard defensive positions    
    for pos in pos_standard.values():        
        pygame.draw.circle(screen, 'black', pos, 8, 3)
    
## Draw situational positions       
def draw_coverage_id():
      
    for key, pos_situation in pos_coverage.items():
        pygame.draw.circle(screen, 'blue', pos_situation, 35, 2)
        
        text = "#" + str(key)
        # string_, colour, coord, font, justification: 1 = topleft 2 = center
        draw_text(text, 'black', pos_situation, setup.font12, 2)

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
    
    x = end_pos[0]+20
    pos_coord = (x, end_pos[1]+10)
    distance_coord = (x, end_pos[1]+30)
    
    ## Draw 
    # string_, colour, coord, font, justification: 1 = topleft 2 = center
    draw_text(pos_str, 'black', pos_coord, setup.font15, 1)
    draw_text(distance_str, 'grey', distance_coord, setup.font15, 1)
    
    pygame.draw.line(screen, 'grey', start_pos, end_pos, 2)


## CREATE A SINGLE TEST PLAY SITUATION
situation_3_bool = False
situation_7_bool = False


def choose_situation(curr_situation, num_keys, defensive_plays):
    
    ## Let the user enter 2 digits
    for i, val in enumerate(num_keys):
        if val:
            if curr_situation == 0: 
                curr_situation = i
            
            elif curr_situation < 10: 
                curr_situation =  curr_situation * 10 + i # Tens
                
            ## else you're trying to add a third digit after reaching a 2 digit # 
            else:
                curr_situation = i ## Roll over if you tried entering too high a 
    num_keys = [False] * 10 

    ### Write instructions: key assignments for coverage situations     
    x, y = 1400, 950
    
    instructions_text = "Press 'c' to reset situations. Press 's' to activate current situation"
    draw_text(instructions_text, 'black', (x, y), setup.font20, 1)
   
    y += 20
    draw_text("You pressed: ", 'black', (x, y), setup.font20, 1)
    
    x += 120
    draw_text(str(curr_situation), 'black', (x, y), setup.font20, 1)
    
    x += 40
    if curr_situation in defensive_plays:
        text = defensive_plays[curr_situation][0]
        draw_text(text, 'black', (x, y), setup.font20, 1)
        
        
    
    return curr_situation, num_keys


def do_situation(curr_situation, defensive_plays, pos_coverage, pos_standard, situation_start, ball_pos):

    if situation_start:
        fielder_index = [None, 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9']
        defensive_play = defensive_plays[curr_situation]
        
        ## First, find the guy fielding the ball and place the ball relative to him
        for fielder, role in enumerate(defensive_play[1:]):
            
            if role == 1:
                fielder_id = fielder_index[fielder + 1]
                fielder_pos = pos_standard[fielder_id]  # pass 'f1', 'f2' etc. to get standard pos
                ball_pos = (fielder_pos[0] - 150, fielder_pos[1] - 150)

        ## Next, assign goals to all 9 defensive players. This requires ball_pos
        for fielder, fielder_action_id in enumerate(defensive_play[1:]):
            fielder_id = fielder_index[fielder + 1]
            
            if fielder_action_id == 1:
                fielder_objects[fielder_id].assign_goal(ball_pos)
            
            elif fielder_action_id == 2:
                backup_pos = (ball_pos[0]-70, ball_pos[1]-70)
                fielder_objects[fielder_id].assign_goal(backup_pos)
                
            else:
                fielder_goal = pos_coverage[fielder_action_id]
                fielder_objects[fielder_id].assign_goal(fielder_goal)   

    # Display the ball           
    pygame.draw.circle(screen, 'grey', ball_pos, 10)
    
    #x, y = (1400, 1100)
    #draw_text(str(defensive_play), 'black', (x, y), setup.font15, 1)

    
    """    
 

        for assignment in assignments_sit_3:
            fielder_id = assignment[0]
            coverage_id = assignment[1]
            
            fielder_goal = pos_coverage[coverage_id]
            
            fielder_objects[fielder_id].assign_goal(fielder_goal)      

        f8 = (ball_pos[0]+50, ball_pos[1]-120)
        fielder_objects['f8'].assign_goal(f8)           
        fielder_objects['f9'].assign_goal(ball_pos)
        """
        
    return False, ball_pos  # Turn off situation start


##### ***** MAIN LOOP ***** #####

exit = False

while not exit:
    
    clock.tick(fps)
    
    ## Draw background objects
    screen.fill('white')
    screen.blit(diamond, (10, 10))

    ### Events ### 
    # s = run test situation | m = toggle measuring tape | a = show arrondissements | p = show situational positions 
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            exit = True

        ## Runner movement events
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                exit = True

            ## Movement keys
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
                
            ## Option selection keys
            for i, num_key in enumerate( [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9] ):
                if event.key == num_key:
                    num_keys[i] = True 
                    
            ## Reset situations
            if event.key == K_c:
                num_keys = [False] * 10
                curr_situation = 0
            
            if event.key == K_s:
                situation_start = True
            
            

            ### Set up stuff 

            if event.key == K_a:
                show_arrondissements = not(show_arrondissements)
                
            if event.key == K_p:
                show_positions = not(show_positions)
                
            if event.key == K_e:
                situation_3_bool = not(situation_3_bool)
                situation_start = True
            
            if event.key == K_u:
                situation_7_bool = not(situation_7_bool)
                situation_start = True
            
            if event.key == K_m:
                measuring_tape = not(measuring_tape)
            
            if event.key == K_SPACE:
                baserunner_advance = True
                baserunner.assign_goal()
        
        
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
            
            ### Set up stuff 
            if event.key == K_SPACE:
                baserunner_advance = False

    
    #### Main actions ####
            
    ## Display markers / anchor points 
    if show_arrondissements:
        draw_arrondissements() ## This is what I call my idea for mapping field locations so Python can determine what kind of hit it was from where it went  
    
    if show_positions:
        draw_coverage_id() ## 
        
    if measuring_tape:
        draw_measuring_tape()


    ## Update baseball plays 
    curr_situation, num_keys = choose_situation(curr_situation, num_keys, defensive_plays)
    situation_start, ball_pos = do_situation(curr_situation, defensive_plays, pos_coverage, pos_standard, situation_start, ball_pos)
    
    ## Reset fielders upon pressing 'c'
    if curr_situation == 0:
        fielder_objects = setup.make_fielders(pos_standard, screen)
    

    ## Update and draw fielders
    for fielder in fielder_objects.values():
        fielder.goal_move()
        
        if not( fielder.get_goal() ):        
            fielder.move_man(left, right, north, south) ## This overwrites the goal-setting animation unless only called when no goal
        fielder.detect_collisions(base_rects)
        fielder.draw_fielder()
        
    
    ## For now, just focus on one baserunner
    baserunner.goal_move()
        
    if not( baserunner.get_goal() ): 
        baserunner.move_man(left, right, north, south)  ## This overwrites the goal-setting animation unless only called when no goal
        
    baserunner.detect_collisions(base_rects, fielder_objects)
    baserunner.draw_baserunner()

   
    pygame.display.update()

