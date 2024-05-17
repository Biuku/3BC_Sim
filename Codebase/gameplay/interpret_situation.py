""" MAY 13 -- Creating this to encapsulate everything that determines the baseball situation

- Ball's location and projected location
- Runners on 
- Outs

"""


import pygame
from pygame.locals import *
import math

from helpers import Helpers
from setup import Setup


pygame.init()


class InterpretSituation:
    
    def __init__(self):

        self.setup = Setup() 
        self.helpers = Helpers()
        
        self.curr_outs = 0
        self.runners_on_at_contact = {1: False, 2: False, 3: False}
        
        self.ball_depth_index = self.make_ball_depth_index()
        
        self.ball_distance = 0


    #### Functions ####
    


    def get_ball_direction(self, ball_coord):
    
        ball_theta_deg = self.helpers.get_ball_theta_deg( ball_coord )

        found = False
        ball_location_text = "Foul: right side"
        
        for theta_key, field_loc in self.setup.field_direction_thetas.items():
            
            if not found and ball_theta_deg > self.setup.boundary_thetas[theta_key]: 
                ball_location_text = field_loc
                found = True  
        
        return ball_location_text
    
    
    def update_ball_distance_feet(self, ball_coord):
        #pass
        
        ## Calculate distance in feel from Home
        start_coord = self.setup.four_B_tip
        self.ball_distance_feet = self.helpers.measure_distance_in_feet(start_coord, ball_coord)


    ## Take in the ball's distance from Home in feet, return a value from 1-6 
    def get_ball_depth(self, ball_coord):
        
        self.update_ball_distance_feet(ball_coord)
        
        ball_depth_int = 0
        keep_looking = True
        
        for radius, depth_index in self.setup.ball_depth_lookup.items():
            
            if keep_looking and self.ball_distance_feet < radius:
                ball_depth_int = depth_index
                keep_looking = False
        
        return ball_depth_int

    
    ## An index that matches the 6 ball depth zones to English descriptions
    def make_ball_depth_index(self):
        
        ball_depth_index = {
            0: "N/A",
            1: "Before mound",
            2: "Base paths",
            3: "Texas leaguer",
            4: "Mid OF",
            5: "Deep OF",
        }
        
        return ball_depth_index
    
        ## In setup
        """
        ball_depth_lookup = {
        70: 1,
        150: 2,
        200: 3,
        270: 4,
        450: 5,
        }
            
        """

# Last time