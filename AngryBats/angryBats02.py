""" April 28, 2024 -- SIDE QUEST TO GET SMART AT VIDEO GAME PHYSICS / FIRING CANNONBALL... 

Will do a big refactor of this today, April 28

"""

import pygame
from pygame.locals import *
import math
from helpers_angryBats import Helpers
from helpers_angryBats import ScreenPrinter
from setup_angryBats import Setup
from ball2 import Ball

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(1, 30) # Opens Pygame to top-left of monitor


##### ***** INITIALIZE PYGAME ***** #####
pygame.init()

# Game clock
clock = pygame.time.Clock()
fps = 90

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

    #screenPrinter.print_coord( ["Mouse coord", pygame.mouse.get_pos(), ""] )
    screenPrinter.print_simple( ["Exit velo", ball.launch_velo_mph, ""] )
    screenPrinter.print_simple( ["Launch angle", ball.launch_angle_leftward, ""] )
    screenPrinter.paragraph_break()
        
    #screenPrinter.print_simple( ["Ball launched", ball.launched_toggle, ""] )
    #screenPrinter.print_simple( ["Ball rolling", ball.rolling_toggle, ""] )
    #screenPrinter.print_simple( ["Ball bouncing", ball.bounce_toggle, ""] )
    #screenPrinter.paragraph_break()
    
    #screenPrinter.print_coord( ["Ball coord", ball.master_coord, ""] )
    screenPrinter.print_int( ["Ball height", ball.curr_height_feet, "' "])
    screenPrinter.print_int( ["Max ball height", ball.max_height_feet, "' "])
    screenPrinter.print_int( ["Ball distance from home", ball.curr_distance_from_home_x_feet, "' "])
    screenPrinter.paragraph_break()
    
    screenPrinter.print_int( ["Ball total velo", ball.curr_velo_mph, " mph"])
    #screenPrinter.print_rounded( ["Velocity X", ball.velocity_x_pg, " pixels per frame"], 1 )
    #screenPrinter.print_rounded( ["Velocity Y", ball.velocity_y_pg, " pixels per frame"], 1 )
    screenPrinter.paragraph_break()
    
    screenPrinter.print_rounded( ["Total flight/air time", ball.flight_duration_s, " seconds"], 1 )
    screenPrinter.print_rounded( ["Total time till end", ball.total_duration_s, " seconds"], 1 )
    screenPrinter.print_int( ["# bounces", ball.bounce_count, ""])
    #screenPrinter.print_rounded( ["Time since bounce", ball.bounce_duration_s, " seconds"], 1 )
    #screenPrinter.print_rounded( ["Duration of rolling", ball.rolling_duration_s, " seconds"], 1 )
     

def do_mouse_drag_ball():
    if mouse_drag_ball_toggle:
        ball.mouse_drag_ball()
        

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
            
            if event.key == K_LEFT:
                ball.launch_velo_mph -= 5
            
            if event.key == K_RIGHT or event.key == K_KP6:
                ball.launch_velo_mph += 5
                
            if event.key == K_UP:
                ball.launch_angle_leftward += 2
            
            if event.key == K_DOWN:
                ball.launch_angle_leftward -= 2
                
            
                
        ## Mouse button events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                mouse_drag_ball_toggle = True
                

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Left click
                mouse_drag_ball_toggle = False


    #### Main actions ####  

    if not(pause_toggle):
       
        ### User actions
        do_mouse_drag_ball()

        ## Move launched ball | Ball launched after hitting <space>
        ball.move_ball()
    
    ball.draw_ball()
    write_text_onScreen()
        
    pygame.display.update()

pygame.quit()

