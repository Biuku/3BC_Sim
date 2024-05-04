import pygame
from pygame.locals import *
import math
import random
from helpers_angryBats import Helpers
from setup_angryBats import Setup


pygame.init()


class Shadow:
    
    def __init__(self, screen, w, h, radius):
        for _ in range(1):
            self.screen = screen

            self.setup = Setup(self.screen, w, h)
            self.helpers = Helpers(self.screen)

            ## Constants
            self.thickness = 3
            self.y = self.setup.top_of_floor + self.thickness/2
            
            self.min_width = int(radius * 1.6) ## Extra width so the shadow doesn't become miniscule
            self.max_width = 200 ## Just guessed
            self.max_possible_height_feet = 200 ## 80 mph exit velo with 90 degree launch angle = 215' max height  

            # Colours
            self.zero_shadow_rgb = self.setup.green_grass_c  #[65, 150, 10]
            self.curr_rgb = tuple(self.zero_shadow_rgb)
            self.max_darkness_lowerbound_c = 0.10 # When very high up, stay 15% darker than the colour of grass
            self.washout_upperbound_c = 0.9 # When on the ground, stay 20% away from total black when on the ground

            #### Shadow coord and size ####
            ## Higher order var 
            self.master_ball_height_pct = 0
            self.width = self.min_width

            ## Concrete var
            self.master_x = 200
            self.line_start_x = self.master_x - self.width
            self.line_end_x = self.master_x + self.width

            ## CALCULATED SHADOW VARIABLES

    def update_shadow(self, height_feet, x_coord): 

        
        ## Set the general var
        self.master_ball_height_pct = min(height_feet / self.max_possible_height_feet, 1) ## Don't exceed 100%
        
        self.master_x = x_coord
        
        self.update_width()
        self.update_coord()
        self.update_colour()

        self.draw_shadow()


    def update_width(self):
        width = self.max_width * self.master_ball_height_pct
        self.width = max(self.min_width, width)


    def update_coord(self):
        self.line_start_x = self.master_x - self.width / 2 
        self.line_end_x = self.master_x + self.width / 2        


    def update_colour(self):
        ## Higher % = very washed out 
        colour_update_factor = self.master_ball_height_pct
        colour_update_factor *= 3 ## Juice it so the colour is more washed out for each % of height
        
        ## Set guardrails so it doesn't wash out or become too dark 
        colour_update_factor = max(self.max_darkness_lowerbound_c, colour_update_factor)
        colour_update_factor = min(self.washout_upperbound_c, colour_update_factor) 
        
        ## adjust rgb
        curr_rgb = [ int(x * colour_update_factor) for x in self.zero_shadow_rgb  ]
        self.curr_rgb = tuple(curr_rgb)

    
    def draw_shadow(self):
        pygame.draw.line(self.screen, self.curr_rgb, (self.line_start_x, self.y), (self.line_end_x, self.y), self.thickness)
    
