""" Updated April 13 -- added Rect's and collision detection with bases """

import pygame
from pygame.locals import *
from helpers import Helpers

from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0


class Man: 

    def __init__(self, screen, pos, man_id):

        self.screen = screen
        self.man_id = man_id
        self.helper = Helpers(self.screen)
        
        #### ANIMATION -- set up of frames ####
        
        ### Load the animation frames 
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
        self.baserunner_frames_L = cycle([self.man_L1, self.man_L1, self.man_L2, self.man_L2, self.man_L3, self.man_L3]) # Doubling up frames to better match animation to locomotion without reducing fps to ridiculous level
        self.baserunner_frames_R = cycle([self.man_R1, self.man_R1, self.man_R2, self.man_R2, self.man_R3, self.man_R3])
        self.baserunner_frames_N = cycle([self.man_N1, self.man_N1, self.man_N2, self.man_N2, self.man_N3, self.man_N3, self.man_N4, self.man_N4])
        
        # Fielder
        self.fielder_frames_L = cycle([self.fielder_L1, self.fielder_L1, self.fielder_L2, self.fielder_L2, self.fielder_L3, self.fielder_L3]) # Doubling up frames to better match animation to locomotion without reducing fps to ridiculous level
        self.fielder_frames_R = cycle([self.fielder_R1, self.fielder_R1, self.fielder_R2, self.fielder_R2, self.fielder_R3, self.fielder_R3])
        self.fielder_frames_N = cycle([self.fielder_N1, self.fielder_N1, self.fielder_N2, self.fielder_N2, self.fielder_N3, self.fielder_N3, self.fielder_N4, self.fielder_N4])
        
        ### Create first frame and rects  
        # Baserunner
        self.baserunner_curr_frame = next(self.baserunner_frames_L)
        self.baserunner_rect = self.baserunner_curr_frame.get_rect()
        
        # Fielder
        self.fielder_curr_frame = next(self.fielder_frames_L)
        self.fielder_rect = self.fielder_curr_frame.get_rect()
        
        
        #### MOTION AND POSITION  ####
        
        ### LOCOMOTION -- set up, including start position and speed of locomotion  
        # TEMPORARILY INCREAING RUNNING SPEED TO MAKE TESTING FASTER/EASIER
        self.man_speed_x = 2 #4/3 # Optimal speed of NSEW locomotion = 4/3 -- pixels of movement per frame
        self.man_speed_y = 2 #4/3
        self.man_diagonal_factor = 0.744 ## Diagonal motion is 1.35x faster than North-South or lateral motion -- this should equalize that.
        self.collision = False
        self.direction_facing = 0 # 0 = None 1 = left | 2 = right | 3 = north
        
        ### Agnostic position
        self.sprite_size = [self.fielder_rect.width, self.fielder_rect.height]
        self.agnostic_pos = self.get_start_agnostic_pos(pos)
        
        ### Agnostic goal toggle 
        self.goal = False
        self.moving = False
        
        ### Non-agnostic attributes
        # Baserunner-specific attributes
        self.baserunner_rect.topleft = self.agnostic_pos
        
        #Fielder
        self.fielder_rect.topleft = self.agnostic_pos

        ### Meta attributes -- colours for boxes used during development
        self.rect_colour = 'white' 
        self.rect_thickness = 1
 
    
    def move_man(self, left, right, north, south):
        ## Only advance the animatio when moving 
        self.moving = False
        if right or left or north or south:
            self.moving = True
        
        self.direction_facing = 0 # 0 = None 1 = left | 2 = right | 3 = north
        x =  self.agnostic_pos[0]
        y =  self.agnostic_pos[1]
    
        if left:
            self.direction_facing = 1

            if north:
                x -= self.man_speed_y * self.man_diagonal_factor
                y -= self.man_speed_x * self.man_diagonal_factor

            elif south:
                x -= self.man_speed_x * self.man_diagonal_factor
                y += self.man_speed_y * self.man_diagonal_factor

            else:
                x -= self.man_speed_x

        elif right:
            self.direction_facing = 2
            
            if north:
                x += self.man_speed_x * self.man_diagonal_factor
                y -= self.man_speed_y * self.man_diagonal_factor

            elif south:
                x += self.man_speed_x * self.man_diagonal_factor        
                y += self.man_speed_y * self.man_diagonal_factor

            else:
                x += self.man_speed_x
                
        elif north:   
            self.direction_facing = 3
            y -= self.man_speed_y
                
        elif south:        
            self.direction_facing = 3
            y += self.man_speed_y
        
        self.agnostic_pos = (x, y)
    

    def draw_fielder(self):
        self.fielder_rect.x = self.agnostic_pos[0]
        self.fielder_rect.y = self.agnostic_pos[1]
        
        if self.moving:
        
            if self.direction_facing == 1:
                self.fielder_curr_frame = next(self.fielder_frames_L)

            elif self.direction_facing == 2:
                self.fielder_curr_frame = next(self.fielder_frames_R)
            
            elif self.direction_facing == 3:
                self.fielder_curr_frame = next(self.fielder_frames_N)
                
        self.screen.blit(self.fielder_curr_frame, self.fielder_rect)
        pygame.draw.rect(self.screen, self.rect_colour, self.fielder_rect, self.rect_thickness)
        
        ## Write fielder ID on fielder
        font = pygame.font.SysFont('Arial', 12)
        x = self.fielder_rect.x + 16
        y = self.fielder_rect.y + 42
        
        text = "F" + str(self.man_id)
        
        #self.draw_text(text, 'black', (x, y), font, 2)
        self.helper.draw_text(text, 'black', (x, y), font, 2)
            
      
    def draw_baserunner(self):
        self.baserunner_rect.x = self.agnostic_pos[0]
        self.baserunner_rect.y = self.agnostic_pos[1]
        
        if self.moving:
        
            if self.direction_facing == 1:
                self.baserunner_curr_frame = next(self.baserunner_frames_L)

            elif self.direction_facing == 2:
                self.baserunner_curr_frame = next(self.baserunner_frames_R)
            
            elif self.direction_facing == 3:
                self.baserunner_curr_frame = next(self.baserunner_frames_N)
            
            else:
                self.baserunner_curr_frame = next(self.baserunner_frames_L)

        self.screen.blit(self.baserunner_curr_frame, self.baserunner_rect)
        pygame.draw.rect(self.screen, self.rect_colour, self.baserunner_rect, self.rect_thickness)

        
    def get_goal(self):
        return self.goal                                
   
    
    # Used by child Classes
    def offset_pos(self, pos):
        x = pos[0] - (self.sprite_size[0] / 2) 
        y = pos[1] - (self.sprite_size[1]/ 2)
        
        return (x, y)

    
    def get_start_agnostic_pos(self, pos):
        w = self.sprite_size[0]
        h = self.sprite_size[1]
        
        x = pos[0] - w/2
        y = pos[1] - h/2
        
        return (x, y)
   
