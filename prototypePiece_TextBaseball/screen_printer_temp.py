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
    
    def __init__(self, screen, name_map, x = 200):
        self.screen = screen

        self.x_constant = x
        self.x = self.x_constant
        self.y_constant = 200
        self.y = self.y_constant
        self.tab = 30
        
        self.y_pg_break = 25
        
        self.name_map = name_map


        ## Fonts
        self.font12 = pygame.font.SysFont('Arial', 12) 
        self.font15 = pygame.font.SysFont('Arial', 15)
        self.font17 = pygame.font.SysFont('Arial', 16)
        self.font20 = pygame.font.SysFont('Arial_bold', 22)
        

    for left_side in range(1):
        
        """ LEFT SIDE OF THE SCREEN """
        def left_side(self, primary, runner, base):

            ### PREP
            if base:
                base = str(base)+"B"
            
            self.draw_major_vertical_demarcation_line(1000)
            self.new_frame() ## Reset y for start row of printing on screen

        ### STATIC INSTRUCTIONS
            
            self.print_heading( "INSTRUCTIONS" )
            self.paragraph_break()
            self.print_subheading( [ "Primary UI options:" ] )
            self.x += self.tab 
            
            tab = 150
            colour = 'black'
            primary_map = {'s': 'Change state:', 'r': "Tag runner:", 'b': 'Tag base:', 'o': 'Occupy base:', 
                   'c': 'Create baserunner:', 'x': "Reset user input:"
                   }
            
            for key, value, in primary_map.items():
                self.print_tabbed_same_line( [ value, key], tab, None, colour)
            
            self.x -= self.tab 

                        
            #### Display user input
            self.section_break()
            self.print_heading( "USER INPUT" )
            
            ### Display primary input
            self.x -= self.tab ## Adjust for normal tab on displaying UI
            self.print_user_input_tabbed( ["Primary user input:", primary], 150)
            self.x += self.tab 

            self.paragraph_break()  
            
            if primary == 'State':
                self.print_subheading( [ "Change state"] ) ### !!! MAKE THIS A SUBEADING !!!
                
                tab = 80
                state_map = {"Pre-pitch": "0", "BIP": "1", "FBC": "2"}
                
                self.x += self.tab
                
                for key, value in state_map.items():
                    self.print_tabbed_same_line( [ key, value], tab, None, colour)

                self.x -= self.tab

            elif primary == 'Tag runner':
                self.print_subheading( [ "Tag runner"] )            
                self.print_baserunner_names()
                self.print_secondary_input_subhead()
                
                self.print_user_input_tabbed( ["Runner to tag:", runner], 110 )
                                             
            
            elif primary == 'Tag base':
                self.print_subheading( [ "Tag base"] )

                self.print_str_tabbed( "Select start base: 1, 2, 3, 4")                                
                
                self.print_secondary_input_subhead()
                
                self.print_user_input_tabbed( ["Base:", base], 50 )
            

            elif primary == 'Occupy base':
                self.print_subheading( [ "Occupy base" ] )                

                self.print_str_tabbed( "Select start base: 1, 2, 3, 4")                                
                self.print_baserunner_names()

                self.print_secondary_input_subhead()
                
                self.print_user_input_tabbed( ["Base:", base], 70 )
                self.print_user_input_tabbed( ["Runner:", runner], 70 )
                

            elif primary == 'Create baserunner':
                self.print_subheading( [ "Create runner", "", "" ] )
                self.print_str_tabbed( "Select start base: 1, 2, 3, 4")

                self.print_secondary_input_subhead()
                
                self.print_user_input_tabbed( ["Base: ", base], 50)



            ## Display secondary user input
            self.y = 1350 - 500


        def print_baserunner_names(self):
            
            self.x += self.tab
            
            self.paragraph_break()
            self.print_simple( [ "Select runner using one of these keys:", "", "" ] )
            
            for key, name in self.name_map.items():
                name += ":"
                tab_pixels = 105
                self.print_tabbed_same_line( [name, key], tab_pixels, None, 'black')

            self.x -= self.tab

            self.paragraph_break()  
        

        def print_secondary_input_subhead(self):
            self.paragraph_break()  
            self.print_subheading(["Secondary user input", "", ""])
            self.paragraph_break()  



        
    """ RIGHT SIDE OF THE SCREEN """
    def right_side(self, sit_state, base_occupants, ):
        self.x = 1200
        self.y = self.y_constant
        
        for ball_in_play in range(1):
         
            self.print_heading( "STATUS:" )
            self.print_simple(["", sit_state, ""])
            
            self.section_break()
        
        """
        for runner_attainments in range(1):
            
            base_occupants = [1] ## Temp to prevent breakage
            
            self.print_heading( "OCCUPIED BASES" )
            
            for base in range(1, 4):
                str_ = str(base) + "B: "
                
                if base in base_occupants:
                    runner = base_occupants[base]
                    str_ += runner
                
                self.print_str_tabbed( [ "", str_, "" ] ) 
            
            self.paragraph_break() 
        """
            
            
        """ IGNORE RUNS AND OUTS FOR NOW
            self.print_simple( ["RUNNERS WHO SCORED, RUNNERS WHO ARE OUT", "", ""] )
            self.print_simple( ["Runners who scored:", "", ""])
            for runner in scored:
                self.print_str_tabbed( [ "", runner.name, "" ] ) 
                
            self.print_simple( ["Runners who are out:", "", ""])
            if runners_out:
                
                for runner in runners_out:
                    self.print_str_tabbed( [ "", runner, "" ] ) 
            """


        """
        self.section_break() 

        for runner_forces_tagups in range(1):

            self.print_heading( "RUNNER FORCES AND TAGUPS" )
            
            for runner, rights_dict in runner_rights.items():
                string_ = runner + " is entitled to " + rights_dict['Rights'] + " and is "
                
                if rights_dict['Forced status']:
                    string_ += "under force"
                    
                else:
                    string_ += "not under force"
                    
                self.print_simple( [ "", string_, "" ] )
                
            self.section_break() 
        """

    ## Pass text as a list: [start text, variable, end text]     
    for types_of_printing in range(1):
        
        def print_foundation_str(self, text, font, colour):
            text = font.render(text, True, colour)
            text_rect = text.get_rect()
            text_rect.topleft = (self.x, self.y)
        
            self.screen.blit(text, text_rect)

                
        def print_heading(self, text):
            font = pygame.font.SysFont('Arial_bold', 35)
            colour = 'black'
            self.print_foundation_str(text, font, colour)
            self.y += 2 * self.y_pg_break

            
        def print_subheading(self, text):
            font = pygame.font.SysFont('Arial_bold', 25)
            colour = 'black'
            
            text = text[0]
            
            self.print_foundation_str(text, font, colour)
            self.y += self.y_pg_break


        def print_simple(self, text, font = None, colour = 'black'):
            if not(font):
                font = self.font17

            text = text[0] + " " + str(text[1]) + text[2]
            self.print_foundation_str(text, font, colour)
            self.y += self.y_pg_break
            

        def print_str_tabbed(self, text_str, font = None, colour = 'black'):
            if not(font):
                font = self.font17

            self.x += self.tab 
            self.print_foundation_str(text_str, font, colour)
            self.x -= self.tab
            self.y += self.y_pg_break


        def print_tabbed_same_line(self, text, tab_pixels, font, colour = 'black'):
            if not(font):
                font = self.font17
            
            self.print_str_same_line( text[0], font, colour)

            self.x += tab_pixels
            self.print_foundation_str( text[1], font, colour )
            self.x -= tab_pixels
            
            self.y += self.y_pg_break
            
                    
        def print_str_same_line(self, text_str, font = None, colour = 'black'):
            if not(font):
                font = self.font17

            self.print_foundation_str(text_str, font, colour)
        

        def print_user_input_tabbed(self, text, tab = 100):
            self.x += self.tab 

            font = self.font17
            
            self.print_str_same_line(text[0], font, 'black')
            
            self.x += tab 
            self.print_foundation_str(text[1], font, 'blue')
            self.x -= tab

            self.x -= self.tab 

            self.y += self.y_pg_break
            



    for breaks in range(1):

        def paragraph_break(self):
            self.y += 15

        def section_break(self):
            self.paragraph_break()   
            self.draw_minor_separation_line ()        
            self.paragraph_break()   


    for helpers in range(1):
        
        def new_frame(self):
            self.y = self.y_constant
            self.x = self.x_constant

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