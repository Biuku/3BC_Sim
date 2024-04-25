""" April 25, 2024 -- SIDE QUEST TO GET SMART AT VIDEO GAME PHYSICS / FIRING CANNONBALL... 

"""

import pygame
from pygame.locals import *
#import math
import pymunk
from helpers import Helpers

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(1, 30) # Opens Pygame to top-left of monitor

##### ***** INITIALIZE PYGAME AND PYMUNK ***** #####
pygame.init()
screen_w = 2200 #3400 #= optimal for my widescreen
screen_h = 1350
screen = pygame.display.set_mode((screen_w, screen_h))

space = pymunk.Space()
space.gravity = 0, -32.2/2.8088 # -100 # -5 # See below for why -5
elasticity_ = .8


""" Setting the right gravity 
- The screen is about 1330 pixels high = 3758' high
- It should take 15.8s to hit the ground (Chat GPT, but sounds about right from skydiving...)
- Well -5 got me 13.5s... it's blood slow... not sure it will feel realistic. 
    I can cross-check with the math for cannonball arcs when i start launching balls

"""

helper = Helpers(screen)

## Game clock 
clock = pygame.time.Clock()
fps = 45


##### Set key boundary constants #####

## Preliminary constants
for FALSE_LOOP in range(1):
    floor_thickness = 17
    wall_thickness = 10
    pixels_per_foot = 2.8088 # conversion -- from 3BC_alpha

    ## Playing field
    field_width_x = 1210 # pixels > (950, 35) - (950, 1245) from 3BC_alpha > setup
    of_width_x = 310 * pixels_per_foot
    inf_width_x = field_width_x - of_width_x
    of_wall_height_y = int(100 * pixels_per_foot)

    ## Non-playing field
    launchZone_width_x = 400 
    text_interface_border_x = field_width_x + launchZone_width_x
    
    ## height of ball when batted
    launch_height_y = 3 * pixels_per_foot # 3'

    ## Colours
    extremely_light_gray = (240, 240, 240)
    very_light_gray_c = (220, 220, 220)
    inf_gray_c = (192, 192, 192)
    med_gray_c = (128, 128, 128)
    dark_gray_c = (47,47,47)
    green_grass_c = (65,152,10)
    extremely_light_blue_c = (225, 245, 245)

    ##### Set ball-object variables #####
    ball_start_coord = (200, screen_h - 300)
    ball_radius = 9
    ball_thickness = 2
    ball_c =  med_gray_c
    
    ball_prev_coord_pg = ball_start_coord
    ball_curr_velo = ball_prev_velo_mph = 0
    ball_acceleration_mph = 0
    

## Game toggles
ball_clicked = False

### MAIN FUNCTIONS
def draw_background(screen_w, screen_h):

    ### Set up ###    
    top_of_floor = screen_h - (floor_thickness / 2 )
        
        
    #### Playing field ###

    ## WALL: Draw a thin OF wall
    x = 4
    start_coord_pg = (x, 0)
    end_coord_pg = (x, screen_h)
    pygame.draw.line(screen, dark_gray_c, start_coord_pg, end_coord_pg, wall_thickness)
    # PYMUNK
    # to do ... 
    
    
    ## FLOOR: Draw a green OF ~ 420-120 ~ 300'
    tilt = 35 # make the object angled to create a cool bounce ... for testing
   
    start_coord_pg = (wall_thickness, top_of_floor - tilt)
    end_coord_pg = (wall_thickness + of_width_x, top_of_floor)
    pygame.draw.line(screen, green_grass_c, start_coord_pg, end_coord_pg, floor_thickness)
    
    # PYMUNK
    start_coord_pm = convert_coord( start_coord_pg )
    end_coord_pm = convert_coord( end_coord_pg )
    segment_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    segment_shape = pymunk.Segment(segment_body, start_coord_pm, end_coord_pm, 5)
    segment_shape.elasticity = elasticity_ 
    space.add(segment_body, segment_shape)
    
    
    ##FLOOR: Draw a gray infield ~ 120'
    start_coord_pg = (wall_thickness + of_width_x, top_of_floor)
    end_coord_pg = (wall_thickness + field_width_x, top_of_floor)
    pygame.draw.line(screen, inf_gray_c, start_coord_pg, end_coord_pg, floor_thickness)
    # PYMUNK
    # to do ... 
       
    #### Non-playing field ###
    
    ### Launch zone

    ## Draw a subtle background for the launch zone
    left = field_width_x
    top = 0
    width = launchZone_width_x
    height = screen_h
    pygame.draw.rect( screen, extremely_light_blue_c, pygame.Rect(left, top, width, height) )
    
     
    ## FLOOR: Draw the launch zone floor
    y = screen_h - floor_thickness//2
    start_coord = (field_width_x, y)
    end_coord = (text_interface_border_x, y)
    pygame.draw.line(screen, 'blue', start_coord, end_coord, floor_thickness)
    
    ## WALL: Draw a thin vertical line demarcating the launch zone
    #y = screen_h - of_wall_height_y
    y = screen_h - floor_thickness - launch_height_y  ## 3' off the ground
    start_coord = (field_width_x, y)
    end_coord = (field_width_x, screen_h)
    pygame.draw.line(screen, 'blue', start_coord, end_coord, 5)
    
    #### Text interface zone
     
    ## Draw line demarcating text interface zone
    start_coord = (text_interface_border_x, 0)
    end_coord = (text_interface_border_x, screen_h)
    pygame.draw.line(screen, med_gray_c, start_coord, end_coord, wall_thickness)
    
    ### Draw a border along the top of the screen
    start_coord = (0, 4)
    end_coord = (screen_w, 4)
    pygame.draw.line(screen, med_gray_c, start_coord, end_coord, wall_thickness)


