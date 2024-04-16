""" Created: April 16 """

import pygame
from pygame.locals import *
pygame.init()


class Ball: 

    def __init__(self, screen, coord):

        self.screen = screen
        self.coord = coord
        self.collision = False
        
  
        #### MOTION AND POSITION  ####
        
        ### LOCOMOTION -- set up, including start position and speed of locomotion 
        self.man_speed_x = 2 #4/3 # Optimal speed of NSEW locomotion = 4/3 -- pixels of movement per frame
        self.man_speed_y = 2 #4/3
        self.man_diagonal_factor = 0.744 ## Diagonal motion is 1.35x faster than North-South or lateral motion -- this should equalize that.
        
        ### Agnostic goal toggle 
        self.goal = False
        self.moving = False
        

        ### Meta attributes -- colours for boxes used during development
        self.colour = 'grey' 
        self.size = 8
 
    def reset_ball(self, coord):
        self.coord = coord
        self.goal = False
        self.moving = False
        
    def get_coord(self):
        return self.coord
        
    def update_coord(self, coord):
        self.coord = coord
    
    def move_ball(self, left, right, north, south):
        x =  self.coord[0]
        y =  self.coord[1]
    
        if left:

            if north:
                x -= self.man_speed_y * self.man_diagonal_factor
                y -= self.man_speed_x * self.man_diagonal_factor

            elif south:
                x -= self.man_speed_x * self.man_diagonal_factor
                y += self.man_speed_y * self.man_diagonal_factor

            else:
                x -= self.man_speed_x

        elif right:
            
            if north:
                x += self.man_speed_x * self.man_diagonal_factor
                y -= self.man_speed_y * self.man_diagonal_factor

            elif south:
                x += self.man_speed_x * self.man_diagonal_factor        
                y += self.man_speed_y * self.man_diagonal_factor

            else:
                x += self.man_speed_x
                
        elif north:   
            y -= self.man_speed_y
                
        elif south:        
            y += self.man_speed_y
        
        self.agnostic_pos = (x, y)
    

    def draw_ball(self):
        pygame.draw.circle(self.screen, self.colour, self.coord, self.size)
                
        
    def get_goal(self):
        return self.goal                                
   
    
    # LEFT OVER FROM MAN_FOUNDATION -- DO I NEED THIS? 
    def offset_pos(self, coord):
        x = coord[0] - (self.size / 2) 
        y = coord[1] - (self.size / 2)
        
        return (x, y)
