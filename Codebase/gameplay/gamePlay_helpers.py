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


    for _init_ in range(1):

        def make_fielders(self, Fielder_object):

            fielder_objects = {}

            for fielder_id in [x for x in range(1, 10)]:
                coord = self.setup.fielder_standard_coord[fielder_id]                
                fielder_objects[fielder_id] = Fielder_object(self.screen, coord, fielder_id)

            return fielder_objects


        def make_baserunners(self, Baserunner_object):
            r1 = 1
            return Baserunner_object(self.screen, r1)

    """
    for do_game_situation in range(1): 
        
        def meta_place_ball_for_situation(self, defensive_assignments): 
            primary_fielder = defensive_assignments.index(1)
            x, y = self.setup.fielder_standard_coord[primary_fielder]
            ball_new_coord = (x - 150, y - 150)
            
            return ball_new_coord
                
            #self.ball.update_coord_for_situation(ball_new_coord)
    """ 
        
    def get_throw_theta(self, thrower_object, receiver_object):

        start_coord = thrower_object.get_centre_coord()
        end_coord = receiver_object.get_centre_coord()

        theta_rad = self.helpers.coord_to_theta(start_coord, end_coord)

        return math.degrees(theta_rad)
# Last time