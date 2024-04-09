""" April 7, 2024 -- Refactoring my single instance of a 'man' (able to run/move) into an object """

import pygame
from pygame.locals import *
from pygame.sprite import Sprite


class Man(): #Sprite

    def __init__(self, screen, x, y, team):

        #super().__init__()
        self.screen = screen

        self.team = team # "baserunner" or "fielder"
        self.man_x = x # start position
        self.man_y = y # start position
        
       

        #### Draw sprites    
        self.screen.blit(self.man_curr_frame, (int(self.man_x), int(self.man_y)))
            
