""" Created: June 7

"""

import pygame
from pygame.locals import *
from _screen_printer.screen_printer_print_engine import ScreenPrinter_PrintEngine

pygame.init()


class RightSide: 
    
    def __init__(self, screen, name_map = None, x = 200):
        self.engine = ScreenPrinter_PrintEngine(screen)
        
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
        

    def print_right_side(self, sit_state, base_occupants, runner_status, runners_out):

        ### PREP
        self.engine.change_column(2)
            
        self.print_state(sit_state)
        self.engine.section_break()

        self.print_base_occupants(base_occupants)
        self.engine.paragraph_break()  
        
        self.print_status_runners(runner_status)
        
        self.engine.section_break()
        
        self.print_runners_out(runners_out)
 

    for sections in range(1):
        
        def print_state(self, state_int):
            tab = self.tab
            inLine_tab = 50
            
            map = {0: "Pre-pitch", 1: "Ball in play", 2: "Fly ball caught"}
            state_str = None

            if state_int < 0:
                state_str = "PRE-GAME"
            
            elif state_int < 3: 
                state_str = map[state_int]

            self.engine.print_heading_str( "GAME STATUS" )
            self.engine.paragraph_break()
            self.engine.print_subheading_str( "State" )
            self.engine.print_two_same_line_li( [ "State: ", state_str], tab, inLine_tab, 'blue')

        
        def print_base_occupants(self, base_occupants):
            tab = self.tab
            inLine_tab = 75
            
            self.engine.print_subheading_str( "Base occupants" )
            
            for base, occupant_name in base_occupants.items():
                
                if base == 0:
                    base_str = "Batter"
                else:
                    base_str = str(base) + "B"
                
                if occupant_name == None:
                    occupant_name = "-"
                    
                li = [base_str, occupant_name]
                self.engine.print_two_same_line_li( li, tab, inLine_tab, 'Blue')
                

        def print_status_runners(self, runner_status):
            tab = self.tab
            inLine_tab = 100
            
            self.engine.print_subheading_str( "Runners" )
            
            self.x += self.tab
            
            ## If the dict is empty
            if not runner_status:
                self.engine.print_str("No runners")
            
            for name, sub_dict in runner_status.items():
                self.engine.print_str(name, 0, 'blue')
                
                for key, value in sub_dict.items():
                    li = [key, value]
                    self.engine.print_two_same_line_li(li, tab, inLine_tab, 'blue')
                
                self.engine.paragraph_break()

            self.x -= self.tab
            
            
        def print_runners_out(self, runners_out):
            tab = self.tab
            
            self.engine.print_subheading_str( "Runners out" )
            
            if not(runners_out):
                self.engine.print_str("No runners", tab)
                return
            
            for runner in runners_out:
                #self.engine.print_str(runner.name, tab, 'blue') ## This correctly calls the runner object
                self.engine.print_str(runner, tab, 'blue') ## This is temp for testing -- using just a str name


        def print_secondary_input_subhead(self):
            self.engine.paragraph_break()  
            self.engine.print_subheading_str("Secondary user input")

