""" April 16, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

Huge refactor today -- shifted basically all game play to a GamePlay module with OOP

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
w = 2000 #3400 #= optimal for my widescreen
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
boundary_coords = gamePlay.boundary_coords  # lf_foulPole, cf_wall, rf_foulPole, four_B_tip
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
        

## Measure the distance from Home in feet 
def draw_measuring_tape():
    
    ### Temp -- make the measuring tape 475' long, at centroid = 1430
    centroid = (950, 1430)
    dist_feet = 475
    dist_pixels = 1406.1038
    
    
    start_coord = centroid #boundary_coords['four_B_tip']
    
    ### I need to draw the tape so it never exceeds 475' from the main centroid -- i.e., so the y coordinate is set, given the x mouse pos    
    ## I know 'a' (x2 - x1) and 'c' (fixed at but need 'band length of hyp and , given 
    
    #""" 
    end_coord = pygame.mouse.get_pos()
    distance_in_feet = helper.measure_distance_in_feet(start_coord, end_coord)
    
    ## Set up on-screen coordinates
    coord_str = "(" + str(end_coord[0]) + ", " + str(end_coord[1]) + ")"
    distance_str = str( int(distance_in_feet) ) + "'" 
    
    x = end_coord[0]+20
    pos_coord = (x, end_coord[1]+10)
    distance_coord = (x, end_coord[1]+30)
    
    #"""
    
    ## Draw 
    # string_, colour, coord, font, justification: 1 = topleft 2 = center
    helper.draw_text(coord_str, 'black', pos_coord, setup.font15, 1)
    helper.draw_text(distance_str, 'grey', distance_coord, setup.font15, 1)
    
    pygame.draw.line(screen, 'grey', start_coord, end_coord, 2)



### TEMP META TEST Find the of wall centroid

def temp_distance_finding(boundary_coords): 
    
    lf_foulPole = boundary_coords['lf_foulPole']
    rf_foulPole = boundary_coords['rf_foulPole']
    cf_wall = boundary_coords['cf_wall']
    main_centroid = (950, 1430)
    
    
    a = cf_wall[0] - lf_foulPole[0]
    b = main_centroid[1] - cf_wall[1]
    c = helper.measure_distance_in_pixels(main_centroid, lf_foulPole)
    
    #print(f"\n    a = {a}, b = {b}, c = {c} \n") 
    
    
    #"""
    min_diff = 10000
    best_y = None
    centre_x = 950

    dict = {}

    for y in range(1100, 1700, 1):
        
        start_coord = (centre_x, y)    
        
        # Get distance to CF wall
        #cf_dist = helper.measure_distance_in_feet(start_coord, cf_wall)
        #rf_dist = helper.measure_distance_in_feet(start_coord, rf_foulPole)
        
        cf_dist = helper.measure_distance_in_pixels(start_coord, cf_wall)
        rf_dist = helper.measure_distance_in_pixels(start_coord, rf_foulPole)
        lf_dist = helper.measure_distance_in_pixels(start_coord, lf_foulPole)
        
        #curr_diff = abs(cf_dist - rf_dist)
        
        curr_diff = (cf_dist - rf_dist)**2 + (cf_dist - lf_dist)**2
        
        dict[y] = [round(curr_diff, 2), cf_dist]
        
        
        if curr_diff < min_diff:
            best_y = y
            min_diff = curr_diff
            dist = cf_dist
    #"""
        #print(f"\ny = {y}, curr_diff = {round(curr_diff, 1)}\n" )
    
    step_= 0 
    
    for key, value in dict.items(): 
        print(f"y={key} dist={value}  |  ", end = " ")
        step_ += 1
        if step_%5 == 0:
            print()

    print("\n    Best coord, dist: ", best_y, ", ", round(dist, 1), "\n")
    
    best_y = min(dict, key=dict.get)
    best_dist = min(dict.values()[0])
             
    print(f"    Best y = {best_y}, shortest_distance = {round(best_dist, 1)}\n\n" )
    

    



temp_distance_finding(boundary_coords)

## lf centroid is y = 1480
## rf centroid is y = 1380
# Oh shit!

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
            
    ## Display markers / anchor points 
    if show_boundary_markers:
        draw_boundary_markers()
    
    if show_defensiveSit_coord:
        draw_defensiveSit_id() ## 
        
    if measuring_tape:
        draw_measuring_tape()
    
    
    ## Update baseball plays 
    gamePlay.print_instructions()
    gamePlay.choose_situation()
    gamePlay.do_situation()
    
    ## Update and draw fielders and baserunners
    gamePlay.move_fielders(left, right, north, south)
    gamePlay.move_baserunners(left, right, north, south)
    gamePlay.move_ball(moving_ball)
    
    gamePlay.reset_instructionCoord()

    pygame.display.update() 

