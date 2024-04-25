""" April 22, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

"""

import pygame
from pygame.locals import *
import math

from setup import Setup
from gamePlay import GamePlay
from helpers import Helpers

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(1, 30) # Opens Pygame to top-left of monitor

##### ***** INITIALIZE PYGAME ***** #####

pygame.init()
w = 2500 #3400 #= optimal for my widescreen
h = 1350
screen = pygame.display.set_mode((w, h))
setup = Setup(screen)
helper = Helpers(screen)
gamePlay = GamePlay(screen)

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
show_boundary_markers = False
show_defensiveSit_coord = False
measuring_tape = False
moving_ball = False


##### Import key data to run the meta functions (can be discarded when final) #####

## Get foundational coordinates | dicts
for false_loop in range(1):
    boundary_coords = gamePlay.boundary_coords  # lf_foulPole, cf_wall, rf_foulPole, four_B_tip, main_centroid
    boundary_thetas = gamePlay.boundary_thetas # lf_foulPole_deg, cf_deg, rf_foulPole_deg, cf_left_deg, cf_right_deg
    base_centroids = gamePlay.base_centroids  # one_B, two_B, three_B, four_B, rubber_P
    base_rects = gamePlay.base_rects # Dict of base rects -- collision objects
    fielder_standard_coord = gamePlay.fielder_standard_coord # Standard fielder pre-pitch coordinates: 1-9
    defensiveSit_fielder_coord = gamePlay.defensiveSit_fielder_coord


### META FUNCTIONS -- used primarily during code-buid ###

## Create boundary markers -- to show all the key coord's to reference off of 
def draw_boundary_markers():
    
    # Draw edges of game play
    boundary_marker_size = 7
    base_marker_size = 2
    
    for boundary_coord in boundary_coords.values():
        pygame.draw.circle(screen, 'blue', boundary_coord, boundary_marker_size)
        
    # Draw centre of bases
    for base_centroid in base_centroids.values():
        pygame.draw.circle(screen, 'blue', base_centroid, base_marker_size) 
        
    for base in base_rects.values():
        pygame.draw.rect(screen, "blue", base, 2)
    
    # Draw markers for the 9 standard defensive positions    
    for coord in fielder_standard_coord.values():        
        pygame.draw.circle(screen, 'blue', coord, 8, 3)
    
## Draw situational positions       
def draw_defensiveSit_id():
      
    for defensiveSit_id, defensive_sit_coord in defensiveSit_fielder_coord.items():
        pygame.draw.circle(screen, 'gray', defensive_sit_coord, 35, 2)
        
        text = "#" + str(defensiveSit_id)
        
        # string_, colour, coord, font, justification: 1 = topleft 2 = center
        helper.draw_text(text, 'gray', defensive_sit_coord, setup.font12, 2)
        

def draw_OF_wall():
    """ I have an image rn as the OF, but it's got some symmetry challenges. Want to replace with clearly defined coordinates. """
    centroid = boundary_coords['main_centroid'] 
    radius = helper.measure_distance_in_pixels(boundary_coords['main_centroid'], boundary_coords['cf_wall'])
    
    #### 1. First, I need to hide a bunch of things from the png that are screwy because it is not symmetrical ####
    
    ## Draw white ring -- because the png is so screwy I need to cover up part of the black OF wall beyond the new wall 
    white_ring_thickness = 50
    pygame.draw.circle(screen, 'white', centroid, radius + white_ring_thickness, white_ring_thickness)
    
    ## Draw green ring -- because the png is so screwy I need to cover up part of the white 
    green_ring_thickness = 300
    green = (66, 140, 66)
    pygame.draw.circle(screen, green, centroid, radius, green_ring_thickness)


    #### 2. Second, draw the perfectly symmetrical black wall and grey warning track
    
    ## Draw wall -- the true edge of the wall is the radius, but have to start drawing past it and inwards by its thickness 
    floor_thickness = 12
    pygame.draw.circle(screen, 'black', centroid, radius + floor_thickness, floor_thickness)
    
    ## Draw warning track
    warning_track_thickness = 50
    warning_track_colour = (238, 238, 238)
    pygame.draw.circle(screen, warning_track_colour, centroid, radius, warning_track_thickness)
    

    #### 3. Third, cover the wall either side of diamond.png, which the circles above currently extend into
    start_x = 1862 + 10 # width of the diamond.png + offset I originally made
    width = w - start_x

    # left: float, top: float, width: float, height:
    pygame.draw.rect( screen, 'white', pygame.Rect(0, 0, 10, h) ) ## Cover the 10 pixel sliver on the left of diamond.png 
    pygame.draw.rect( screen, 'white', pygame.Rect(start_x, 0, width, h) ) ## Cover from the right-edge of diamond.png to the right edge of the screen


def draw_foul_lines():
    start_coord = boundary_coords['four_B_tip']
    lf_pole = boundary_coords['lf_foulPole']
    rf_pole = boundary_coords['rf_foulPole']
    chalk_thickness = 8
    
    pygame.draw.line(screen, 'white', start_coord, lf_pole, chalk_thickness)
    pygame.draw.line(screen, 'white', start_coord, rf_pole, chalk_thickness)
    

def draw_arrondissements():
    
    centroid = boundary_coords['four_B_tip']
    dist_pixels = helper.measure_distance_in_pixels(centroid, boundary_coords['cf_wall']) 
    
    CF_left_end = helper.theta_to_endCoord(centroid, boundary_thetas['cf_left_deg'], dist_pixels)
    CF_right_end = helper.theta_to_endCoord(centroid, boundary_thetas['cf_right_deg'], dist_pixels)
    
    pygame.draw.line(screen, 'blue', centroid, CF_left_end, 2)
    pygame.draw.line(screen, 'blue', centroid, CF_right_end, 2)


