""" April 25, 2024 -- SIDE QUEST TO GET SMART AT VIDEO GAME PHYSICS / FIRING CANNONBALL... 

"""

import pygame
from pygame.locals import *
import math
from helpers_angryBats import Helpers

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(1, 30) # Opens Pygame to top-left of monitor


##### ***** INITIALIZE PYGAME AND PYMUNK ***** #####
pygame.init()
screen_w = 2200 #3400 #= optimal for my widescreen
screen_h = 1350
screen = pygame.display.set_mode((screen_w, screen_h))

helper = Helpers(screen)

## Game clock 
clock = pygame.time.Clock()
fps = 45

##### Set key boundary constants #####

## Preliminary constants
for FALSE_LOOP in range(1):
    
    pixels_per_foot = 2.8088 # conversion -- from 3BC_alpha

    ## Foundational var
    floor_thickness = 17
    wall_thickness = 10    
    top_of_floor = screen_h - (floor_thickness / 2 )

    ## Playing field
    field_width_x = 1210 # pixels > (950, 35) - (950, 1245) from 3BC_alpha > setup
    of_width_x = 310 * pixels_per_foot
    inf_width_x = field_width_x - of_width_x
    
    ## Key x markers 
    inf_start_x = wall_thickness + of_width_x
    launchZone_start_x = inf_start_x + inf_width_x
    text_display_start_x = launchZone_start_x + 400
    
    ## Colours
    extremely_light_gray = (240, 240, 240)
    very_light_gray_c = (220, 220, 220)
    inf_gray_c = (192, 192, 192)
    med_gray_c = (128, 128, 128)
    dark_gray_c = (47,47,47)
    green_grass_c = (65,152,10)
    extremely_light_blue_c = (225, 245, 245)

    ##### Ball variables #####
    
    ## Basic ball var
    ball_coord_pg = ball_start_coord = (200, screen_h - 200)
    ball_radius = 9
    ball_edge_thickness = 2
    
    ## Ball gravity stuff
    #gravity = 1.7  ## Manually calibrated to 1.7 -- ideal at 200', a little slow at 100'. Note, based on acceleration taking in time in seconds, not miliseconds
    time_of_ball_start_flight_ms = pygame.time.get_ticks()
    time_of_ball_start_roll_ms = pygame.time.get_ticks()
    
    ## Ball launch stuff
    batted_ball_start_y = screen_h - floor_thickness - (4 * pixels_per_foot) ## 4' | This is also used to draw the launch nub
    batted_ball_start_coord = ( wall_thickness + field_width_x - ball_radius,  batted_ball_start_y)
    ball_launch_start_coord = batted_ball_start_coord ## Separating fromn batted ball's start coord to enable "launches" for throws
    ball_height_feet = 0
    ball_velo_mph = 0
    launch_reporting_data = [0, 0, 0]
    ball_x__distance_from_home = 0
    

    # with gravity of 120, launch velo of 360 mimics about 95 mph  
    gravity = 120 

    launch_angle = 1
    angle_deg = 180 - launch_angle
    angle_rad = math.radians(angle_deg)
    
    launch_velo_mph = 55
    launch_velo = launch_velo_mph * 3.79
    
    drag_factor_gravel = 41
    drag_factor_grass = 50    
    
    ball_prev_coord_pg = ball_start_coord #For measuring ball velo 
    
    
    ## Toggles
    mouse_drag_ball_toggle = False
    ball_falling_toggle = False ## Ball is falling after being click-dragged  
    ball_launched_toggle = False ## Space bar to launch
    ball_rolling_toggle = False
    pause_toggle = False
-------------------------------------


