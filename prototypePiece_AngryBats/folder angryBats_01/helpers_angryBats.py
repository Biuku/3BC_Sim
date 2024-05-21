""" Created: April 25

THIS IS A STANDALONE HELPER FUNC TO SUPPORT THE ANGRY-BATS SUB-PROJECT

"""

import pygame
from pygame.locals import *
import math


pygame.init()


class Helpers: 
    
    def __init__(self, screen):
        self.screen = screen
        self.pixels_per_foot = ( (355/127) + (362/127) ) / 2
        self.pixels_per_step = self.pixels_per_foot * 2.5
        #self.setup = Setup(self.screen)
        
         ## Fonts     
        self.font12 = pygame.font.SysFont('Arial', 12) 
        self.font15 = pygame.font.SysFont('Arial', 15) #pygame.font.Font('freesansbold.ttf', 15)
        self.font20 = pygame.font.SysFont('Arial', 18)
    

    def draw_text(self, string_, colour, coord, font, justification):
        
        text = font.render(string_, True, colour)
        text_rect = text.get_rect()
    
        text_rect.topleft = coord
    
        if justification == 2: 
            text_rect.center = coord
            
        self.screen.blit(text, text_rect)

    ## Called by gamePlay
    def print_instruction_iterable(self, instruction_text, x, y):
        
        for text in instruction_text:
            self.draw_text(text, 'black', (x, y), self.font20, 1)
            y += 20
            
        #return y

        
    ## Utility function to convert a line between two points into a distance in feet
    def measure_distance_in_feet(self, start_pos, end_pos):
    
        ## First, what is the conversion factor? Average the pixels between 1B/3B and 2B/4B 
        pixels_to_feet = ( (355/127) + (362/127) ) / 2
        
        ## Next, convert two sets of coordinates to a linear distance using trigonometry        
        distance_in_pixels = self.measure_distance_in_pixels(start_pos, end_pos)
        
        return distance_in_pixels / pixels_to_feet 
    
    
    def measure_distance_in_pixels(self, start_pos, end_pos):
        
        ## Convert two sets of coordinates to a linear distance using trigonometry
        distance_in_pixels = math.sqrt( ( end_pos[0] - start_pos[0] )**2  +  ( end_pos[1] - start_pos[1] )**2 )
        
        return distance_in_pixels 


    ## Get end-coord coord from start_coord, angle theta, and distance 
    def theta_to_endCoord(self, start_coord, theta_deg, dist_pixels):
        
        theta_rad = math.radians(theta_deg)
        end_x = start_coord[0] + dist_pixels * math.cos(theta_rad)
        end_y = start_coord[1] - dist_pixels * math.sin(theta_rad) # Negative because Pygame Y axis
        
        return (end_x, end_y)

    
    def coord_to_theta(self, start_coord, end_coord):
        adj = dx = end_coord[0] - start_coord[0]
        opp = dy = -1 * (end_coord[1] - start_coord[1]) # -1 *    # Negative because Pygame Y axis
        hyp = math.sqrt(adj**2 + opp**2)
        
        #theta_rad = math.acos(adj/hyp)
        theta_rad = math.atan2(opp, adj) # Got this formula from Chat GPT... I don't really understand trig well enough to know it intuitively
        
        return theta_rad
    
    
    def get_y_for_given_feet(self, start_pos, end_pos):

        ## First, what is the conversion factor? Average the pixels between 1B/3B and 2B/4B 
        pixels_to_feet = ( (355/127) + (362/127) ) / 2
        
        ## Next, convert two sets of coordinates to a linear distance using trigonometry
        distance_in_pixels = math.sqrt( ( end_pos[0] - start_pos[0] )**2  +  ( end_pos[1] - start_pos[1] )**2 )
        
        return distance_in_pixels / pixels_to_feet 


