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


    def measure_distance_in_pixels(self, start_pos, end_pos):
        
        ## Convert two sets of coordinates to a linear distance using trigonometry
        distance_in_pixels = math.sqrt( ( end_pos[0] - start_pos[0] )**2  +  ( end_pos[1] - start_pos[1] )**2 )
        
        return distance_in_pixels 

    ## Utility function to convert a line between two points into a distance in feet
    def measure_distance_in_feet(self, start_pos, end_pos):

        ## Convert two sets of coordinates to a linear distance using trigonometry        
        distance_in_pixels = self.measure_distance_in_pixels(start_pos, end_pos)
        
        return distance_in_pixels / self.pixels_per_foot 
    

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
    

    def get_total_time_seconds(self, start_time_ms):
        
        current_time = pygame.time.get_ticks()
        total_time_seconds = (current_time - start_time_ms) / 1000
        
        return total_time_seconds


    def get_gravity_delta_y(self, gravity, total_time_seconds):
        delta_y = (0.5) * gravity * (total_time_seconds**2)
        return delta_y



"""" *** SCREEN PRINTER CLASS *** """



class ScreenPrinter: 
    
    def __init__(self, screen, x_coord):
        self.screen = screen
        self.helper = Helpers(screen)
        self.x = x_coord
        self.y_constant = 400
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
        text = text[0] + ": " + str(text[1]) + text[2]
        #text = text[0] + str(11)

        text = font.render(text, True, colour)
        text_rect = text.get_rect()
    
        text_rect.topleft = (self.x, self.y)
    
        self.screen.blit(text, text_rect)
        
        self.y += 25

        
    def print_rounded(self, text, rounding):
        
        text[1] = round(text[1], rounding)
        
        self.print_simple(text)
        
    def print_int(self, text):
        
        text[1] = int(text[1])
        
        self.print_simple(text)
        
            
    def print_coord(self, text):
        coord = text[1]
        coord = ( int(coord[0]), int(coord[1]) )

        text[1] = str(coord)
        
        self.print_simple(text)
        

    
    ## Called by gamePlay
    def print_instruction_iterable(self, instruction_text, x, y):
        
        for text in instruction_text:
            self.draw_text(text, 'black', (x, y), self.font20, 1)
            y += 20
            
        #return y

    def draw_text(self, string_, colour, coord, font, justification):
        
        text = font.render(string_, True, colour)
        text_rect = text.get_rect()
    
        text_rect.topleft = coord
    
        if justification == 2: 
            text_rect.center = coord
            
        self.screen.blit(text, text_rect)

