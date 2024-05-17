""" Created: April 16 | Shifting a few common functions here

"""

import pygame
from pygame.locals import *
import math
import numpy as np

from setup import Setup

pygame.init()


class Helpers:

    def __init__(self):
        
        self.setup = Setup()
        self.main_centroid_radius = self.measure_distance_in_pixels(self.setup.main_centroid,  self.setup.cf_wall)
        
        self.pixels_per_foot =  2.8088
        self.feet_per_pixel = 1 / self.pixels_per_foot
        self.pixels_per_step = self.pixels_per_foot * 2.5
    
        ## Fonts
        self.font12 = pygame.font.SysFont('Arial', 12) 
        self.font15 = pygame.font.SysFont('Arial', 15) #pygame.font.Font('freesansbold.ttf', 15)
        self.font20 = pygame.font.SysFont('Arial', 18)


    ## Utility function to convert a line between two points into a distance in feet
    def measure_distance_in_feet(self, start_coord, end_coord):
        
        distance_in_pixels = self.measure_distance_in_pixels(start_coord, end_coord)
        
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


    def get_ball_theta_deg(self, ball_coord):
        centroid = self.setup.boundaries['four_B_tip']
        
        theta_rad = self.coord_to_theta(centroid, ball_coord)
        theta_deg = math.degrees(theta_rad)
        
        return theta_deg




    ## Not sure I still use these

    def get_total_time_seconds(self, start_time_ms): 
        current_time = pygame.time.get_ticks()
        total_time_seconds = (current_time - start_time_ms) / 1000
        
        return total_time_seconds


# Last line