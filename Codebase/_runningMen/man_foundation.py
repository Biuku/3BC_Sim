""" Updated April 13 -- added Rect's and collision detection with bases """

import pygame
from pygame.locals import *
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0
import math

from helpers import Helpers
from setup import Setup
from screen_printer import ScreenPrinter


class Man: 

    def __init__(self, screen, coord, man_id, type):

        self.setup = Setup()
        self.helpers = Helpers()
        self.screenPrinter = ScreenPrinter(screen)
        
        self.screen = screen
        self.man_id = man_id
        self.type = type ## 'baserunner' or 'fielder'
                       
        for animation_frames in range(1):
            
            for frame_ingestion in range(1):
                # Baserunner -- team Red
                self.man_L1 = pygame.image.load("images/baserunners/man_left_1.png")  
                self.man_L2 = pygame.image.load("images/baserunners/man_left_2.png") 
                self.man_L3 = pygame.image.load("images/baserunners/man_left_3.png") 

                self.man_R1 = pygame.image.load("images/baserunners/man_right_1.png")
                self.man_R2 = pygame.image.load("images/baserunners/man_right_2.png") 
                self.man_R3 = pygame.image.load("images/baserunners/man_right_3.png")

                self.man_N1 = pygame.image.load("images/baserunners/man_north_1.png")
                self.man_N2 = pygame.image.load("images/baserunners/man_north_2.png")
                self.man_N3 = pygame.image.load("images/baserunners/man_north_3.png")
                self.man_N4 = pygame.image.load("images/baserunners/man_north_4.png")
                
                # Fielder -- team Blue
                self.fielder_L1 = pygame.image.load("images/fielders/man_left_1.png")  
                self.fielder_L2 = pygame.image.load("images/fielders/man_left_2.png") 
                self.fielder_L3 = pygame.image.load("images/fielders/man_left_3.png") 

                self.fielder_R1 = pygame.image.load("images/fielders/man_right_1.png")
                self.fielder_R2 = pygame.image.load("images/fielders/man_right_2.png") 
                self.fielder_R3 = pygame.image.load("images/fielders/man_right_3.png")

                self.fielder_N1 = pygame.image.load("images/fielders/man_north_1.png")
                self.fielder_N2 = pygame.image.load("images/fielders/man_north_2.png")
                self.fielder_N3 = pygame.image.load("images/fielders/man_north_3.png")
                self.fielder_N4 = pygame.image.load("images/fielders/man_north_4.png")
        
            ### Organize frames into lists     
            # Baserunner 
            self.baserunner_frames_L = cycle([self.man_L1, self.man_L2, self.man_L3, ]) # Doubling up frames to better match animation to locomotion without reducing fps to ridiculous level
            self.baserunner_frames_R = cycle([self.man_R1, self.man_R2, self.man_R3])
            self.baserunner_frames_N = cycle([self.man_N1, self.man_N2, self.man_N3, self.man_N4])
            
            # Fielder
            self.fielder_frames_L = cycle([self.fielder_L1,  self.fielder_L2, self.fielder_L3]) # Doubling up frames to better match animation to locomotion without reducing fps to ridiculous level
            self.fielder_frames_R = cycle([self.fielder_R1, self.fielder_R2, self.fielder_R3])
            self.fielder_frames_N = cycle([self.fielder_N1, self.fielder_N2, self.fielder_N3, self.fielder_N4])
        
            # Agnostics
            self.frames_L = None 
            self.frames_R = None 
            self.frames_N = None 
            self.make_frames_agnostic()

            ### Create first frame and rects             
            self.curr_frame = next(self.frames_L)
            self.man_rect = self.curr_frame.get_rect()
        
            ## Control animation speed separate from game fps
            self.prev_ticks = 0
            self.animation_speed_ticks = 40 ## Number of ticks between animation frames 
         
        for motion_and_position in range(1):
                    
            ### LOCOMOTION
            self.man_speed = .7 #4/3 # Optimal speed of NSEW locomotion = 4/3 -- pixels of movement per frame
            self.man_diagonal_factor = 0.744 ## Diagonal motion is 1.35x faster than North-South or lateral motion -- this should equalize that.
            
            self.theta_rad = 0 ## 
            self.direction_facing = 0 # 0 = None 1 = left | 2 = right | 3 = north
            
            ### Agnostic position
            self.sprite_size = [self.man_rect.width, self.man_rect.height]
            self.agnostic_pos = self.offset_pos(coord)
        
        ### Agnostic goal toggle 
        self.goal = False
        self.moving = False
        
        ### Agnostic
        self.man_rect.topleft = self.agnostic_pos

        ### Meta attributes -- colours for boxes used during development
        self.rect_colour = 'white' 
        self.rect_thickness = 1
        

 

    #### MAIN FUNCTIONS ####
    
    ### Instantiate agnostic frames
    
    def make_frames_agnostic(self):
        if self.type == 'fielder':
            self.frames_L = self.fielder_frames_L
            self.frames_R = self.fielder_frames_R 
            self.frames_N = self.fielder_frames_N 
        
        else:
            self.frames_L = self.baserunner_frames_L
            self.frames_R = self.baserunner_frames_R 
            self.frames_N = self.baserunner_frames_N 
            
    for move_and_draw_man in range(1):
                    
        def draw_man(self):
                self.man_rect.x = self.agnostic_pos[0]
                self.man_rect.y = self.agnostic_pos[1]
                
                if self.moving:
                    self.control_animation_speed()                    
                  
                self.screen.blit(self.curr_frame, self.man_rect)
                pygame.draw.rect(self.screen, self.rect_colour, self.man_rect, self.rect_thickness)
                
                ## Write fielder ID on fielder
                if self.type == 'fielder':

                    x = self.man_rect.x + 16
                    y = self.man_rect.y + 42
                    
                    text = "F" + str(self.man_id)
                    
                    self.screenPrinter.draw_text(text, 'black', (x, y), self.setup.font12, 2)
    
    
        def control_animation_speed(self):
            
            ## Slow down the animation frame rate relative to overall fps
            ticks = pygame.time.get_ticks()
            
            if ticks - self.prev_ticks > self.animation_speed_ticks:
                self.prev_ticks = ticks
            
                if self.direction_facing == 1:
                    self.curr_frame = next(self.frames_L)

                elif self.direction_facing == 2:
                    self.curr_frame = next(self.frames_R)
                
                elif self.direction_facing == 3:
                    self.curr_frame = next(self.frames_N)

    

 
        def move_man(self, left, right, north, south):
            
            ## Only advance the animation when moving
            self.moving = False       
            if right or left or north or south:
                self.moving = True
            
            self.direction_facing = 0 # 0 = None 1 = left | 2 = right | 3 = north
            x =  self.agnostic_pos[0]
            y =  self.agnostic_pos[1]
        
            if left:
                self.direction_facing = 1

                if north:
                    x -= self.man_speed * self.man_diagonal_factor
                    y -= self.man_speed * self.man_diagonal_factor

                elif south:
                    x -= self.man_speed * self.man_diagonal_factor
                    y += self.man_speed * self.man_diagonal_factor

                else:
                    x -= self.man_speed

            elif right:
                self.direction_facing = 2
                
                if north:
                    x += self.man_speed * self.man_diagonal_factor
                    y -= self.man_speed * self.man_diagonal_factor

                elif south:
                    x += self.man_speed * self.man_diagonal_factor        
                    y += self.man_speed * self.man_diagonal_factor

                else:
                    x += self.man_speed
                    
            elif north:   
                self.direction_facing = 3
                y -= self.man_speed
                    
            elif south:        
                self.direction_facing = 3
                y += self.man_speed
            
            self.agnostic_pos = (x, y)


        def get_direction_facing(self):
            theta_deg = math.degrees(self.theta_rad)
            
            ## Set a constant in deg that says how close I need to be to 90 and 180 for the man to not face North
            left_right_threshold = 60

            distance_from_left = abs( 180 - abs(theta_deg) )
            distance_from_right = abs( 0 - abs(theta_deg) )

            if distance_from_left < left_right_threshold:
                return 1 # 1 = left
                
            if distance_from_right < left_right_threshold:
                return 2 # 2 = right

            return 3 # = North/South

            
    def get_goal(self):
        return self.goal                                
   

    # Used by child Classes to place the top-left corner of the rect in a way that centres the 'man' on a given coordinate 
    def offset_pos(self, coord):
        x = coord[0] - (self.sprite_size[0] / 2) 
        y = coord[1] - (self.sprite_size[1]/ 2)
        
        return (x, y)
    

    def get_centre_coord(self):
        x, y = self.agnostic_pos
        
        x += self.man_rect.width / 2
        y += self.man_rect.height / 2
        
        return (x, y)
        

    def get_id(self):
        return self.man_id


# Last line