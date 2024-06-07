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
            if base != None:
                base = str(base)+"B"
            
            self.draw_major_vertical_demarcation_line(1000)
            self.new_frame() ## Reset y for start row of printing on screen

            ## DO LEFT SIDE
            self.print_LS_static_instructions()
            self.section_break()                            

            self.print_primary_UI(primary)
            self.section_break()

            if primary == 'State':
                self.print_UI_state()

            elif primary == 'Tag runner':
                self.print_UI_tagRunner(runner)

            elif primary == 'Tag base':
                self.print_UI_tagBase(base)

            elif primary == 'Occupy base':
                self.print_UI_occupyBase(base, runner)

            elif primary == 'Create baserunner':
                self.print_UI_createBaserunner(base)


        def print_LS_static_instructions(self):
            tab = self.tab
            inLine_tab = 150
            
            primary_map = {'s': 'Change state:', 'r': "Tag runner:", 'b': 'Tag base:', 'o': 'Occupy base:', 
                   'c': 'Create baserunner:', 'x': 'Reset user input:'}

            self.print_heading_str( "INSTRUCTIONS" )
            self.paragraph_break()
            self.print_subheading_str( "Primary UI options:" )

            for key, value, in primary_map.items():
                self.print_two_same_line_li( [ value, key], tab, inLine_tab, 'black')


        def print_primary_UI(self, primary):
            tab = self.tab
            inLine_tab = 150

            self.print_heading_str( "USER INPUT" )

            self.print_two_same_line_li( ["Primary user input:", primary], tab, inLine_tab, 'blue')   


        def print_UI_state(self):
            tab = self.tab
            inLine_tab = 80
            state_map = {"Pre-pitch": "0", "BIP": "1", "FBC": "2"}
            
            self.print_subheading_str( "Change state" )

            for key, value in state_map.items():
                self.print_two_same_line_li( [ key, value], tab, inLine_tab, 'black')


        def print_UI_tagRunner(self, runner):
            tab = self.tab
            inLine_tab = 110
            
            self.print_subheading_str( "Tag runner" )            
            self.print_baserunner_names()
            self.print_secondary_input_subhead()
            self.print_two_same_line_li( ["Runner to tag:", runner], tab, inLine_tab, 'blue' )


        def print_UI_tagBase(self, base):
            tab = self.tab
            inLine_tab = 50
                        
            self.print_subheading_str( "Tag base" )
            self.print_str( "Select start base: 1, 2, 3, 4", tab, 'black')                                
            self.print_secondary_input_subhead()
            self.print_two_same_line_li( ["Base:", base], tab, inLine_tab, 'blue' )
        
        
        def print_UI_occupyBase(self, base, runner):
            tab = self.tab
            inLine_tab = 70
            
            self.print_subheading_str( "Occupy base" )                

            self.print_str( "Select start base: 1, 2, 3, 4", self.tab, 'black')                                
            self.print_baserunner_names()

            self.print_secondary_input_subhead()
            
            self.print_two_same_line_li( ["Base:", base], tab, inLine_tab, 'blue' )
            self.print_two_same_line_li( ["Runner:", runner], tab, inLine_tab, 'blue')
        
        
        def print_UI_createBaserunner(self, base):
            tab = self.tab
            inLine_tab = 50
            
            self.print_subheading_str( "Create runner" )
            self.print_str( "Select start base: 1, 2, 3, 4", self.tab, 'black')

            self.print_secondary_input_subhead()
            
            self.print_two_same_line_li( ["Base: ", base], tab, inLine_tab, 'blue')


        def print_baserunner_names(self):
            tab = self.tab
            inLine_tab = 40
            
            self.paragraph_break()
            self.print_str( "Select runner using one of these keys:", tab )
            
            for key, name in self.name_map.items():
                name += ":"
                inLine_tab = 105
                self.print_two_same_line_li( [name, key], tab, inLine_tab, 'black')

            self.paragraph_break()  


        def print_secondary_input_subhead(self):
            self.paragraph_break()  
            self.print_subheading_str("Secondary user input")


    for right_side in range(1): 
        """ RIGHT SIDE OF THE SCREEN """

        def right_side(self, sit_state, base_occupants, runner_status, runners_out):
            self.x = 1200
            self.y = self.y_constant
            
            self.print_state(sit_state)
            self.section_break()

            self.print_base_occupants(base_occupants)
            self.paragraph_break()  
            
            self.print_status_runners(runner_status)
            
            self.section_break()
            
            self.print_runners_out(runners_out)
 

        def print_state(self, state_int):
            tab = self.tab
            inLine_tab = 50
            
            map = {0: "Pre-pitch", 1: "Ball in play", 2: "Fly ball caught"}
            state_str = None

            if state_int < 0:
                state_str = "PRE-GAME"
            
            elif state_int < 3: 
                state_str = map[state_int]

            self.print_heading_str( "GAME STATUS" )
            self.paragraph_break()
            self.print_subheading_str( "State" )
            self.print_two_same_line_li( [ "State: ", state_str], tab, inLine_tab, 'blue')

        
        def print_base_occupants(self, base_occupants):
            tab = self.tab
            inLine_tab = 75
            
            self.print_subheading_str( "Base occupants" )
            
            for base, occupant_name in base_occupants.items():
                
                if base == 0:
                    base_str = "Batter"
                else:
                    base_str = str(base) + "B"
                
                if occupant_name == None:
                    occupant_name = "-"
                    
                li = [base_str, occupant_name]
                self.print_two_same_line_li( li, tab, inLine_tab, 'Blue')
                

        def print_status_runners(self, runner_status):
            tab = self.tab
            inLine_tab = 100
            
            self.print_subheading_str( "Runners" )
            
            self.x += self.tab
            
            ## If the dict is empty
            if not runner_status:
                self.print_str("No runners")
            
            for name, sub_dict in runner_status.items():
                self.print_str(name, 0, 'blue')
                
                for key, value in sub_dict.items():
                    li = [key, value]
                    self.print_two_same_line_li(li, tab, inLine_tab, 'blue')
                
                self.paragraph_break()

            self.x -= self.tab
            
            
        def print_runners_out(self, runners_out):
            tab = self.tab
            
            self.print_subheading_str( "Runners out" )
            
            if not(runners_out):
                self.print_str("No runners", tab)
                return
            
            for runner in runners_out:
                self.print_str(runner.name, tab, 'blue')

    
        """
        for runner_attainments in range(1):


        self.section_break() 

        for runner_forces_tagups in range(1):

            self.print_heading_str( "RUNNER FORCES AND TAGUPS" )
            
            for runner, rights_dict in runner_rights.items():
                string_ = runner + " is entitled to " + rights_dict['Rights'] + " and is "
                
                if rights_dict['Forced status']:
                    string_ += "under force"
                    
                else:
                    string_ += "not under force"
                    
                self.print_simple_li( [ "", string_, "" ] )
                
            self.section_break() 
        """

    for types_of_printing in range(1):
        
        def print_foundation_str(self, text, font, colour):
            text = font.render(text, True, colour)
            text_rect = text.get_rect()
            text_rect.topleft = (self.x, self.y)
        
            self.screen.blit(text, text_rect)
            
                
        def print_heading_str(self, text):
            font = pygame.font.SysFont('Arial_bold', 35)
            self.print_foundation_str(text, font, 'black')
            self.y += 2 * self.y_pg_break

            
        def print_subheading_str(self, text):
            font = pygame.font.SysFont('Arial_bold', 25)
            self.print_foundation_str(text, font, 'black')
            self.y += self.y_pg_break


        def print_simple_li(self, text, tab = 0, colour = 'black'):
            self.x += tab

            text = text[0] + " " + str(text[1]) + text[2]
            self.print_foundation_str(text, self.font17, colour)
            self.x -= tab
            
            self.y += self.y_pg_break

            
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