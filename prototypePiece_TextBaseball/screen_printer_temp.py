""" Created: May 19

Creating a temp version screen_printing to support my migration of the text-based game-rules engine from Jupyter to the IDE and pygame.
But it will remain text-based... just got too long for pyGame. Plus, this will allow easier text input and output

"""

import pygame
from pygame.locals import *
import math
import numpy as np

pygame.init()


class ScreenPrinter: 
    
    def __init__(self, screen, x = 200):
        self.screen = screen

        self.x = x
        self.tab = 30
        self.y_constant = 200
        self.y = self.y_constant

        ## Fonts
        self.font12 = pygame.font.SysFont('Arial', 12) 
        self.font15 = pygame.font.SysFont('Arial', 15)
        self.font17 = pygame.font.SysFont('Arial', 16)
        self.font20 = pygame.font.SysFont('Arial', 22)
        
        
    """ LEFT SIDE OF THE SCREEN """
    def left_side(self, primary, secondary, runners_to_act):

        ### PREP
        
        self.draw_major_vertical_demarcation_line(1000)
        self.new_frame() ## Reset y for start row of printing on screen

     ### STATIC INSTRUCTIONS
        
        self.print_heading( "INSTRUCTIONS" )
        
        self.print_simple( [ "Run a contact play:     C", "", "" ] )
        self.print_simple( [ "Advance baserunner:  A ", "", "" ] )
        self.print_simple( [ "Fielder actions:            F ", "", "" ] )
        self.paragraph_break()

        self.print_simple( [ "Put the ball in play with current situation:   SPACE ", "", "" ] )
        self.print_simple( [ "Complete this play: RETURN ", "", "" ] )
        self.print_simple( [ "Reset user input:   R ", "", "" ] )
        self.section_break() 
        
        self.print_heading( "USER INPUT" )
        
        if primary == 'c':
            self.print_simple( [ "Contact play", "", "" ] )
            self.print_simple_tabbed( [ "GB: 5", "", "" ] )
            self.print_simple_tabbed( [ "FB:  6", "", "" ] )
            self.print_simple_tabbed( [ "FB caught: 7", "", "" ] )
            self.print_simple_tabbed( [ "FB not caught: 8", "", "" ] )
            self.paragraph_break()   
        
        elif primary == 'a':
            self.print_simple( [ "Advance baserunner", "", "" ] )
            self.paragraph_break()  
            
            self.print_simple( [ "Runner:", "", "" ] )
            self.print_simple_tabbed( [ "Isaac:   i ", "", "" ] )
            self.print_simple_tabbed( [ "Jack:   J ", "", "" ] )
            self.print_simple_tabbed( [ "JD:     D ", "", "" ] )

            self.paragraph_break()   
            self.print_simple( [ "Direction:", "", "" ] )
            
            self.print_simple_tabbed( [ "Forward: 9", "", "" ] )
            self.print_simple_tabbed( [ "Back:      0", "", "" ] )

            self.paragraph_break()   
        
        elif primary == 'f':
            self.print_simple( [ "Fielder actions", "", "" ] )
            self.paragraph_break()   
              
            self.print_simple( [ "Tag a base: 1, 2, 3", "", "" ] )
            
            self.paragraph_break()   
            self.print_simple( [ "Tag a runner: ", "", "" ] )
            
            self.print_simple_tabbed( [ "Isaac:   i ", "", "" ] )
            self.print_simple_tabbed( [ "Jack:   J ", "", "" ] )
            self.print_simple_tabbed( [ "JD:     D ", "", "" ] )
            self.section_break() 
        
        ## Display secondary user input
        self.y = 1350 - 500

        self.print_simple( [ "Secondary user input:     ", secondary, "" ] )        
        self.print_joined_list( ["Runners to act: ", runners_to_act, ""] )
                
        
    """ RIGHT SIDE OF THE SCREEN """
    def right_side(self, sit_state, base_occupants, scored, runners_out, runner_rights, tagable_bases):
        self.x = 1200
        self.y = self.y_constant
        
        for ball_in_play in range(1):
         
            self.print_heading( "STATUS:" )
            self.print_simple(["", sit_state, ""])
            
            self.section_break()
        
        
        for runner_attainments in range(1):
            
            self.print_heading( "OCCUPIED BASES" )
            
            for base in range(1, 4):
                str_ = str(base) + "B: "
                
                if base in base_occupants:
                    runner = base_occupants[base]
                    str_ += runner
                
                self.print_simple_tabbed( [ "", str_, "" ] ) 
            
            self.paragraph_break() 
            
            self.print_simple( ["RUNNERS WHO SCORED, RUNNERS WHO ARE OUT", "", ""] )
            self.print_simple( ["Runners who scored:", "", ""])
            for runner in scored:
                self.print_simple_tabbed( [ "", runner.name, "" ] ) 
                
            self.print_simple( ["Runners who are out:", "", ""])
            if runners_out:
                
                for runner in runners_out:
                    self.print_simple_tabbed( [ "", runner, "" ] ) 
            


            self.section_break() 

        
        for runner_rights_ in range(1):

            self.print_heading( "RUNNER RIGHTS AND FORCES" )
            
            for runner, rights_dict in runner_rights.items():
                string_ = runner + " is entitled to " + rights_dict['Rights'] + " and is "
                
                if rights_dict['Forced status']:
                    string_ += "under force"
                    
                else:
                    string_ += "not under force"
                    
                self.print_simple( [ "", string_, "" ] )
                
            self.section_break() 
        
        
        ### Tagable bases
        for tagable_bases_ in range(1):
            
            self.print_heading( "TAGABLE BASES -- CAN BE TAGGED TO PUT THE RUNNER OUT" )
                        
            for base, runner in tagable_bases.items():
                if runner: 
                    string_ = str(base) + "B: " + runner
                    self.print_simple( [ "", string_, "" ] )
            
        self.x = 200


    ## Pass text as a list: [start text, variable, end text]     
    for types_of_printing in range(1):
        
        
        def print_heading(self, text):
            font = self.font20
            colour = 'black'
            
            text = font.render(text, True, colour)
            text_rect = text.get_rect()
            text_rect.topleft = (self.x, self.y)
        
            self.screen.blit(text, text_rect)
            
            self.y += 25
            self.y += 25


        def print_simple(self, text):
            #font = self.font20
            font = self.font17
            colour = 'black'
            text = text[0] + " " + str(text[1]) + text[2]

            text = font.render(text, True, colour)
            text_rect = text.get_rect()
        
            text_rect.topleft = (self.x, self.y)
        
            self.screen.blit(text, text_rect)
            
            self.y += 25


        def print_joined_list(self, text):
            text[1] = " ".join(text[1])
            self.print_simple(text)
            
        
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

        def section_break(self):
            self.paragraph_break()   
            self.draw_minor_separation_line ()        
            self.paragraph_break()   


    for helpers in range(1):
        
        def new_frame(self):
            self.y = self.y_constant

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
        
        def draw_minor_separation_line(self):
            
            self.y += 25
            x_end = self.x + 400
            thickness = 2
            
            pygame.draw.line(self.screen, 'grey', (self.x, self.y), (x_end, self.y), thickness)
            
            self.y += 25

        
        def draw_major_vertical_demarcation_line(self, x):
            h = self.screen.get_height()
            
            pygame.draw.line(self.screen, 'grey', (x, 0), (x, h), 5)


# Last line