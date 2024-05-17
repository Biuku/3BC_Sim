""" Updated April 13 
Splitting my "man" Class into Fielders and Baserunners, with a common core inherited by each

"""

import pygame
from pygame.locals import *
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0
import math

from _runningMen.man_foundation import Man
from _runningMen.man_helpers import ManHelpers

from helpers import Helpers
from setup import Setup


class Fielder(Man):

    def __init__(self, screen, pos, id):

        super().__init__(screen, pos, id, 'fielder') #Inheret all Mankind

        self.man_helpers = ManHelpers(screen, self.man_speed)

        self.screen = screen
        self.goal_coord = (0,0)
        self.base_collided_with = None

        self.ball_possession_toggle = False
        self.ball_exchange_toggle = False
        self.throw_receiver_toggle = False



    #### MAIN FUNCTIONS

    for goals in range(1):

        def assign_goal(self, goal_pos):
            self.goal_coord = self.offset_pos(goal_pos)
            self.goal = True


        # Fielder motion 
        def goal_move(self):
            self.moving = False
            
            if self.goal:
                
                self.moving = True
                
                self.man_helpers.update_movement_data(self.agnostic_pos, self.goal_coord)
                
                self.agnostic_pos, self.theta_rad = self.man_helpers.move_man_theta()
                self.direction_facing = self.get_direction_facing()
                    
                self.goal = self.man_helpers.check_end_goal_move() # Keep running till centred on the base


    # Detect collisions #One for fielders, one for baserunners
    def check_base_collision(self):

        # Need to set collision to True if it collides with even 1 base
        self.base_collided_with = self.man_helpers.detect_base_collisions(self.man_rect) # Return None if no base collision 
        self.update_for_collision_status() 


    def update_for_collision_status(self):

            self.draw_rect = True
            
            if self.throw_receiver_toggle:
                self.rect_thickness = 3
                self.rect_colour = 'blue'

            elif self.ball_exchange_toggle:
                self.rect_thickness = 3
                self.rect_colour = 'black'

            elif self.ball_possession_toggle:
                self.rect_thickness = 2
                self.rect_colour = 'grey'

            elif self.base_collided_with:    
                self.rect_thickness = 3
                self.rect_colour = 'red'
            
            ## Else, display the 'nothing special' thing
            else:
                self.draw_rect = False
                #self.rect_thickness = 1
                #self.rect_colour = 'white' 
                
                
    def update_throw_receiver(self, throw_receiver_toggle):
        self.throw_receiver_toggle = throw_receiver_toggle
        
    def update_ball_possession(self, possession, exchange):
        self.ball_possession_toggle = possession
        self.ball_exchange_toggle = exchange 


## Last line