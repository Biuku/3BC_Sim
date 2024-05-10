""" Updated April 13 
Splitting my "man" Class into Fielders and Baserunners, with a common core inherited by each

"""

import pygame
from pygame.locals import *
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0
import math

from _runningMen.man_foundation import Man



colour_white = (255, 255, 255)
colour_red = (255, 0, 0)

class Fielder(Man):

    def __init__(self, screen, pos, fielder_id):

        super().__init__(screen, pos, fielder_id) #Inheret all Mankind
        self.screen = screen
        self.goal_pos = (0,0)
        self.base_collision = 0
        #self.ball_proximity = False

    #### MAIN FUNCTIONS

    for goals in range(1):

        def assign_goal(self, goal_pos):
            self.goal_pos = self.offset_pos(goal_pos)
            self.goal = True


        # Fielder motion 
        def goal_move(self):
            self.moving = False
            
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

        
    # Detect collisions #One for fielders, one for baserunners
    def check_base_collision(self, bases):
        # Need to set collision to True if it collides with even 1 base
        
        self.collision = False
        self.rect_thickness = 1
        self.rect_colour = colour_white 
        
        for key, base in bases.items():
            if base.colliderect(self.fielder_rect):
                        
                self.collision = True
                self.rect_thickness = 4
                self.rect_colour = colour_red
                
                if key in [1, 2, 3, 4]:  # Exclude collisions with the rubber
                    self.base_collision = key


    def check_ball_proximity_2D(self, ball_coord_2D_pg, proximity_threshold_pg):
        
        fielder_centre_coord = self.get_centre_coord()
            
        distance_pg = self.helpers.measure_distance_in_pixels(fielder_centre_coord, ball_coord_2D_pg)
        
        if distance_pg < proximity_threshold_pg:
            return True


## Last line