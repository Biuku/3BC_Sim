""" April 28, 2024 -- SIDE QUEST TO GET SMART AT VIDEO GAME PHYSICS / FIRING CANNONBALL... 

Will do a big refactor of this today, April 28

"""

import pygame
from pygame.locals import *
import math
from helpers_angryBats import Helpers
from helpers_angryBats import ScreenPrinter
from setup_angryBats import Setup
#from gameplay_angryBats import GamePlay
from ball import Ball

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(1, 30) # Opens Pygame to top-left of monitor


##### ***** INITIALIZE PYGAME ***** #####
pygame.init()

# Game clock
clock = pygame.time.Clock()
fps = 45

# Master screen   
screen_w = 2200 #3400 #= optimal for my widescreen
screen_h = 1350
screen = pygame.display.set_mode((screen_w, screen_h))

## Class composition
helper = Helpers(screen)
screenPrinter = ScreenPrinter(screen, screen_w - 500)
setup = Setup(screen, screen_w, screen_h)
ball = Ball(screen, screen_w, screen_h, fps)


## Game togggles
mouse_drag_ball_toggle = False
pause_toggle = False


### MAIN FUNCTIONS
def draw_background():
    screen.fill('white')
    setup.draw_playing_area()
    setup.draw_launch_zone()
    setup.draw_text_inferface_zone()
    

def write_text_onScreen():
    screenPrinter.new_frame() ## Reset y for start row of printing on screen
    
    ## Send to screen
    screenPrinter.print_coord( ["Ball coord", ball.master_coord, ""] )
    screenPrinter.print_coord( ["Mouse coord", pygame.mouse.get_pos(), ""] )
    screenPrinter.paragraph_break()
    
    screenPrinter.print_simple( ["Ball launched", ball.launched_toggle, ""] )
    screenPrinter.print_simple( ["Ball rolling", ball.rolling_toggle, ""] )
    screenPrinter.paragraph_break()
    
    screenPrinter.print_int( ["Ball height", ball.curr_height_feet, "' "])
    screenPrinter.print_int( ["Ball distance from home", ball.curr_distance_from_home_x_feet, "' "])
    #screenPrinter.print_int( ["Ball velo", ball.curr_velo_mph, " mph"])
    screenPrinter.paragraph_break()
    
    #screenPrinter.print_int( ["Gravity delta y", gravity_delta_y, " pixels"])
    #screenPrinter.paragraph_break()
    
    #screenPrinter.print_rounded( ["Time falling", total_time_ball_flight_seconds, " seconds"], 1 )
        

""" I think I'll remove 'ball falling' from this; i.e., not migrate this to the ball object -- it wasn't helpful in calculating gravity
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
"""


def show_theta_line(theta_deg, start_coord):
    length_of_line = 300

    end_coord = helper.theta_to_endCoord(start_coord, theta_deg, length_of_line)
    
    pygame.draw.line(screen, 'blue', start_coord, end_coord, 3)
    pygame.draw.circle(screen, 'red', start_coord, 5)


def do_mouse_drag_ball():
    if mouse_drag_ball_toggle:
        ball.mouse_drag_ball()
        
"""
## Render ball, keeping it within the playing area
def check_collisions(ball_coord_pg):
    x, y = ball_coord_pg
    
    x = min(x, launchZone_start_x - ball_radius - (wall_thickness//2) + 1 ) # Right edge
    x = max(x, wall_thickness + ball_radius) # Left edge
    y = min(y, screen_h - ball_radius - floor_thickness ) # bottom
    y = max(y, wall_thickness//2 + ball_radius + 1) # Top
    
    return (x, y)
"""

##### ***** MAIN LOOP ***** #####

exit = False


while not exit:
    
    clock.tick(fps)
    
    draw_background()

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
                pause_toggle = not(pause_toggle) 

            if event.key == K_SPACE:
                ball.launch_ball()
                
        ## Mouse button events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                mouse_drag_ball_toggle = True
                ball_falling_toggle = False

            
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Left click
                mouse_drag_ball_toggle = False
                ball_falling_toggle = True
                #time_of_ball_start_flight_ms = pygame.time.get_ticks() ## Start counting the t factor in acceleration


    #### Main actions ####  


    if not(pause_toggle):
       
        ### User actions
        do_mouse_drag_ball()

        ## Move launched ball | Ball launched after hitting <space>
        ball.move_ball_in_air()
        ball.check_collisions()
    
    ball.draw_ball()
    write_text_onScreen()
        
    pygame.display.update()

pygame.quit()

