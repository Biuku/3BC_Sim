""" April 22, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

"""

import pygame
from pygame.locals import *
import math

from setup import Setup
from gameplay.gamePlay import GamePlay
from helpers import Helpers
from screen_printer import ScreenPrinter

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(1, 30) # Opens Pygame to top-left of monitor

##### ***** INITIALIZE PYGAME ***** #####

pygame.init()
w = 2500 #3400 #= optimal for my widescreen
h = 1350
screen = pygame.display.set_mode( (w, h) )

setup = Setup(w)
helpers = Helpers()
screenPrinter = ScreenPrinter(screen)
gamePlay = GamePlay(screen) 

fps = setup.fps

# Game clock 
clock = pygame.time.Clock()

# Graphics setup
diamond = pygame.image.load("images/diamond_1.png")

## Game toggles
left = right = north = south = False

# Meta / development toggles
show_boundary_markers = False
show_defensiveSit_coord = False
measuring_tape = False
mouse_drag_ball_toggle = False


### Ball launch data
for ball_launch_data_setup in range(1):
    
    launch_metrics_deltas = {
        "exit_velo": 0,
        "launch_angle": 0,
        "launch_direction": 0,
                    }

    prev_ticks = 0


"""  KEYS to setup > coordinate dicts
- setup.boundaries                      # lf_foulPole |  cf_wall |  rf_foulPole |  four_B_tip |  main_centroid
- setup.boundary_thetas                 # lf_foulPole_deg |  cf_deg |  rf_foulPole_deg |  cf_left_deg |  cf_right_deg
- setup.base_centroids                  # 1 |  2 |  3 |  4 |  p
- setup.base_rects                      # 1 |  2 |  3 |  4 -- collision objects
- setup.fielder_standard_coord          # 1-9 -- standard fielder pre-pitch coordinates: 1-9
- setup.defensiveSit_fielder_coord 
"""    

### DRAW THE BACKGROUND
for background in range(1):
    
    def draw_background():     
        screen.blit(diamond, (10, 10))
        draw_OF_wall()
        draw_foul_lines()
    
    
    def draw_OF_wall():

        centroid = setup.boundaries['main_centroid'] ## The centre of a circle that includes the OF wall arc. This point is off-screen, South
        
        radius = helpers.main_centroid_radius #helpers.measure_distance_in_pixels(centroid,  setup.boundaries['cf_wall'])
        
        ### 1. First, I need to hide a bunch of things from the png that are screwy because it is not symmetrical ####
        ## Draw white ring -- I need to cover up part of the black OF wall beyond the new wall 
        white_ring_thickness = 50
        pygame.draw.circle(screen, 'white', centroid, radius + white_ring_thickness, white_ring_thickness)
        
        ## Draw green ring -- I need to cover up part of the white 
        green_ring_thickness = 300
        green = (66, 140, 66)
        pygame.draw.circle(screen, green, centroid, radius, green_ring_thickness)

        ### 2. Second, draw the perfectly symmetrical black wall and grey warning track
        ## Draw OF wall -- the true edge of the wall is the radius, but have to start drawing past it and inwards by its thickness 
        wall_thickness = 12
        pygame.draw.circle(screen, 'black', centroid, radius + wall_thickness, wall_thickness)
        
        ## Draw warning track
        warning_track_thickness = 50
        warning_track_colour = (238, 238, 238)
        pygame.draw.circle(screen, warning_track_colour, centroid, radius, warning_track_thickness)
        
        ### 3. Third, cover the wall either side of diamond.png, which the circles above currently extend into
        start_x = 1862 + 10 # width of the diamond.png + offset I originally made
        width = w - start_x
        pygame.draw.rect( screen, 'white', pygame.Rect(0, 0, 10, h) ) ## Left side: cover the 10 pixel sliver on the left of diamond.png 
        pygame.draw.rect( screen, 'white', pygame.Rect(start_x, 0, width, h) ) ## Right side: cover from the right-edge of diamond.png to the right edge of the screen


    def draw_foul_lines():
        start_coord = setup.boundaries['four_B_tip']
        lf_pole = setup.boundaries['lf_foulPole']
        rf_pole = setup.boundaries['rf_foulPole']
        chalk_thickness = 8
        
        pygame.draw.line(screen, 'white', start_coord, lf_pole, chalk_thickness)
        pygame.draw.line(screen, 'white', start_coord, rf_pole, chalk_thickness)
        