def write_text_onScreen(body, ball_curr_velo_mph, ball_acceleration):
    text_x = text_interface_border_x + 50
    text_y = 400 
    
    mouse_coord = pygame.mouse.get_pos()
    pm_coord = body.position
    
    mouse_coord_text = "Mouse coord: ("   +   str(mouse_coord[0])   +   ", "   +   str(mouse_coord[1])   +   ")"
    pm_coord_text = "Pymunk coord: ("   +   str(int(pm_coord[0]))   +   ", "   +   str(int(pm_coord[1]))   +   ")"
    ball_clicked_text = "Ball clicked: " + str(ball_clicked)
    
    ## Ball velo calculated manually from comparing feet moved per frame to frames-per-second 
    ball_clock_velo_text = "Ball velocity from game clock: " + str( int(ball_curr_velo_mph) )  + " mph"
    
    ## Ball velo pulled from Pymunk object
    ball_pm_velo_text = "Ball velocity from Pymunk object: " + str( int(body.velocity.length) ) + ""
    
    ## Acceleration 
    ball_acceleration_text = "Ball acceleration from game clock: " + str( round(ball_acceleration, 2) ) + " mph^2"
    
                                              
    instruction_text = [mouse_coord_text, pm_coord_text, ball_clicked_text, ball_clock_velo_text, ball_pm_velo_text, ball_acceleration_text]
    
    helper.print_instruction_iterable(instruction_text, text_x, text_y)
    
    
    

def convert_coord(coord):
    return coord[0], screen_h - coord[1]
    ## It's the same formula for pg > pm and reverse. Assume y = 25 pixels from the bottom in pg
    # pm > pg  >  pg = 1000 - 25 = 975
    # pg > pm  >  pm = 1000 - 975 = 25
    
    
#Get mph for text display only 
def get_velo_ball(ball_coord_pg, ball_prev_coord_pg):
    distance_in_feet = helper.measure_distance_in_feet(ball_prev_coord_pg, ball_coord_pg)
    feet_per_second = distance_in_feet * fps # Game runs at 1/fps, so 45 frames in 1 IRL second
    
    ball_curr_velo_mph = feet_per_second * (3600/5280)
    
    ball_prev_coord_pg = ball_coord_pg
    
    return ball_curr_velo_mph, ball_prev_coord_pg


def get_acceleration_ball(ball_prev_velo_mph, ball_curr_velo):
    # Velo's are mph, so need to convert 1 frame to a value in hours
    #time_frame = 1 / (60 * 60 * fps) 
    

    ball_acceleration_per_frame = ball_curr_velo - ball_prev_velo_mph
    ball_acceleration = ball_acceleration_per_frame / .001 #time_frame
    
    return ball_acceleration


##### *** PYMUNK *** #####
body = pymunk.Body()
body.position = convert_coord(ball_start_coord) #200, 400
shape = pymunk.Circle(body, 10)
shape.density = 1
shape.elasticity = elasticity_     
space.add(body, shape)



##### ***** MAIN LOOP ***** #####

current_time = pygame.time.get_ticks()
prev_time = current_time

exit = False

while not exit:
    
    clock.tick(fps)
    space.step(1/fps) # Pymunk flock tick control
    
    ## Draw background objects
    screen.fill('white')

    draw_background(screen_w, screen_h)

    ### Events ### 
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            exit = True

        ## Runner movement events
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                exit = True
            
            ## Option selection keys
            if event.key == K_s:
                gamePlay.update_situation_start(True)
         
            if event.key == K_SPACE:
                gamePlay.advance_baserunner()


        ## Mouse button events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                ball_clicked = True
            
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Left click
                ball_clicked = False
            
    
    #### Main actions ####

    
    if ball_clicked:
        x, y = pygame.mouse.get_pos()
        
        # Edge cases 
        x = min(x, text_interface_border_x - ball_radius - (wall_thickness//2) + 1 ) # Right edge
        x = max(x, wall_thickness + ball_radius) # Left edge
        y = min(y, screen_h - ball_radius - floor_thickness ) # bottom
        y = max(y, wall_thickness//2 + ball_radius + 1) # Top
        
        mouse_coord_pm = convert_coord( (x, y) )
        
        body.position = mouse_coord_pm
    
    ## Draw the ball controlled in Pymunk
    ball_coord_pg = convert_coord(body.position) ## Account for flipped y axis
    pygame.draw.circle(screen, extremely_light_gray, ball_coord_pg, ball_radius-ball_thickness)
    pygame.draw.circle(screen, ball_c, ball_coord_pg, ball_radius, ball_thickness)
    
    
    #### Capture metrics for reporting in the user interface ####
    
    ## Get ball velocity manually from distance travelled in PG coord over time  
    ball_curr_velo_mph, ball_prev_coord_pg = get_velo_ball(ball_coord_pg, ball_prev_coord_pg)
    
    ## Acceleration
    #ball_acceleration = get_acceleration_ball(ball_prev_velo_mph, ball_curr_velo_mph)
    current_time = pygame.time.get_ticks()
    
    if current_time - prev_time >= 1000:
        ball_acceleration_per_second = (ball_curr_velo_mph - ball_prev_velo_mph) / 1 # Just showing the unit
        ball_acceleration_mph = ball_acceleration_per_second * 60 * 60
        
        ball_prev_velo_mph = ball_curr_velo_mph
    
     

    write_text_onScreen(body, ball_curr_velo_mph, ball_acceleration_mph)
    

    pygame.display.update() 

pygame.quit()

