""" Updated April 13 
Splitting my "man" Class into Fielders and Baserunners, with a common core inherited by each

"""

import pygame
from pygame.locals import *
import math 
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0

from _runningMen.man_foundation import Man
from setup import Setup



colour_white = (255, 255, 255)
colour_red = (255, 0, 0)

class Baserunner(Man):

    def __init__(self, screen):
        
        self.setup = Setup()
        self.screen = screen
         
        super().__init__(screen, self.set_start_coord(), "baserunner")   # Inheret all Mankind         
          
        self.goal_pos = (0, 0)
        self.base_attained = 0
        self.score = False
        
    
    #### MAIN FUNCTIONS
        
    for goals in range(1):
        def assign_goal(self):
            self.goal = True
            
            goal_pos = self.setup.base_centroids[1]
            
            if self.base_attained == 1:
                goal_pos = self.setup.base_centroids[2]
            
            elif self.base_attained == 2:
                goal_pos = self.setup.base_centroids[3]
                
            elif self.base_attained == 3:
                goal_pos = self.setup.base_centroids[4]
            
            self.goal_pos = self.offset_pos(goal_pos)


        ## Manually remove goal during code-build
        def remove_goal(self):
            self.goal = False

            
    for move in range(1):
        
        def move_baserunner(self):  #left, right, north, south
              
            if self.goal:
                
                self.moving = True
                
                ## 1. Get theta of journey
                self.theta_rad = self.helpers.coord_to_theta(self.agnostic_pos, self.goal_pos)

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
                    
                self.direction_facing = self.get_direction_facing()

            #else: 
            #    self.move_man(left, right, north, south)

            
    for attain_base in range(1):
                        
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
        
            ## To do -- detect collisions with fielders

        
        def update_base_attained(self, base_collision):
            
            ## Cannot attain a base unless you've obtained all previous bases
            # base_collision will contain one of: one_B, two_B, three_B
            
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


    for other_stuff in range(1):         
        
        def score_run(self):
            print("Woopie doo. You got a run") 
            
        def set_start_coord(self):
            home = self.setup.base_centroids[4]
            x = home[0] - 32
            y = home[1] - 10
            
            return (x, y)      