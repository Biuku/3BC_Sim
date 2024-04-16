""" Created: April 16 

Shifting a few common functions here

"""

import pygame
from pygame.locals import *
import math
import numpy as np

pygame.init()


class Helpers: 
    
    def __init__(self, screen):
        self.screen = screen
        self.pixels_per_foot = ( (355/127) + (362/127) ) / 2
        self.pixels_per_step = self.pixels_per_foot * 2.5
    
    def draw_text(self, string_, colour, coord, font, justification):
        
        text = font.render(string_, True, colour)
        text_rect = text.get_rect()
    # 
        text_rect.topleft = coord
    
        if justification == 2: 
            text_rect.center = coord
            
        self.screen.blit(text, text_rect)
        
        
    ## Utility function to convert a line between two points into a distance in feet
    def measure_distance_in_feet(self, start_pos, end_pos):
    
        ## First, what is the conversion factor? Average the pixels between 1B/3B and 2B/4B 
        pixels_to_feet = ( (355/127) + (362/127) ) / 2
        
        ## Next, convert two sets of coordinates to a linear distance using trigonometry
        distance_in_pixels = math.sqrt( ( end_pos[0] - start_pos[0] )**2  +  ( end_pos[1] - start_pos[1] )**2 )
        
        return distance_in_pixels / pixels_to_feet 
    
    ## Do trionometry to convert 'steps over' and 'steps back' in baseball to Pygame coordinates   
    def convert_steps_to_pos(self, old_coord, steps): 
        
        # 1. Get delta_x and delta_y for 'steps over' and same for 'steps back' -- ignore direction for now / only positive 
        nw_feet_abs = np.sqrt( (steps[0] **2)/2 )
        ne_feet_abs = np.sqrt( (steps[1] **2)/2 )
        
        # 2. Package these deltas into an np array
        feet_abs = np.array([ [nw_feet_abs, nw_feet_abs], [ne_feet_abs, ne_feet_abs] ])
           
        # 3. Apply direction to all 4 deltas  
        direction_constants = np.array([ [-1, -1 ],  [1, -1] ])    # NW = -x, -y | NE = x, y
        
        NW_direct = np.sign( steps[0] )
        NE_direct = np.sign( steps[1] )
        step_directions = np.array([ [NW_direct, NW_direct], [NE_direct, NE_direct] ])
                                             
        direction_factors = step_directions * direction_constants
      
        all_delta_xy = feet_abs * direction_factors
            
        # 4. Sum x's and y's to get one delta for each -- superposition
        x = np.sum(all_delta_xy[:, 0])
        y = np.sum(all_delta_xy[:, 1])
        
        # 5. Recombine and convert to pixels 
        super_deltas = np.array([ x, y]) * self.pixels_per_step        
        
        # 6. Return absolute pos
        return old_coord + super_deltas
