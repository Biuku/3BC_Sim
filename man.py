""" Updated April 13 -- added Rect's and collision detection with bases """

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

#from pygame.sprite import Sprite
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0


colour_white = (255, 255, 255)
colour_red = (255, 0, 0)

class Man(): #Sprite

    def __init__(self, screen, pos, fielder_id, team):

        #super().__init__()
        self.screen = screen

        self.team = team  # "baserunner" or "fielder"
        self.fielder_id = fielder_id
        self.goal = False
        self.goal_pos = (0,0)
        self.collision = False
        
        ### ANIMATION -- set up of frames
        ## Load the baserunner animation frames -- team Red
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
        
        ## Load the fielder animation frames -- team Blue
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
  
        # Organize frames in lists -- use 'itertools > cycle' to streamline code to loop from the end of the list to the beginning 
        if self.team == "baserunner":
            self.man_frames_L = cycle([self.man_L1, self.man_L1, self.man_L2, self.man_L2, self.man_L3, self.man_L3]) # Doubling up frames to better match animation to locomotion without reducing fps to ridiculous level
            self.man_frames_R = cycle([self.man_R1, self.man_R1, self.man_R2, self.man_R2, self.man_R3, self.man_R3])
            self.man_frames_N = cycle([self.man_N1, self.man_N1, self.man_N2, self.man_N2, self.man_N3, self.man_N3, self.man_N4, self.man_N4])        
            
        else:
            self.man_frames_L = cycle([self.fielder_L1, self.fielder_L1, self.fielder_L2, self.fielder_L2, self.fielder_L3, self.fielder_L3]) # Doubling up frames to better match animation to locomotion without reducing fps to ridiculous level
            self.man_frames_R = cycle([self.fielder_R1, self.fielder_R1, self.fielder_R2, self.fielder_R2, self.fielder_R3, self.fielder_R3])
            self.man_frames_N = cycle([self.fielder_N1, self.fielder_N1, self.fielder_N2, self.fielder_N2, self.fielder_N3, self.fielder_N3, self.fielder_N4, self.fielder_N4])
    
    
        # Start frame and rect for collision detection
        self.man_curr_frame = next(self.man_frames_L)
        self.rect = self.man_curr_frame.get_rect()
        self.rect.topleft = self.offset_pos(pos)
        self.rect_colour = colour_white
        self.rect_thickness = 1


        ### LOCOMOTION -- set up, including start position and speed of locomotion  
        self.man_speed_x = 4/3 # Speed of lateral locomotion -- pixels of movement per frame
        self.man_speed_y = 4/3
        self.man_diagonal_factor = 0.744 ## Diagonal motion is 1.35x faster than North-South or lateral motion -- this should equalize that.


    # Fielder objective
    def assign_goal(self, goal_pos):
        self.goal_pos = self.offset_pos(goal_pos)
        self.goal = True
        
    # Fielder motion 
    def goal_move(self):
        if self.goal:
            
            x_journey = self.goal_pos[0] - self.rect.x
            y_journey = self.goal_pos[1] - self.rect.y
            
            right = left = south = north = False
            
            if x_journey > 0:
                right = True
            
            elif x_journey < 0:
                left = True
            
            if y_journey < 0:
                north = True
                
            elif y_journey > 0: 
                south = True
            
                        
            # Cheat -- use the kb_move func to move the guy 
            self.kb_move( left, right, north, south)
            
            # Turn off goal seeking when they reach the goal
            if abs(x_journey) <= 2 and abs(y_journey) <= 2:
                self.goal = False
                print("Goal cancelled for: ", self.fielder_id)
            
        
    # Manual movement from keyboad (Fielder or Baserunner)
    def kb_move(self, left, right, north, south):
        if left:
            self.man_curr_frame = next(self.man_frames_L)

            if north:
                self.rect.y -= self.man_speed_y * self.man_diagonal_factor
                self.rect.x -= self.man_speed_x * self.man_diagonal_factor

            elif south:
                self.rect.y += self.man_speed_y * self.man_diagonal_factor
                self.rect.x -= self.man_speed_x * self.man_diagonal_factor
            
            else:
                self.rect.x -= self.man_speed_x

        elif right:
            self.man_curr_frame = next(self.man_frames_R)
            
            if north:
                self.rect.y -= self.man_speed_y * self.man_diagonal_factor
                self.rect.x += self.man_speed_x * self.man_diagonal_factor
            
            elif south:
                self.rect.y += self.man_speed_y * self.man_diagonal_factor
                self.rect.x += self.man_speed_x * self.man_diagonal_factor
        
            else:
                self.rect.x += self.man_speed_x
                
        elif north:   
            self.man_curr_frame = next(self.man_frames_N)
            self.rect.y -= self.man_speed_y
                
        elif south:        
            self.man_curr_frame = next(self.man_frames_N)
            self.rect.y += self.man_speed_y
        
    # Detect collisions #One for fielders, one for baserunners
    def detect_collisions(self, bases):
        # Need to set collision to True if it collides with even 1 base
        
        self.collision = False
        
        for base in bases:
            if base.colliderect(self.rect):
                self.collision = True
                 
    # Draw self -- common to fielders and baserunners
    def draw(self):
        self.screen.blit(self.man_curr_frame, self.rect)
        
        if self.collision:
            self.rect_thickness = 4
            self.rect_colour = colour_red
        
        else:
            self.rect_thickness = 1
            self.rect_colour = colour_white    
        
        pygame.draw.rect(self.screen, self.rect_colour, self.rect, self.rect_thickness)
                                  

    ## Takes in (x, y) and moves up-left by half the sprite's size to centre it on the desired coordinate
    # Common to fielders and baserunners
    def offset_pos(self, pos):
        
        x = pos[0] - (self.rect.width / 2)
        y = pos[1] - (self.rect.height / 2)
        
        return (x, y)
                
        