### MAIN FUNCTIONS
def draw_background(screen_w, screen_h):
     
    #### Playing field ###

    ## WALL: Draw a thin OF wall
    x = 4
    height = 300
    start_coord_pg = (x, screen_h)
    end_coord_pg = (x, screen_h - height)
    pygame.draw.line(screen, dark_gray_c, start_coord_pg, end_coord_pg, wall_thickness)
    
    ## FLOOR: Draw a green OF ~ 420-120 ~ 300'
    tilt = 0 # make the object angled to create a cool bounce ... for testing
    start_coord_pg = (wall_thickness, top_of_floor - tilt)
    end_coord_pg = (inf_start_x, top_of_floor)
    pygame.draw.line(screen, green_grass_c, start_coord_pg, end_coord_pg, floor_thickness)
    
    ##FLOOR: Draw a gray infield ~ 120'
    start_coord_pg = (inf_start_x, top_of_floor)
    end_coord_pg = (launchZone_start_x, top_of_floor)
    pygame.draw.line(screen, inf_gray_c, start_coord_pg, end_coord_pg, floor_thickness)

    #### Non-playing field ###    
    ### Launch zone

    ## Draw a subtle background for the launch zone
    left = launchZone_start_x
    top = 0
    width = text_display_start_x - launchZone_start_x # #400
    height = screen_h
    pygame.draw.rect( screen, extremely_light_blue_c, pygame.Rect(left, top, width, height) )
    
    ## FLOOR: Draw the launch zone floor
    start_coord = (launchZone_start_x, top_of_floor)
    end_coord = (text_display_start_x, top_of_floor)
    pygame.draw.line(screen, 'blue', start_coord, end_coord, floor_thickness)
    
    ## WALL: Draw launch 'nub' -- top is roughly point of contact on ball launches 
    start_coord = (launchZone_start_x, batted_ball_start_y)
    end_coord = (launchZone_start_x, screen_h)
    pygame.draw.line(screen, 'blue', start_coord, end_coord, 5)
    
    #### Text interface zone
     
    ## Draw vertical line demarcating text interface zone
    start_coord = (text_display_start_x, 0)
    end_coord = (text_display_start_x, screen_h)
    pygame.draw.line(screen, med_gray_c, start_coord, end_coord, wall_thickness)
    
    ### Draw a border along the top of the screen
    start_coord = (0, 4)
    end_coord = (screen_w, 4)
    pygame.draw.line(screen, med_gray_c, start_coord, end_coord, wall_thickness)


def write_text_onScreen(ball_coord_pg, ball_velo_mph, ball_height_feet, ball_x__distance_from_home, total_time_ball_flight_seconds, gravity_delta_y, launch_reporting_data, ball_rolling_toggle, ball_launched_toggle):
    text_x = launchZone_start_x + 50
    text_y = 400 
    
    mouse_coord = pygame.mouse.get_pos()
    mouse_coord_text = "Mouse coord: ("   +   str(mouse_coord[0])   +   ", "   +   str(mouse_coord[1])   +   ")"
    ball_coord = ( int(ball_coord_pg[0]), int(ball_coord_pg[1]) ) 
    ball_coord_text = "Ball coord: " + str( ball_coord)

    
    #ball_clicked_text = "Ball clicked: " + str(mouse_drag_ball_toggle)
    #ball_falling_toggle_text = "Ball falling: " + str(ball_falling_toggle)
    ball_launched_toggle_text = "Ball launched: " + str(ball_launched_toggle)
    ball_rolling_toggle_text = "Ball rolling: " + str(ball_rolling_toggle)
    ball_height_feet_text = "Ball height: " + str( int(ball_height_feet) )  + "'"    
    ball_x_distance_feet_text = "Ball distance from home: " + str( int(ball_x__distance_from_home) )  + "'"  
    ball_velo_text = "Ball velo: " + str( int(ball_velo_mph) )  + " mph"
    gravity_delta_y_text = "Gravity delta y: " + str( int(gravity_delta_y)) + " pixels"
    
    # launch_reporting_data = [launch_vector_x, launch_vector_y, launch_delta_y]
    launch_vector_x_text = "Launch vector x: " + str( int(launch_reporting_data[0]) ) + " pixels"     
    #launch_vector_y_text = "Launch vector y: " + str( int(launch_reporting_data[1]) ) + " pixels"
    #launch_delta_y_text = "Launch delta y: " + str( int(launch_reporting_data[2]) ) + " pixels"              
      
    total_time_falling_seconds_text = "Time falling: " + str( round(total_time_ball_flight_seconds, 1) )  + " seconds"
    
    instruction_text = [mouse_coord_text, ball_coord_text, "",
                        ball_launched_toggle_text, ball_rolling_toggle_text, "",
                        ball_height_feet_text, ball_x_distance_feet_text, ball_velo_text, "", 
                        gravity_delta_y_text, launch_vector_x_text, "", 
                        total_time_falling_seconds_text,
                        ] 
    
    helper.print_instruction_iterable(instruction_text, text_x, text_y)
    

#Get ball height in feet 
def get_height_ball(ball_coord_pg): 
    height_in_pixels = screen_h - floor_thickness - ball_coord_pg[1]
    
    return height_in_pixels / pixels_per_foot
    

def get_x_distance_from_home_ball(ball_coord_pg):
    distance_in_pixels = launchZone_start_x - ball_coord_pg[0] 
    
    return distance_in_pixels / pixels_per_foot


