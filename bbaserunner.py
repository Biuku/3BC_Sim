""" Updated April 13 
Splitting my "man" Class into Fielders and Baserunners, with a common core inherited by each

"""

import pygame
from pygame.locals import *
from man_foundation import Man
from itertools import cycle ## lets you cycle through a list [10, 11, 12] so upon 12 it returns to index 0

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
        
        #goal_pos = [goal_pos[0], goal_pos[1]] # Reformat to be modifiable
        
        self.goal_pos = self.offset_pos(goal_pos)
        
        

    def goal_move(self):
        self.moving = False
        
        if self.goal:
 
            x_journey = self.goal_pos[0] - self.agnostic_pos[0]
            y_journey = self.goal_pos[1] - self.agnostic_pos[1]
            
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
                print("Goal cancelled for baserunner: ")
 
            
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
                    
        self.display_baserunner_status()
    
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
        
    def display_baserunner_status(self):
        
        ### Meta -- display the latest base attained
        text = "No bases attained"
        pos = (1400, 900)
        
        if self.base_attained > 0:
            text = "Highest base attained: " + str(self.base_attained) + "B" 
        
        text_base_attained = self.font20.render(text, True, 'black')  # Text, antialiasing, color
        text_base_attained_rect = text_base_attained.get_rect()
        text_base_attained_rect.topleft = pos
        
        self.screen.blit(text_base_attained, text_base_attained_rect)       
        
    def score_run(self):
        print("Woopie doo. You got a run") 
        
        