""" Created: May 9 

Moving the heavy part of GamePlay > write_text_onScreen() to here. Will then pass it a neatly packaged dictionary of variables.


"""

import pygame
from pygame.locals import *
import math
import numpy as np

pygame.init()


 
class ScreenPrinter: 
    
    def __init__(self, screen, x = 2000):
        self.screen = screen
        

        self.x = x
        self.tab = 30
        self.y_constant = 200
        self.y = self.y_constant
        
        
       
        ## Fonts     
        self.font12 = pygame.font.SysFont('Arial', 12) 
        self.font15 = pygame.font.SysFont('Arial', 15) #pygame.font.Font('freesansbold.ttf', 15)
        self.font20 = pygame.font.SysFont('Arial', 18)


    
    def write_text_onScreen(self, general, ball_metrics, ball_inputs):
            
        ### PREP
       
        self.draw_demarcation_line()
        self.new_frame() ## Reset y for start row of printing on screen
        

        ### STATIC INSTRUCTIONS
        self.print_simple( ["INSTRUCTIONS", "", ""] )
        self.print_simple( ["Press 'b' to show Boundary Markers", "", ""] )
        self.print_simple( ["Press 'n' to show Defensive SituatioN Markers", "", ""] )
        self.print_simple( ["Press 'r' to advance the baserunneR", "", ""] )
        self.print_simple( ["Press 'SPACE' to launch a baseball", "", ""] )
        self.print_simple( ["Right-click to drop the baseball", "", ""] )
        
        self.paragraph_break()
        
        self.print_simple( ["Select a Defensive Situation:", "", ""] )
        self.print_simple_tabbed( ["- Press 'L' to reset situations", "", ""] )
        self.print_simple_tabbed( ["- Press 'ENTER' to activate current situation", "", ""] )   
        
        ## User input  
        self.print_user_input( ["You pressed:", general['defensive_sit'], general['defensive_sit_text'] ])
        self.paragraph_break()

        ## Baseball status  
        #self.print_simple( ["BASES:", "", ""] )
        #self.print_simple( ["Highest base attained:", general['base_attained'], ""] )
        #self.paragraph_break()

        self.print_simple( ["BALL LOCATION:", "", ""] )
        #self.print_simple( [ general['ball_loc_field'], "", "" ] )
        self.print_int( ["Ball height:", ball_metrics["ball_height"], "' "])
        self.print_rounded( ["Max ball height:", ball_metrics["max_ball_height"], "' "], 1)
        #self.print_int( ["Ball height in pixels:", ball_metrics["ball_height_pixels"], " pixels"])
        self.print_int( ["Ball 2D distance from Home:", ball_metrics["ball_distance_Home"], "'"])
        self.print_int( ["Ball velocity in 3D:", ball_metrics["ball_velo"], " mph"])
        self.print_coord( ["Ball 2D coord:", ball_metrics["ball_coord"], ""])
        self.paragraph_break()
        
        self.print_simple( ["Ball launched:", ball_metrics["launched_toggle"], " "] )
        #self.print_simple( ["Ball rolling", ball_metrics["rolling_toggle"], " "] )
        #self.print_simple( ["Total time:", ball_metrics["total_time"], " "] )                        
        #self.print_simple( ["Flight time", ball_metrics["flight_time"], " "] )
        self.print_simple( ["# bounces", ball_metrics["num_bounces"], " "] )
        self.paragraph_break()
        self.paragraph_break()
        
        self.print_simple( ["BALL LAUNCH (WASD: ", "", ""] )
        self.print_simple( ["Exit velo (a-d): ", ball_inputs["exit_velo"], " mph"] )
        self.print_simple( ["Launch angle (w-s)", ball_inputs["launch_angle"], "°"] )
        self.print_simple( ["Launch direction (z-x): ", ball_inputs["launch_direction"], "°"] )
        self.paragraph_break()


    def prep_screen_data(self):
        if self.curr_defensiveSit in self.defensiveSit_plays:
            self.current_defensiveSit_text = self.defensiveSit_plays[self.curr_defensiveSit][0]
    
        base_attained = self.baserunner.get_base_attained()        
        if base_attained > 0:
            self.base_attained_text = str(base_attained) + "B" 

    def new_frame(self):
        self.y = self.y_constant


    ## Pass text as a list: [start text, variable, end text]     
    for types_of_printing in range(1):
    
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

        def paragraph_break(self):
            self.y += 25


    def print_instruction_iterable(self, instruction_text, x, y):
        for text in instruction_text:
            self.draw_text(text, 'black', (x, y), self.font20, 1)
            y += 20
            

    ## Used to print a few characters next to an object for code-build. E.g., man_foundation > fielder position #; main > measuring tape data.
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