def get_total_time_seconds(start_time_ms):
    
    current_time = pygame.time.get_ticks()
    total_time_seconds = (current_time - start_time_ms) / 1000
    
    return total_time_seconds

    
#Get mph for text display, and to de-activate "Ball Falling" acceleration timer and calculation 
def get_velo_ball(ball_coord_pg, ball_prev_coord_pg):

    distance_in_feet = helper.measure_distance_in_feet(ball_prev_coord_pg, ball_coord_pg)
    feet_per_second = distance_in_feet * fps # Game runs at 1/fps, so 45 frames in 1 IRL second
    
    ball_velo_mph = feet_per_second * (3600/5280)
    
    ball_prev_coord_pg = ball_coord_pg # Reset prev ball_coord to measure distance on the next frame


    return ball_velo_mph, ball_prev_coord_pg


def get_gravity_delta_y(total_time_ball_flight_seconds):
    delta_y = (0.5) * gravity * (total_time_ball_flight_seconds**2)
    return delta_y

## Ball falls after being click-dragged
def do_ball_falling(ball_coord_pg, total_time_ball_flight_seconds, gravity_delta_y):

    if ball_falling_toggle:
        y = ball_coord_pg[1]
        y += gravity_delta_y
        
        ball_coord_pg = (ball_coord_pg[0], y)  ## need to return ball_coord_pg in either case -- ball falling or not
    
    return ball_coord_pg
    

## User actions

def move_ball_in_air(ball_coord_pg, gravity_delta_y):
    reporting_data = [0, 0, 0]  ## If we're not launching a ball have a value to return
    
    if ball_launched_toggle:
        
        ## Set up some variables
        start_x, start_y = ball_launch_start_coord[0], ball_launch_start_coord[1]
        time = total_time_ball_flight_seconds
        
        drag_vector = 0
        if ball_rolling_toggle:
            drag_vector = roald_dahl(ball_coord_pg[0])
            print(f"Drag vector: {int(drag_vector)}")
            
        ## Delta x
        launch_vector_x = math.cos(angle_rad) * launch_velo
        launch_delta_x =  launch_vector_x * time
        new_x = start_x + launch_delta_x + drag_vector
        
        ## Delta y
        launch_vector_y = -1 * (math.sin(angle_rad) * launch_velo)
        launch_delta_y =  launch_vector_y * time
        new_y = start_y + launch_delta_y + gravity_delta_y

        ball_coord_pg = (new_x, new_y)
        
        ## Show a marker to help me see the launch angle
        show_theta_line(angle_deg, (start_x, start_y)   )
        
        reporting_data = [launch_vector_x, launch_vector_y, launch_delta_y ]
        
    return ball_coord_pg, reporting_data, 


def check_ball_start_rolling(time_of_ball_start_roll_ms, ball_rolling_toggle):
    if ball_launched_toggle:
        if total_time_ball_flight_seconds > 1:
            if ball_coord_pg[1] >= top_of_floor - 20 : # If the ball is at or below the top of the floor
                time_of_ball_start_roll_ms = pygame.time.get_ticks()
                ball_rolling_toggle = True
                
    
    return time_of_ball_start_roll_ms, ball_rolling_toggle


def roald_dahl(curr_x):
    
    tolerance = 10 ## fudge factor to prevent a ball from leaping backwards and getting stuck in a loop
    
    ## slow more if it's on grass
    drag_vector = 0
    
    if curr_x > inf_start_x + tolerance:
        drag_vector = drag_factor_gravel * total_time_ball_rolling_seconds**2
    
    elif curr_x <= inf_start_x - tolerance:
        drag_vector = drag_factor_grass * total_time_ball_rolling_seconds**2
    
    return drag_vector
    


def show_theta_line(theta_deg, start_coord):
    length_of_line = 300

    end_coord = helper.theta_to_endCoord(start_coord, theta_deg, length_of_line)
    
    pygame.draw.line(screen, 'blue', start_coord, end_coord, 3)
    pygame.draw.circle(screen, 'red', start_coord, 5)


def do_mouse_drag_ball(ball_coord_pg):
    if mouse_drag_ball_toggle:
        x, y = pygame.mouse.get_pos()
        
        ball_coord_pg = (x, y)
    
    return ball_coord_pg


