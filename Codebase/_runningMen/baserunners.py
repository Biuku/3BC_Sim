""" Updated April 13 
Splitting my "man" Class into Fielders and Baserunners, with a common core inherited by each

"""

import pygame
from pygame.locals import *
import math 
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0

from _runningMen.man_foundation import Man
from _runningMen.man_helpers import ManHelpers

from helpers import Helpers
from setup import Setup


class Baserunner(Man):

    def __init__(self, screen, id):
        
        self.setup = Setup()
        self.helpers = Helpers()
        self.screen = screen
        
         
        super().__init__(screen, self.set_start_coord(), id, 'baserunner')   # Inheret all Mankind         
          
        self.man_helpers = ManHelpers(screen, self.man_speed)
        
        self.goal_coord = (0, 0)
        self.base_collided_with = None
        self.base_attained = 0 ## If the baserunner somehow touches 2B from Home, they do collide with it, they do not attain it

    
    #### MAIN FUNCTIONS
        
    for goals in range(1):
        
        def assign_goal(self):

            self.goal = True            
            goal_base = self.base_attained + 1
            goal_coord = self.setup.base_centroids[goal_base]
            
            self.goal_coord = self.offset_pos(goal_coord)

            
    for move in range(1):
        
        def move_baserunner(self):  #left, right, north, south
            
            self.moving = False
            
            if self.goal:
                
                self.moving = True
                
                self.man_helpers.update_movement_data(self.agnostic_pos, self.goal_coord)
  
                self.agnostic_pos, self.theta_rad = self.man_helpers.move_man_theta()
                self.direction_facing = self.get_direction_facing()
                    
                self.goal = self.man_helpers.check_end_goal_move() # Keep running till centred on the base, regardless of being safe
                

            #else: 
            #    self.move_man(left, right, north, south)
        

            
    for attain_base in range(1):

        # Detect collisions #One for fielders, one for baserunnersgoal_coord
        def detect_collisions(self, fielder_objects):
            
            self.base_collided_with = self.man_helpers.detect_base_collisions(self.man_rect) # Return None if no base collision 
            self.update_for_collision_status() 


        def update_for_collision_status(self):

            if self.base_collided_with:    
                self.rect_thickness = 4
                self.rect_colour = 'red' #colour_red
                self.update_base_attained()
                
            else:
                self.rect_thickness = 1
                self.rect_colour = 'white' #colour_white 
            
            
        ## Only called on collision with a base
        def update_base_attained(self):
            
            ## Cannot attain a base unless you've obtained all preceding bases
            base_attained = False
            
            if self.base_collided_with == 1:
                base_attained = 1
            
            if self.base_collided_with == 2 and self.base_attained == 1:
                base_attained = 2
            
            if self.base_collided_with == 3 and self.base_attained == 2:
                base_attained = 3
                
            if self.base_collided_with == 4 and self.base_attained == 3:
                print("Woopie doo. You got a run") 
            
            if base_attained:
                self.base_attained = base_attained

    
    ## Called by GamePlay
    def get_base_attained(self):
        return self.base_attained


    for other_stuff in range(1):         
  
        def set_start_coord(self):
            
            home = self.setup.base_centroids[4]

            x = home[0] - 32
            y = home[1] - 10
            
            return (x, y)      