for user_input_helpers in range(1):
    
    num_keys = [False] * 10 ## Keep track of multiple num keys pressed above the kb
    curr_defensiveSit = 0
    
    
    def reset_numkeys(): 
        return [False] * 10

    
    def choose_situation(curr_defensiveSit): #curr_defensiveSit, num_keys, defensiveSit_plays
            
        ## Let the user enter 2 digits
        for i, val in enumerate(num_keys):
            
            if val:
                if curr_defensiveSit == 0: 
                    curr_defensiveSit = i
                
                ## If there is a number from 1-9 (e.g., "4"), make it the tens 
                elif curr_defensiveSit < 10: 
                    curr_defensiveSit = curr_defensiveSit * 10 + i # Tens
                    
                ## else you're trying to add a third digit after reaching a 2 digit # 
                else:
                    curr_defensiveSit = i ## Roll over if you tried entering too high a 
        
        gamePlay.update_curr_defensiveSit(curr_defensiveSit)
        
        return curr_defensiveSit


    def control_ticks_for_launch_data(prev_ticks_, launch_metrics_deltas):
        ticks = pygame.time.get_ticks()  ## Number of miliseconds since pygame.init() called
       
        if ticks - prev_ticks_ > .03 * 1000:  ## Seconds delay between updates
            prev_ticks_ = ticks

            gamePlay.send_launch_deltas_to_ball(launch_metrics_deltas)
            
        
        return prev_ticks_


for meta_functions in range(1):

    def draw_boundary_markers():
        boundary_marker_size = 7
        ring_size = 5

        # Mark edge boundaries    
        for boundary_coord in setup.boundaries.values():
            pygame.draw.circle(screen, 'blue', boundary_coord, boundary_marker_size, ring_size)

        # Mark base centres and rects
        for base_centroid in setup.base_centroids.values():
            pygame.draw.circle(screen, 'blue', base_centroid, boundary_marker_size, ring_size) 

        # Mark 9 standard defensive positions   
        for coord in setup.fielder_standard_coord.values():        
            pygame.draw.circle(screen, 'blue', coord, 8, 3)

        ## Demarcate LF-CF-RF in blue
        centroid = setup.boundaries['four_B_tip']
        dist_pixels = helpers.measure_distance_in_pixels(centroid, setup.boundaries['cf_wall']) 

        CF_left_end = helpers.theta_to_endCoord(centroid, setup.boundary_thetas['cf_left_deg'], dist_pixels)
        CF_right_end = helpers.theta_to_endCoord(centroid, setup.boundary_thetas['cf_right_deg'], dist_pixels)

        pygame.draw.line(screen, 'blue', centroid, CF_left_end, 2)
        pygame.draw.line(screen, 'blue', centroid, CF_right_end, 2)

        draw_ball_depth_perimeters()


    def draw_ball_depth_perimeters():

        centroid = setup.four_B_tip
        
        # Use main centroid    
        #centroid = setup.main_centroid
        #main_centroid_to_home_y = abs( setup.main_centroid[1] - setup.four_B_tip[1] )
        
        for radius in setup.ball_depth_lookup:
            
            radius *= setup.pixels_per_foot # Convert to pixels
            radius += 0 #main_centroid_to_home_y # The lookup is based on distance from Home. Adjust if using main_centroid as the centre 
            
            pygame.draw.circle(screen, 'blue', centroid, radius, 2)


    ## Draw situational positions       
    def draw_defensiveSit_id():
        radius = 25
        
        for defensiveSit_id, defensive_sit_coord in setup.defensiveSit_fielder_coord.items():
            pygame.draw.circle(screen, setup.med_gray_c , defensive_sit_coord, radius)
            
            text = "#" + str(defensiveSit_id)
            
            # string_, colour, coord, font, justification: 1 = topleft 2 = center
            screenPrinter.draw_text(text, 'white', defensive_sit_coord, setup.font12, 2)
            
        
    ## Measure the distance from Home in feet 
    def draw_measuring_tape():
            
        """ Arc from Home """
        centroid = setup.boundaries['four_B_tip']    
                    
        Q = pygame.mouse.get_pos()
        RC = (Q[0], centroid[1]) # Note, centroid is off screen (below)
        
        # Get theta
        theta_rad = helpers.coord_to_theta(centroid, Q)

        """ For arc describing OF wall """     
        end_coord = Q
        start_coord = centroid

        ## Set up on-screen coordinates
        for text_coord in range(1):
            coord_str = "(" + str( int(end_coord[0]) ) + ", " + str( int(end_coord[1]) ) + ")"
            
            distance_in_feet = helpers.measure_distance_in_feet(start_coord, end_coord)
            distance_str = str( int(distance_in_feet) ) + "'" 
            
            theta_str = str( int(math.degrees(theta_rad)) ) + "\u00b0"
            
            texts = [coord_str, distance_str, theta_str]

            ## Draw     
            x = end_coord[0]+20

            for i, text in enumerate(texts):
                y = end_coord[1] - 10 + (20 * i)
                screenPrinter.draw_text(text, 'black', (x, y), setup.font15, 1)
            
        pygame.draw.line(screen, 'red', start_coord, end_coord, 4)


