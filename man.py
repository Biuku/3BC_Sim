""" April 7, 2024 -- Refactoring my single instance of a 'man' (able to run/move) into an object """

import pygame
from pygame.locals import *

#from pygame.sprite import Sprite
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0

class Man():   #(Sprite)

    def __init__(self, screen, x, y, team):

        self.screen = screen
        self.team = team # "baserunner" or "fielder"
        self.man_x = x # start position
        self.man_y = y # start position
        
        ### ANIMATION -- set up of frames
        ## Load the baserunner frames -- team Red
        # Load the frames for leftward, rightward and North/South running animation 
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

        # Organize frames in lists -- use 'itertools > cycle' to streamline code to loop from the end of the list to the beginning 
        



        ## Load the fielder frames -- team Blue
        # Load the frames for leftward, rightward and North/South running animation 
        self.fielder_L1 = pygame.image.load("images/fielders/man_fielder_left_1.png")  
        self.fielder_L2 = pygame.image.load("images/fielders/man_fielder_left_2.png") 
        self.fielder_L3 = pygame.image.load("images/fielders/man_fielder_left_3.png") 

        self.fielder_R1 = pygame.image.load("images/fielders/man_fielder_right_1.png")
        self.fielder_R2 = pygame.image.load("images/fielders/man_fielder_right_2.png") 
        self.fielder_R3 = pygame.image.load("images/fielders/man_fielder_right_3.png")

        self.fielder_N1 = pygame.image.load("images/fielders/man_fielder_north_1.png")
        self.fielder_N2 = pygame.image.load("images/fielders/man_fielder_north_2.png")
        self.fielder_N3 = pygame.image.load("images/fielders/man_fielder_north_3.png")
        self.fielder_N4 = pygame.image.load("images/fielders/man_fielder_north_4.png")

  
        # Organize frames in lists -- use 'itertools > cycle' to streamline code to loop from the end of the list to the beginning 
        if self.team == "baserunner":

            self.man_frames_L = cycle([self.man_L1, self.man_L1, self.man_L2, self.man_L2, self.man_L3, self.man_L3]) # Doubling up frames to better match animation to locomotion without reducing fps to ridiculous level
            self.man_frames_R = cycle([self.man_R1, self.man_R1, self.man_R2, self.man_R2, self.man_R3, self.man_R3])
            self.man_frames_N = cycle([self.man_N1, self.man_N1, self.man_N2, self.man_N2, self.man_N3, self.man_N3, self.man_N4, self.man_N4])        
            
        else:
            self.man_frames_L = cycle([self.fielder_L1, self.fielder_L1, self.fielder_L2, self.fielder_L2, self.fielder_L3, self.fielder_L3]) # Doubling up frames to better match animation to locomotion without reducing fps to ridiculous level
            self.man_frames_R = cycle([self.fielder_R1, self.fielder_R1, self.fielder_R2, self.fielder_R2, self.fielder_R3, self.fielder_R3])
            self.man_frames_N = cycle([self.fielder_N1, self.fielder_N1, self.fielder_N2, self.fielder_N2, self.fielder_N3, self.fielder_N3, self.fielder_N4, self.fielder_N4])

        
        # Start frame
        self.man_curr_frame = next(self.man_frames_L)

        ### LOCOMOTION -- set up, including start position and speed of locomotion  
        self.man_speed_x = 4/3 # Speed of lateral locomotion -- pixels of movement per frame
        self.man_speed_y = 4/3
        self.man_diagonal_factor = 0.744 ## Diagonal motion is 1.35x faster than North-South or lateral motion. No idea why, but this should equalize that.

    def move(self, left, right, north, south):
        if left:
            self.man_curr_frame = next(self.man_frames_L)

            if north:
                self.man_y -= self.man_speed_y * self.man_diagonal_factor
                self.man_x -= self.man_speed_x * self.man_diagonal_factor

            elif south:
                self.man_y += self.man_speed_y * self.man_diagonal_factor
                self.man_x -= self.man_speed_x * self.man_diagonal_factor
            
            else:
                self.man_x -= self.man_speed_x

        elif right:
            self.man_curr_frame = next(self.man_frames_R)
            
            if north:
                self.man_y -= self.man_speed_y * self.man_diagonal_factor
                self.man_x += self.man_speed_x * self.man_diagonal_factor
            
            elif south:
                self.man_y += self.man_speed_y * self.man_diagonal_factor
                self.man_x += self.man_speed_x * self.man_diagonal_factor
        
            else:
                self.man_x += self.man_speed_x
                
        elif north:   
            self.man_curr_frame = next(self.man_frames_N)
            self.man_y -= self.man_speed_y
                
        elif south:        
            self.man_curr_frame = next(self.man_frames_N)
            self.man_y += self.man_speed_y   

        #### Draw sprites    
        self.screen.blit(self.man_curr_frame, (int(self.man_x), int(self.man_y)))
            
