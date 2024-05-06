""" Created: April 16 

Shifting a few common functions here

"""

import pygame
from pygame.locals import *
import math
import numpy as np
#from setup import Setup

pygame.init()


class Helpers: 
    
    def __init__(self, screen):
        self.screen = screen
        self.pixels_per_foot =  2.8088
        self.pixels_per_step = self.pixels_per_foot * 2.5
    
         ## Fonts     
        self.font12 = pygame.font.SysFont('Arial', 12) 
        self.font15 = pygame.font.SysFont('Arial', 15) #pygame.font.Font('freesansbold.ttf', 15)
        self.font20 = pygame.font.SysFont('Arial', 18)
    
    
    """ NEW FUNCTIONS FROM ANGRY BATS """ 
    def get_total_time_seconds(self, start_time_ms): 
        current_time = pygame.time.get_ticks()
        total_time_seconds = (current_time - start_time_ms) / 1000
        
        return total_time_seconds
    
    
    ## Utility function to convert a line between two points into a distance in feet
    def measure_distance_in_feet(self, start_pos, end_pos):
        distance_in_pixels = self.measure_distance_in_pixels(start_pos, end_pos)
        return distance_in_pixels / self.pixels_per_foot  
    
    
    def measure_distance_in_pixels(self, start_pos, end_pos):
        distance_in_pixels = math.sqrt( ( end_pos[0] - start_pos[0] )**2  +  ( end_pos[1] - start_pos[1] )**2 )
        return distance_in_pixels 


    def measure_3D_distance_in_pixels(self, start_coord, end_coord):
        x1, y1, z1 = start_coord
        x2, y2, z2 = end_coord
        
        ## Step 1 -- Find distance to the middle_coord -- i.e., to the end_coord, but with the same height as the start coord
        distance_to_middle_coord_2D = math.sqrt( (x2-x1)**2 + (y2-y1)**2 ) #self.measure_distance_in_pixels( (x1, y1), (x2, y2))
        
        ## Step 2 -- Use this new value as the base of a triangle with opp = the height
        distance_3D = math.sqrt( distance_to_middle_coord_2D**2 + (z2 - z1)**2 )
        
        return distance_3D
  

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
    
 
    """ LEGACY SCREEN PRINTING FUNCTIONS -- BASERUNNER ID, ETC. """
    def draw_text(self, string_, colour, coord, font, justification):      
        text = font.render(string_, True, colour)
        text_rect = text.get_rect()
    
        text_rect.topleft = coord
    
        if justification == 2: 
            text_rect.center = coord
            
        self.screen.blit(text, text_rect)



""" ANGRYBATS SCREEN PRINTER CLASS """
class ScreenPrinter: 
    
    def __init__(self, screen, x_coord):
        self.screen = screen
        self.helper = Helpers(screen)
        self.x = x_coord
        self.tab = 30
        self.y_constant = 300
        self.y = self.y_constant
       
        ## Fonts     
        self.font12 = pygame.font.SysFont('Arial', 12) 
        self.font15 = pygame.font.SysFont('Arial', 15) #pygame.font.Font('freesansbold.ttf', 15)
        self.font20 = pygame.font.SysFont('Arial', 18)

    ## Pass text as a list: [start text, variable, end text]     
    def new_frame(self):
        self.y = self.y_constant
    
    def paragraph_break(self):
        self.y += 25
        
    def print_simple(self, text):
        font = self.font20
        colour = 'black'
        text = text[0] + " " + str(text[1]) + text[2]

        text = font.render(text, True, colour)
        text_rect = text.get_rect()
    
        text_rect.topleft = (self.x, self.y)
    
        self.screen.blit(text, text_rect)
        
        self.y += 25
        
    def print_simple_tabbed(self, text):
        self.x += self.tab 
        self.print_simple(text)
        self.x -= self.tab
        
    def print_user_input(self, text):
        text[2] = "  " + text[2]
        self.print_simple(text)
        
    def print_rounded(self, text, rounding):
        text[1] = round(text[1], rounding)
        self.print_simple(text)
        
    def print_int(self, text):
        text[1] = int(text[1])
        self.print_simple(text)
        
    def print_coord(self, text):
        
        coords = []
        for coord in text[1]:
        
            coords.append( int(coord) )

        coords = tuple(coords)
        text[1] = str(coords)

        
        self.print_simple(text)

    def print_instruction_iterable(self, instruction_text, x, y):
        for text in instruction_text:
            self.draw_text(text, 'black', (x, y), self.font20, 1)
            y += 20
            
    def draw_text(self, string_, colour, coord, font, justification):
        text = font.render(string_, True, colour)
        text_rect = text.get_rect()
    
        text_rect.topleft = coord
    
        if justification == 2: 
            text_rect.center = coord
            
        self.screen.blit(text, text_rect)

    ## Draw a line between the playing field and the user input space
    def draw_demarcation_line(self):
        h = self.screen.get_height()
        
        pixels_to_end_of_playing_field = 128
        x = self.x - pixels_to_end_of_playing_field 
        
        pygame.draw.line(self.screen, 'grey', (x, 0), (x, h), 5)