##### ***** MAIN LOOP ***** #####

exit = False

while not exit:
    
    clock.tick(fps)
    
    ## Draw background objects
    screen.fill('white')
    draw_background()


    ### Events ### 
    # s = run test situation | m = toggle measuring tape | b = show boundary markers | d = show defensive situations coord 
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            exit = True

        ## Runner movement events
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                exit = True

            for start_movement in range(1):
                if event.key == K_LEFT or event.key == K_KP4:
                    left = True

                if event.key == K_RIGHT or event.key == K_KP6:
                    right = True

                if event.key == K_UP or event.key == K_KP8:
                    north = True

                if event.key == K_DOWN or event.key == K_KP2:
                    south = True


            ## Modify launch velo and angle 
            for modify_launch_metrics_deltas in range(1):
                
                delta = 1

                if event.key == K_w:
                    launch_metrics_deltas['launch_angle'] = delta

                if event.key == K_s:
                    launch_metrics_deltas['launch_angle'] = -delta

                if event.key == K_d:
                    launch_metrics_deltas['exit_velo'] = delta

                if event.key == K_a:
                    launch_metrics_deltas['exit_velo'] = -delta

                if event.key == K_x:
                    launch_metrics_deltas['launch_direction'] = -delta

                if event.key == K_z:
                    launch_metrics_deltas['launch_direction'] = delta


            ### Set up stuff
            # Option selection keys

            for i, num_key in enumerate( [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9] ):
                if event.key == num_key:
                    num_keys[i] = True


            for modify_and_meta in range(1):

                if event.key == K_l:
                    reset_numkeys()
                    gamePlay.reset_play()
                    gamePlay.update_curr_defensiveSit(0)

                if event.key == K_RETURN:
                    gamePlay.update_situation_start(True)

                if event.key == K_b:
                    show_boundary_markers = not(show_boundary_markers)

                if event.key == K_n:
                    show_defensiveSit_coord = not(show_defensiveSit_coord)

                if event.key == K_m:
                    measuring_tape = not(measuring_tape)

                if event.key == K_SPACE:
                    gamePlay.batted_launch()

                if event.key == K_r:
                    gamePlay.advance_baserunner()

                if event.key == K_k:
                    gamePlay.drop_ball()
                    
                if event.key == K_h:
                    gamePlay.throw_ball()

                if event.key == K_j:
                    gamePlay.change_throw_receiver()


        ## KEYUP
        if event.type == KEYUP:
            
            for end_movement in range(1):
                if event.key == K_LEFT or event.key == K_KP4:
                    left = False
                
                if event.key == K_RIGHT or event.key == K_KP6:
                    right = False
                    
                if event.key == K_UP or event.key == K_KP8:
                    north = False
                
                if event.key == K_DOWN or event.key == K_KP2:
                    south = False
            
            launch_metrics_deltas['exit_velo'] = 0
            launch_metrics_deltas['launch_angle'] = 0
            launch_metrics_deltas['launch_direction'] = 0
    
    
        for mouse_button_events in range(1):
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click
                    mouse_drag_ball_toggle = True
        
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Left click
                    mouse_drag_ball_toggle = False
                    

    #### Main actions ####
    
    ## Display markers / anchor points
    for meta_funcs in range(1):
        if show_boundary_markers:
            draw_boundary_markers()
        
        if show_defensiveSit_coord:
            draw_defensiveSit_id() ## 
            
        if measuring_tape:
            draw_measuring_tape()

    ## Pre-pitch things
    for package_gameplay_updates in range(1):
        keyboard_input = [left, right, north, south] 
        gamePlay.packaged_updates(keyboard_input, mouse_drag_ball_toggle)
    
    curr_defensiveSit = choose_situation(curr_defensiveSit)
    num_keys = reset_numkeys()
    
    prev_ticks = control_ticks_for_launch_data(prev_ticks, launch_metrics_deltas)
    
    ## Baseball situation execition 
    gamePlay.master_gameplay_control()


    pygame.display.update() 

# Last line