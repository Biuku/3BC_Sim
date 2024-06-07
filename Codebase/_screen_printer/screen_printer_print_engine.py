""" Created: May 19

Creating a temp version screen_printing to support my migration of the text-based game-rules engine from Jupyter to the IDE and pygame.
But it will remain text-based... just got too long for pyGame. Plus, this will allow easier text input and output

"""

import pygame
from pygame.locals import *

pygame.init()


class ScreenPrinter_PrintEngine: 
    
    def __init__(self, screen):
        self.screen = screen

        self.tab = 30
        self.inLine_tab = 170 
        self.text_margin = 75
        
        ## X
        self.col_width = 500
        self.x_one = 1872
        self.x_two = self.x_one + self.col_width
        self.x_three = self.x_two + self.col_width
        self.x = self.x_one +  self.text_margin
        
        ## Y
        self.y_constant = 150
        self.y = self.y_constant
        self.y_pg_break = 25

        ## Fonts
        self.font12 = pygame.font.SysFont('Arial', 12) 
        self.font15 = pygame.font.SysFont('Arial', 15)
        self.font17 = pygame.font.SysFont('Arial', 16)
        self.font20 = pygame.font.SysFont('Arial_bold', 22)
        self.font_heading = pygame.font.SysFont('Arial_bold', 35)


     
    def change_column(self, col):
        if col == 1:
            self.x = self.x_one + self.text_margin
        
        if col == 2:
            self.x = self.x_two + self.text_margin
        
        if col == 3:
            self.x = self.x_three + self.text_margin
            self.inLine_tab = 170
            
        self.new_frame()


    def draw_vertical_dividers(self):
        self.draw_UI_demarcation_line() ## Draw line separating playing field from UI

        fourth_line_x = self.x_three + self.col_width
        for x in [self.x_two, self.x_three, fourth_line_x]:
            self.draw_major_vertical_demarcation_line(x, 3)


    """ RuEg code """
    
    for RuEg_code in range(1):
        
        def print_heading_str(self, text):
            font = pygame.font.SysFont('Arial_bold', 35)
            self.print_foundation_str(text, font, 'black')
            self.y += 2 * self.y_pg_break

        
        def print_subheading_str(self, text):
            font = pygame.font.SysFont('Arial_bold', 25)
            self.print_foundation_str(text, font, 'black')
            self.y += self.y_pg_break
            

        def print_foundation_str(self, text, font, colour):
            text = font.render(text, True, colour)
            text_rect = text.get_rect()
            text_rect.topleft = (self.x, self.y)
            self.screen.blit(text, text_rect)
            
            
        def print_str(self, text, tab = 0, colour = 'black'):
            self.x += tab            
            self.print_foundation_str(text, self.font17, colour)
            self.x -= tab
            self.y += self.y_pg_break


        def print_two_same_line_li(self, text, tab = 0, inLine_tab = 0, second_colour = 'black'):
            self.x += tab
            self.print_foundation_str(text[0], self.font17, 'black')

            ## The in-line tab
            self.x += inLine_tab
            self.print_foundation_str( text[1], self.font17, second_colour )
            self.x -= inLine_tab
            
            self.x -= tab
            self.y += self.y_pg_break
        

    for legacy_code in range(1):
        
        def print_simple(self, text):
            font = self.font17
            colour = 'black'
            text = text[0] + " " + str(text[1]) + text[2]

            text = font.render(text, True, colour)
            text_rect = text.get_rect()
            text_rect.topleft = (self.x, self.y)
        
            self.screen.blit(text, text_rect)
            
            self.y += 25


        def print_coord(self, text):
            coords = []
            for coord in text[1]:
                coords.append( int(coord) )

            coords = tuple(coords)
            text[1] = str(coords)
            self.print_simple(text)


    for breaks in range(1):
        
        def paragraph_break(self):
            self.y += 25
            
        def section_break(self):
            self.paragraph_break()   
            self.draw_minor_separation_line_hz()        
            self.paragraph_break() 

        def new_frame(self):
            self.y = self.y_constant

    for separation_lines in range(1):

        ## Draw a line between the playing field and the user input space
        def draw_minor_separation_line_hz(self):
            self.y += 25
            thickness = 2
            width = 350       
            x_end = self.x + width
    
            pygame.draw.line(self.screen, 'grey', (self.x, self.y), (x_end, self.y), thickness)

            self.y += 25

        
        def draw_UI_demarcation_line(self):
            thickness = 10
            x = 1872 #self.x - pixels_to_end_of_playing_field
            self.draw_major_vertical_demarcation_line(x, thickness)
            

        def draw_major_vertical_demarcation_line(self, x, thickness = 5):
            h = self.screen.get_height()
            pygame.draw.line(self.screen, 'grey', (x, 0), (x, h), thickness)
            
        
        
    ### I THINK THE NEXT TWO ARE REDUNDANT 
        
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
