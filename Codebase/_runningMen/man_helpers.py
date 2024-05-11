""" Updated April 13 -- added Rect's and collision detection with bases """

import pygame
from pygame.locals import *
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0
import math

from helpers import Helpers
from setup import Setup


class ManHelpers: 

    def __init__(self, screen, speed):

        self.helpers = Helpers()
        self.screen = screen
        self.setup = Setup()
        
        self.curr_coord = None
        self.goal_coord = None
        self.man_speed = speed


    #### MAIN FUNCTIONS ####

    def move_man_theta(self):
        
        theta_rad = self.helpers.coord_to_theta(self.curr_coord, self.goal_coord)
        x, y = self.curr_coord
        
        x += self.man_speed * math.cos(theta_rad)
        y -= self.man_speed * math.sin(theta_rad)  
        
        return (x, y), theta_rad


    def check_end_goal_move(self):

        goal = True
        proximity_to_goal = self.helpers.measure_distance_in_pixels(self.curr_coord, self.goal_coord)
        
        if proximity_to_goal < 2:
            goal = False
        
        return goal
    
    
    def detect_base_collisions(self, man_rect):
                
        for base_ID, base_rect in self.setup.base_rects.items():
                
            if base_rect.colliderect(man_rect):
                return base_ID
        
        return None # No base collided with 

    
    def update_movement_data(self, curr, goal):
        self.curr_coord = curr
        self.goal_coord = goal


# Last line