""" Created: June 7

"""

import pygame
from pygame.locals import *
from _screen_printer.screen_printer_print_engine import ScreenPrinter_PrintEngine

pygame.init()


class LeftSide: 
    
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
        

    def print_left_side(self, primary, runner, base):

        ### PREP
        self.engine.change_column(1)
        
        if base != None:
            base = str(base)+"B"

        ## DO LEFT SIDE
        self.print_LS_static_instructions()
        self.engine.section_break()                            

        self.print_primary_UI(primary)
        self.engine.section_break()

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


    for sections in range(1):

        def print_LS_static_instructions(self):
            tab = self.tab
            inLine_tab = 150
            
            primary_map = {'s': 'Change state:', 'r': "Tag runner:", 'b': 'Tag base:', 'o': 'Occupy base:', 
                   'c': 'Create baserunner:', 'x': 'Reset user input:'}

            self.engine.print_heading_str( "INSTRUCTIONS" )
            self.engine.paragraph_break()
            self.engine.print_subheading_str( "Primary UI options:" )

            for key, value, in primary_map.items():
                self.engine.print_two_same_line_li( [ value, key], tab, inLine_tab, 'black')


        def print_primary_UI(self, primary):
            tab = self.tab
            inLine_tab = 150

            self.engine.print_heading_str( "USER INPUT" )
            self.engine.print_two_same_line_li( ["Primary user input:", primary], tab, inLine_tab, 'blue')   


        def print_UI_state(self):
            tab = self.tab
            inLine_tab = 80
            state_map = {"Pre-pitch": "0", "BIP": "1", "FBC": "2"}
            
            self.engine.print_subheading_str( "Change state" )

            for key, value in state_map.items():
                self.engine.print_two_same_line_li( [ key, value], tab, inLine_tab, 'black')


        def print_UI_tagRunner(self, runner):
            tab = self.tab
            inLine_tab = 110
            
            self.engine.print_subheading_str( "Tag runner" )            
            self.print_baserunner_names()
            self.print_secondary_input_subhead()
            self.engine.print_two_same_line_li( ["Runner to tag:", runner], tab, inLine_tab, 'blue' )


        def print_UI_tagBase(self, base):
            tab = self.tab
            inLine_tab = 50
                        
            self.engine.print_subheading_str( "Tag base" )
            self.engine.print_str( "Select start base: 1, 2, 3, 4", tab, 'black')                                
            self.print_secondary_input_subhead()
            self.engine.print_two_same_line_li( ["Base:", base], tab, inLine_tab, 'blue' )
        
        
        def print_UI_occupyBase(self, base, runner):
            tab = self.tab
            inLine_tab = 70
            
            self.engine.print_subheading_str( "Occupy base" )                

            self.engine.print_str( "Select start base: 1, 2, 3, 4", self.tab, 'black')                                
            self.print_baserunner_names()

            self.print_secondary_input_subhead()
            
            self.engine.print_two_same_line_li( ["Base:", base], tab, inLine_tab, 'blue' )
            self.engine.print_two_same_line_li( ["Runner:", runner], tab, inLine_tab, 'blue')
        
        
        def print_UI_createBaserunner(self, base):
            tab = self.tab
            inLine_tab = 50
            
            self.engine.print_subheading_str( "Create runner" )
            self.engine.print_str( "Select start base: 1, 2, 3, 4", self.tab, 'black')

            self.print_secondary_input_subhead()
            
            self.engine.print_two_same_line_li( ["Base: ", base], tab, inLine_tab, 'blue')


        def print_baserunner_names(self):
            tab = self.tab
            inLine_tab = 40
            
            self.engine.paragraph_break()
            self.engine.print_str( "Select runner using one of these keys:", tab )
            
            for key, name in self.name_map.items():
                name += ":"
                inLine_tab = 105
                self.engine.print_two_same_line_li( [name, key], tab, inLine_tab, 'black')

            self.engine.paragraph_break()  


        def print_secondary_input_subhead(self):
            self.engine.paragraph_break()  
            self.engine.print_subheading_str("Secondary user input")