## Render ball, keeping it within the playing area
def check_collisions(ball_coord_pg):
    x, y = ball_coord_pg
    
    x = min(x, launchZone_start_x - ball_radius - (wall_thickness//2) + 1 ) # Right edge
    x = max(x, wall_thickness + ball_radius) # Left edge
    y = min(y, screen_h - ball_radius - floor_thickness ) # bottom
    y = max(y, wall_thickness//2 + ball_radius + 1) # Top
    
    return (x, y)


def draw_ball(ball_coord_pg):
    pygame.draw.circle(screen, extremely_light_gray, ball_coord_pg, ball_radius-ball_edge_thickness)
    pygame.draw.circle(screen, med_gray_c, ball_coord_pg, ball_radius, ball_edge_thickness)
    
    
##### ***** MAIN LOOP ***** #####

exit = False
print(top_of_floor)

while not exit:
    
    clock.tick(fps)
    
    ## Draw background objects
    screen.fill('white')
    draw_background(screen_w, screen_h)

    ### Events ### 
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            exit = True

        ## Movement events
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                exit = True
            
            ## Option selection keys
            if event.key == K_p:
                if not(pause_toggle):
                    time_of_ball_start_flight_ms += total_time_ball_flight_seconds ### When I unpause, make it as though time was paused too by moving the start time forward
                pause_toggle = not(pause_toggle) 
         
            if event.key == K_SPACE:
                ball_launched_toggle = not(ball_launched_toggle)
                ball_coord_pg = ball_launch_start_coord  ## Move the ball to the contact point prior to launch. These start coord are used during the entire flight 
                time_of_ball_start_flight_ms = pygame.time.get_ticks() ## Start counting the t factor in acceleration

        ## Mouse button events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                mouse_drag_ball_toggle = True
                ball_falling_toggle = False

            
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Left click
                mouse_drag_ball_toggle = False
                ball_falling_toggle = True
                time_of_ball_start_flight_ms = pygame.time.get_ticks() ## Start counting the t factor in acceleration
            
    
    #### Main actions ####    
    if ball_rolling_toggle == False:
        time_of_ball_start_roll_ms, ball_rolling_toggle = check_ball_start_rolling(time_of_ball_start_roll_ms, ball_rolling_toggle)

    total_time_ball_flight_seconds = get_total_time_seconds(time_of_ball_start_flight_ms)
    total_time_ball_rolling_seconds = get_total_time_seconds(time_of_ball_start_roll_ms)
    
    """
    if pause_toggle:
        draw_ball(ball_coord_pg)
        write_text_onScreen( ball_coord_pg, ball_velo_mph, ball_height_feet, ball_x__distance_from_home, total_time_ball_flight_seconds, gravity_delta_y, launch_reporting_data)
        continue ## if we're in pause mode, freeze the screen as it is, but accept kb entry to unpause, etc
    """
    
    ## Get inputs to ball motion calculations
    gravity_delta_y = get_gravity_delta_y(total_time_ball_flight_seconds)
    
    ## Get the ball's velo. If too slow and it wasn't just dropped turn off "Falling" (cease calculating falling when it's stopped)
    ball_velo_mph, ball_prev_coord_pg = get_velo_ball(ball_coord_pg, ball_prev_coord_pg)
    
    
    ## Bring ball graciously to a STOP
    if ball_velo_mph < 3 and total_time_ball_flight_seconds > 1 and ball_height_feet < 5:
        #ball_falling_toggle = False
        ball_launched_toggle = False
        ball_rolling_toggle = False
        
    
    ### User actions
    
    ## Ball falling after mouse drag

    ball_coord_pg = do_mouse_drag_ball(ball_coord_pg)
    ball_coord_pg = do_ball_falling(ball_coord_pg, total_time_ball_flight_seconds, gravity_delta_y)


    ## Ball launched after hitting <space> . vectors are just for text displayed on screen
    ## Move launched ball     
    ball_coord_pg, launch_reporting_data = move_ball_in_air(ball_coord_pg, gravity_delta_y)
    
    ### Render ball, keeping it within the playing area
    ball_coord_pg = check_collisions(ball_coord_pg)
    draw_ball(ball_coord_pg)
    

    ## Report data in the user interface ####
    ball_height_feet = get_height_ball(ball_coord_pg)
    ball_x__distance_from_home = get_x_distance_from_home_ball(ball_coord_pg) 
    write_text_onScreen( ball_coord_pg, ball_velo_mph, ball_height_feet, ball_x__distance_from_home, total_time_ball_flight_seconds, gravity_delta_y, launch_reporting_data, ball_rolling_toggle, ball_launched_toggle)
    
        
    pygame.display.update()

pygame.quit()

