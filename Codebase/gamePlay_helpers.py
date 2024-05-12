""" MAY 10 -- Creating this to shift some non-core code out of the bloated ball2.py module """


import pygame
from pygame.locals import *
import math

from helpers import Helpers
from setup import Setup


pygame.init()


class GameplayHelpers: 
    
    def __init__(self, screen):

        self.setup = Setup() 
        self.helpers = Helpers()
        self.screen = screen


    #### Functions ####

    def get_throw_theta(self, thrower_object, receiver_object):

        start_coord = thrower_object.get_centre_coord()
        end_coord = receiver_object.get_centre_coord()

        theta_rad = self.helpers.coord_to_theta(start_coord, end_coord)

        return math.degrees(theta_rad)


    def interpret_ball_location(self, ball_coord):
    
        ball_theta_deg = self.helpers.get_ball_theta_deg( ball_coord )

        found = False
        ball_location_text = "Foul: right side"
        
        for theta_key, field_loc in self.setup.field_direction_thetas.items():
            
            if not found and ball_theta_deg > self.setup.boundary_thetas[theta_key]: 
                ball_location_text = field_loc
                found = True  
        
        return ball_location_text
    

    def make_fielders(self, Fielder_object):

        fielder_objects = {}

        for fielder_id in [x for x in range(1, 10)]:
            coord = self.setup.fielder_standard_coord[fielder_id]                
            fielder_objects[fielder_id] = Fielder_object(self.screen, coord, fielder_id)

        return fielder_objects


    def make_baserunners(self, Baserunner_object):
        r1 = 1
        return Baserunner_object(self.screen, r1)
    
# Last time