def interpret_ball_location():
    
    # Get ball coord
    ball_coord = gamePlay.get_ball_coord()
    centroid = boundary_coords['four_B_tip'] 
    
    # Get theta of ball
    ball_theta_rad = helper.coord_to_theta(centroid, ball_coord)
    ball_theta_deg = math.degrees(ball_theta_rad)
    
    # if theta is... # boundary_thetas: lf_foulPole_deg, cf_deg, rf_foulPole_deg, cf_left_deg, cf_right_deg 
    ball_loc = None
    
    if ball_theta_deg > boundary_thetas['lf_foulPole_deg']:
        ball_loc = "Foul: left side"
    
    elif ball_theta_deg > boundary_thetas['cf_left_deg']:
        ball_loc = "Left field"
        
    elif ball_theta_deg > boundary_thetas['cf_right_deg']:
        ball_loc = "Centre field"
        
    elif ball_theta_deg > boundary_thetas['rf_foulPole_deg']:
        ball_loc = "Right field"
        
    else:
        ball_loc = "Foul: right side"
        
    gamePlay.print_ball_loc(ball_loc)

    
## Measure the distance from Home in feet 
def draw_measuring_tape():
    
    """ Arc describes OF wall """
    #centroid = boundary_coords['main_centroid'] #centroid = (950, 1430)
    #dist_pixels = helper.measure_distance_in_pixels(centroid, boundary_coords['cf_wall']) # 1406 # dist_feet = 475
    
    """ Arc from Home """
    centroid = boundary_coords['four_B_tip']    
                   
    Q = pygame.mouse.get_pos()
    RC = (Q[0], centroid[1]) # Note, centroid is off screen (below)
    
    ## Draw triangle from centroid to mouse_pos
    #pygame.draw.polygon(screen, 'grey', (centroid, Q, RC) )
    
    # Get theta
    theta_rad = helper.coord_to_theta(centroid, Q)

    """ For arc describing OF wall """     
    ### Given theta and length of measuring tape, get end coord
    #theta_deg = math.degrees(theta_rad)
    #end_coord = helper.theta_to_endCoord(centroid, theta_deg, dist_pixels)

    end_coord = Q
    start_coord = centroid

    ## Set up on-screen coordinates
    coord_str = "(" + str( int(end_coord[0]) ) + ", " + str( int(end_coord[1]) ) + ")"
    
    distance_in_feet = helper.measure_distance_in_feet(start_coord, end_coord)
    distance_str = str( int(distance_in_feet) ) + "'" 
    
    theta_str = str( int(math.degrees(theta_rad)) ) + "\u00b0"
    
    texts = [coord_str, distance_str, theta_str]

    ## Draw     
    x = end_coord[0]+20

    for i, text in enumerate(texts):
        y = end_coord[1] - 10 + (20 * i)
        helper.draw_text(text, 'black', (x, y), setup.font15, 1)
        
    pygame.draw.line(screen, 'red', start_coord, end_coord, 4)


##### ***** MAIN LOOP ***** #####

exit = False

while not exit:
    
    clock.tick(fps)
    
    ## Draw background objects
    screen.fill('white')
    screen.blit(diamond, (10, 10))

    ### Events ### 
    # s = run test situation | m = toggle measuring tape | b = show boundary markers | d = show defensive situations coord 
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
            
            ### Set up stuff 
            
            ## Option selection keys
            for i, num_key in enumerate( [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9] ):
                if event.key == num_key:
                    gamePlay.update_numkeys(i)
                    
            ## Reset situations
            if event.key == K_c:
                gamePlay.reset_numkeys()       
                gamePlay.update_curr_defensiveSit(0)
                gamePlay.reset_fielders() ## send fielders back to their start positions
            
            if event.key == K_s:
                gamePlay.update_situation_start(True)
         
            if event.key == K_b:
                show_boundary_markers = not(show_boundary_markers)
                
            if event.key == K_d:
                show_defensiveSit_coord = not(show_defensiveSit_coord)
                
            if event.key == K_m:
                measuring_tape = not(measuring_tape)
            
            if event.key == K_SPACE:
                gamePlay.advance_baserunner()

            ## Temp -- something got unstable and I need to be able to stop the baserunner from moving 
            if event.key == K_q:
                gamePlay.remove_baserunner_goal()
                
            
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
            #if event.key == K_SPACE:
            #    gamePlay.update_baserunner_advance(False)
        
        ## Mouse button events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                moving_ball = True
            
            elif event.button == 3: # Right click
                pass
            
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Left click
                moving_ball = False
            
            elif event.button == 3: # Right click
                pass
            
    
    #### Main actions ####
            
    ## Draw the artificial diamond -- to replace parts of diamond.png
    draw_OF_wall()
    draw_foul_lines()
    
    ## Display markers / anchor points
    if show_boundary_markers:
        draw_boundary_markers()
        draw_arrondissements()
    
    if show_defensiveSit_coord:
        draw_defensiveSit_id() ## 
        
    if measuring_tape:
        draw_measuring_tape()
        
    for fake_loop in range(1): 
        ## Update baseball plays 
        gamePlay.print_instructions()
        gamePlay.choose_situation()
        gamePlay.do_situation()
        
        ## Update and draw fielders and baserunners
        gamePlay.move_fielders(left, right, north, south)
        gamePlay.move_baserunners(left, right, north, south)
        gamePlay.move_ball(moving_ball)
        
        
        interpret_ball_location()

        gamePlay.reset_instructionCoord()
    

    pygame.display.update() 

