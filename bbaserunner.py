""" Updated April 13 
Splitting my "man" Class into Fielders and Baserunners, with a common core inherited by each

"""

import pygame
from pygame.locals import *
import math 

from man_foundation import Man
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0
from helpers import Helpers

colour_white = (255, 255, 255)
colour_red = (255, 0, 0)

class Baserunner(Man):

    def __init__(self, screen, base_centroids):
        
        ## Super requires these two 
        self.base_centroids = base_centroids    # dict -- keys = one_B, two_B, three_B, four_B, rubber_P
        start_pos = self.set_start_pos(base_centroids)
         
        super().__init__(screen, start_pos, "baserunner")   # Inheret all Mankind         
          
        self.screen = screen
        self.base_centroids = base_centroids
        self.helper = Helpers(screen)


        self.goal_pos = (0, 0)
        self.base_attained = 0
        self.score = False
        
        self.font20 = pygame.font.SysFont('Arial', 18) 
    
    def set_start_pos(self, base_centroids):
        home = base_centroids['four_B']
        x = home[0] - 32
        y = home[1] - 10
        
        return (x, y)      
        
   
    def assign_goal(self):
        self.goal = True
        
        goal_pos = self.base_centroids['one_B']
        
        if self.base_attained == 1:
            goal_pos = self.base_centroids['two_B']
        
        elif self.base_attained == 2:
            goal_pos = self.base_centroids['three_B']
            
        elif self.base_attained == 3:
            goal_pos = self.base_centroids['four_B']
        
        self.goal_pos = self.offset_pos(goal_pos)

    ## Manually remove goal during code-build
    def remove_goal(self):
        self.goal = False
        

    def move_baserunner(self, left, right, north, south):  
              
        if self.goal:
            
            self.moving = True
            
            ## 1. Get theta of journey
            self.theta_rad = self.helper.coord_to_theta(self.agnostic_pos, self.goal_pos)

            ## 3. Move baserunner in direction theta at speed, new_speed
            x, y = self.agnostic_pos
            x += self.man_speed_x * math.cos(self.theta_rad)
            y -= self.man_speed_y * math.sin(self.theta_rad)  ## Do I need another speed for y??
            self.agnostic_pos = (x, y)
            
            # Turn off goal seeking when they reach the goal
            x_journey = self.goal_pos[0] - self.agnostic_pos[0]
            y_journey = self.goal_pos[1] - self.agnostic_pos[1]
            
            if abs(x_journey) <= 2 and abs(y_journey) <= 2:
                self.goal = False
                #print("Goal cancelled for baserunner: ")
                
            self.direction_facing = self.get_direction_facing()

        else: 
            self.move_man(left, right, north, south)


    ## I DON'T NEED THIS FUNC -- TRIG AUTOMATICALLY HANDLES THE DIAGONAL SPEED PROBLEM
    """
    def get_scaled_speed(self, rad):
        deg = math.degrees(rad)
        diagonal_factor_complement = 1 - self.man_diagonal_factor
        
        multiple_of_90 = deg//90
        deg -= 90 * multiple_of_90
        
        ## Get value to scale the diagonal factor by
        inverse_distance_from_45 = 45 - abs(deg-45)
        percent_of_diagonal = inverse_distance_from_45/45
        
        ## Scale the diagonal factor
        scaled_diagonal_factor = diagonal_factor_complement * percent_of_diagonal
        
        ## Scale the speed -- reduce it by the diagonal factor
        scaled_speed = self.man_speed_x * (1 - scaled_diagonal_factor)
        
        return scaled_speed
    """
            
    # Detect collisions #One for fielders, one for baserunners
    def detect_collisions(self, bases, fielders):
        
        self.collision = False
        self.rect_thickness = 1
        self.rect_colour = colour_white 
        
        for key, base in bases.items():
            
            if base.colliderect(self.baserunner_rect):
                    
                self.collision = True
                self.rect_thickness = 4
                self.rect_colour = colour_red
                
                if key in ['one_B', 'two_B', 'three_B', 'four_B']:  # Exclude collisions with the rubber
                    self.update_base_attained(key)
                
                #print("Colliding with: ", key)
    
            else:
                pass

          
        ## To do -- detect collisions with fielders
                    
        #self.display_baserunner_status()
    
    def update_base_attained(self, base_collision):
        
        ## Cannot attain a base unless you've obtained all previous bases
        # base_collision will contain one of: one_B, two_B, three_B
        # For now, ignoring a runner who attains 2B or 3B, then reverts back a base
        
        ## No prerequisite to attain 1B
        if base_collision == 'one_B':
           self.base_attained = 1
        
        elif self.base_attained >= 1:
                
            if base_collision == 'two_B':
                self.base_attained = 2
        
            elif self.base_attained >= 2:      
                
                if base_collision == 'three_B':
                    self.base_attained = 3
                    
                if self.base_attained == 3:
                    if base_collision == 'four_B':
                        self.score_run()
        
    ## Called by GamePlay
    def get_base_attained(self):
        return self.base_attained
         
    def score_run(self):
        print("Woopie doo. You got a run") 
        
        