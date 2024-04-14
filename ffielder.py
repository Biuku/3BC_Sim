""" Updated April 13 
Splitting my "man" Class into Fielders and Baserunners, with a common core inherited by each

"""

import pygame
from pygame.locals import *
from man_foundation import Man
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0

colour_white = (255, 255, 255)
colour_red = (255, 0, 0)

class Fielder(Man):

    def __init__(self, screen, pos, fielder_id):

        super().__init__(screen, pos, "fielder") #Inheret all Mankind
        self.screen = screen

        self.fielder_id = fielder_id
        self.goal_pos = (0,0)

    # Fielder objective
    def assign_goal(self, goal_pos):
        self.goal_pos = self.offset_pos(goal_pos)
        self.goal = True
        
    # Fielder motion 
    def goal_move(self):
        self.moving = False
        
        if self.goal:
            
            x_journey = self.goal_pos[0] - self.agnostic_pos[0] #self.fielder_rect.x
            y_journey = self.goal_pos[1] - self.agnostic_pos[1] #self.fielder_rect.y
            
            right = left = south = north = False
            
            if x_journey > 0:
                right = True
            
            elif x_journey < 0:
                left = True
            
            if y_journey < 0:
                north = True
                
            elif y_journey > 0: 
                south = True
            
            ## Only advance the animatio when moving 
            if right or left or north or south:
                self.moving = True
                    
            # Cheat -- use the kb_move func to move the guy 
            self.move_man( left, right, north, south)
            
            # Turn off goal seeking when they reach the goal
            if abs(x_journey) <= 2 and abs(y_journey) <= 2:
                self.goal = False
                #print("Goal cancelled for: ", self.fielder_id)
       
    # Detect collisions #One for fielders, one for baserunners
    def detect_collisions(self, bases):
        # Need to set collision to True if it collides with even 1 base
        
        self.collision = False
        
        for base in bases.values():
            if base.colliderect(self.fielder_rect):
                self.collision = True
                self.rect_thickness = 4
                self.rect_colour = colour_red
        
            else:
                self.rect_thickness = 1
                self.rect_colour = colour_white 
                    
