""" Created: April 28

THIS IS A STANDALONE HELPER FUNC TO SUPPORT THE ANGRY-BATS SUB-PROJECT

"""

import pygame
from pygame.locals import *
import math


pygame.init()


class Setup: 
    
    def __init__(self, screen, w, h):  
        self.screen = screen
        self.screen_w = w
        self.screen_h = h
        self.pixels_per_foot = ( (355/127) + (362/127) ) / 2
        
        self.floor_thickness = 17
        self.wall_thickness = 10    
        self.top_of_floor = self.screen_h - ( self.floor_thickness )
        self.floor_bisection = self.top_of_floor + (self.floor_thickness/2)
        

        ## Playing field
        self.field_width_x = 1210 # pixels > (950, 35) - (950, 1245) from 3BC_alpha > setup
        self.of_width_x = 310 * self.pixels_per_foot
        self.inf_width_x = self.field_width_x - self.of_width_x
        
        ## Key x markers 
        self.inf_start_x = self.wall_thickness + self.of_width_x
        self.launchZone_start_x = self.inf_start_x + self.inf_width_x
        self.text_display_start_x = self.launchZone_start_x + 400
        
        ## Ball var
        self.ball_launch_y = self.top_of_floor - (4 * self.pixels_per_foot) ## 4' | This is also used to draw the launch nub
        
        ## Colours
        self.extremely_light_gray = (240, 240, 240)
        self.very_light_gray_c = (220, 220, 220)
        self.inf_gray_c = (192, 192, 192)
        self.med_gray_c = (128, 128, 128)
        self.dark_gray_c = (47,47,47)
        self.green_grass_c = (65,152,10)
        self.extremely_light_blue_c = (225, 245, 245)


    def draw_playing_area(self):

        ## WALL: Draw a thin OF wall
        x = self.wall_thickness // 2
        height = 300
        start_coord_pg = (x, self.screen_h)
        end_coord_pg = (x, self.screen_h - height)
        pygame.draw.line(self.screen, self.dark_gray_c, start_coord_pg, end_coord_pg, self.wall_thickness)
        
        ## FLOOR: Draw a green OF ~ 420-120 ~ 300'
        start_coord_pg = (self.wall_thickness, self.floor_bisection)
        end_coord_pg = (self.inf_start_x, self.floor_bisection)
        pygame.draw.line(self.screen, self.green_grass_c, start_coord_pg, end_coord_pg, self.floor_thickness)
        
        ##FLOOR: Draw a gray infield ~ 120'
        start_coord_pg = (self.inf_start_x, self.floor_bisection)
        end_coord_pg = (self.launchZone_start_x, self.floor_bisection)
        pygame.draw.line(self.screen, self.inf_gray_c, start_coord_pg, end_coord_pg, self.floor_thickness)

    
    def draw_launch_zone(self):

        ## Draw a subtle background for the launch zone
        left = self.launchZone_start_x
        top = 0
        width = self.text_display_start_x - self.launchZone_start_x # #400
        height = self.screen_h
        pygame.draw.rect( self.screen, self.extremely_light_blue_c, pygame.Rect(left, top, width, height) )
        
        ## FLOOR: Draw the launch zone floor
        start_coord = (self.launchZone_start_x, self.floor_bisection)
        end_coord = (self.text_display_start_x, self.floor_bisection)
        pygame.draw.line(self.screen, 'blue', start_coord, end_coord, self.floor_thickness)
        
        ## WALL: Draw launch 'nub' -- top is roughly point of contact on ball launches 
        start_coord = (self.launchZone_start_x, self.ball_launch_y)
        end_coord = (self.launchZone_start_x, self.screen_h)
        pygame.draw.line(self.screen, 'blue', start_coord, end_coord, 5)
    
    
    def draw_text_inferface_zone(self):

        ## Draw vertical line demarcating text interface zone
        start_coord = (self.text_display_start_x, 0)
        end_coord = (self.text_display_start_x, self.screen_h)
        pygame.draw.line(self.screen, self.med_gray_c, start_coord, end_coord, self.wall_thickness)
        
        ### Draw a border along the top of the self.screen
        start_coord = (0, 4)
        end_coord = (self.screen_w, 4)
        pygame.draw.line(self.screen, self.med_gray_c, start_coord, end_coord, self.wall_thickness)