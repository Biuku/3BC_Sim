import pygame
from pygame.locals import *
import math
import random

from setup import Setup


pygame.init()


class Shadow:
    
    def __init__(self, screen, radius):
        self.master_y = 0
        self.master_x = 0
        
        for _ in range(1):
            self.setup = Setup()
            
            self.screen = screen

            ## Constants
            self.thickness = 3
            self.ball_radius = radius
            self.min_width = int(radius * 1.2) ## Extra width so the shadow doesn't become miniscule
            self.max_width = 40 ## Just guessed
            self.max_possible_height_feet = 100 ## 80 mph exit velo with 90 degree launch angle = 215' max height  

            # Colours
            self.zero_shadow_rgb = self.setup.green_grass_c  #[65, 150, 10]
            self.curr_rgb = tuple(self.zero_shadow_rgb)

            #### Shadow coord and size ####
            ## Higher order var 
            self.master_ball_height_pct = 0
            self.width = self.min_width

            ## Concrete var
            self.line_start_x = self.master_x - self.width
            self.line_end_x = self.master_x + self.width

            ## CALCULATED SHADOW VARIABLES
            


    def update_shadow(self, ball_height_feet, ball_xy_coord): 

        ## Set the general var
        self.master_ball_height_pct = min(ball_height_feet / self.max_possible_height_feet, 1) ## Don't exceed 100%
        
        self.master_x = ball_xy_coord[0]
        self.update_y(ball_height_feet, ball_xy_coord[1])
        
        self.update_width()
        self.update_coord()
        self.update_colour()

        self.draw_shadow()
        
    
    def update_y(self, ball_height_feet, ball_y_coord_pg):
        
        ## When height is close to zero, dy should be close to zero
        ## When height is close to 150, dy would be at its max... 
        ## Maybe I just move the ball South by the # of feet high... so it's automatically 1/3 of teh # of pixels
        ball_radius_offset = self.ball_radius + 1
        self.master_y = ball_y_coord_pg + ball_radius_offset + ball_height_feet
    
    
    def update_width(self):
        width = self.max_width * self.master_ball_height_pct
        self.width = max(self.min_width, width)


    def update_coord(self):
        self.line_start_x = self.master_x - self.width / 2 
        self.line_end_x = self.master_x + self.width / 2        


    def update_colour(self):
        ## Higher % = very washed out 
        colour_update_factor = self.master_ball_height_pct
        #colour_update_factor *= 3 ## Juice it so the colour is more washed out for each % of height
        
        ## Set guardrails so it doesn't wash out or become too dark 
        #colour_update_factor = 0.90 # Just perceptible
        
        lowerbound =  0.6
        upperbound = 0.9
        
        colour_update_factor = max(lowerbound, colour_update_factor)
        colour_update_factor = min(upperbound, colour_update_factor) 
        
        
        ## adjust rgb
        curr_rgb = [ int(x * colour_update_factor) for x in self.zero_shadow_rgb  ]
        self.curr_rgb = tuple(curr_rgb)

    
    def draw_shadow(self):
        pygame.draw.line(self.screen, self.curr_rgb, (self.line_start_x, self.master_y), (self.line_end_x, self.master_y), self.thickness)
    
