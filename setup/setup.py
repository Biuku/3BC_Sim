""" March 22, 2024 """

import pygame

class Setup:
    def __init__(self):
        self.win_w = 3000
        self.win_h = 1300
        
        self.white, self.black = (255, 255, 255), (10, 10, 10)
        self.light_grey, self.grey, self.dark_grey = (200, 200, 200), (100,100,100), (45, 45, 45)
        self.blue, self.light_blue = (190, 170, 255), (164, 150, 255),
        self.red, self.light_red = (235, 52, 52), (255, 175, 175)
        self.green = (35, 130, 60)
        
        
         ## Pager border
        self.border_gap = 0.01 ## In percent
        self.left_border = self.win_w * self.border_gap
        self.top_border = self.win_h * self.border_gap
 
        self.border_w = self.win_w * (1 - (2 * self.border_gap))
        self.border_h = self.win_h * (1 - (2 * self.border_gap))

        self.border_colour = self.light_grey
        self.border_thickness = 3
        
        
        
    """ Draw rectangle around the entire page to give it an edge """
    def draw_page_border(self, win):
        
        pygame.draw.rect(win, self.border_colour, pygame.Rect(self.left_border, self.top_border, self.border_w, self.border_h), self.border_thickness)
         



""" STUFF I'LL USE LATER 

    self.clock = pygame.time.Clock()
    self.FPS = 120

    self.small_font = pygame.font.SysFont('lucidasans', 10)
    self.med_font = pygame.font.SysFont('lucidasans', 11)
    self.large_font = pygame.font.SysFont('lucidasans', 12)
"""