""" Created: May 9 
Moving the heavy part of GamePlay > write_text_onScreen() to here. Will then pass it a neatly packaged dictionary of variables.
"""

import pygame
from pygame.locals import *

from _screen_printer.screen_printer_print_engine import ScreenPrinter_PrintEngine
from _screen_printer.screen_printer_left_side import LeftSide
from _screen_printer.screen_printer_right_side import RightSide

pygame.init()


class ScreenPrinter: 
    
    def __init__(self, screen):
        self.engine = ScreenPrinter_PrintEngine(screen)
        self.left_side = LeftSide(screen)
        self.right_side = RightSide(screen)
        
        self.screen = screen
        
        self.tab = 30
        self.text_margin = 50
        
        ## X
        self.x_one = 1872
        self.x_two = self.x_one + 550
        self.x_three = self.x_two + 550

        self.x = self.x_one +  self.text_margin
        
        ## Y
        self.y_constant = 150
        self.y = self.y_constant
        self.y_pg_break = 25
        
        self.name_map = {}

        ## Data buckets for organizing what is passed from GamePlay
        self.general = None
        self.ball_metrics = None
        self.ball_inputs = None

        ## Fonts
        self.font12 = pygame.font.SysFont('Arial', 12) 
        self.font15 = pygame.font.SysFont('Arial', 15)
        self.font17 = pygame.font.SysFont('Arial', 16)
        self.font20 = pygame.font.SysFont('Arial', 18)


    def print_UI_to_screen(self, general, ball_metrics, ball_inputs):
        self.general = general
        self.ball_metrics = ball_metrics
        self.ball_inputs = ball_inputs

        for temp_constants in range(1):
            ## Left side
            primary = 's'
            runner = 'Isaac'
            base = '2B'
            ## Right side
            state = 0
            base_occupants = {0: None, 1: 'Isaac', 2: None, 3: None} 
            runner_status = { 'Isaac': {"Attained": '2B', 'Occupied': '2B',"Forced-to": '-', "Tag-up": '-'} }
            runners_out = ['Pasma']

        self.engine.draw_vertical_dividers()
        self.left_side.print_left_side(primary, runner, base)
        self.right_side.print_right_side(state, base_occupants, runner_status, runners_out)

        self.print_legacy_onScreen_text()


    def print_legacy_onScreen_text(self):

        self.engine.change_column(3)
        self.x = self.x_three + self.text_margin
        inLine_tab = 170 

        ### PREP
 
        ### STATIC INSTRUCTIONS
        self.engine.print_heading_str( "INSTRUCTIONS" )
   
        self.engine.print_simple( [ "Show boundary markers: b", "", "" ] )
        self.engine.print_simple( [ "Show defensive coords: n", "", "" ] )
        self.engine.print_simple( [ "Advance baserunner: 'r' ", "", "" ] )
        self.engine.print_simple( [ "Launch baseball: 'SPACE'", "", "" ] )
        self.engine.paragraph_break()
        
        self.engine.print_simple( [ "Drop baseball: k", "", "" ] )
        self.engine.print_simple( [ "Throw ball: h", "", "" ] )
        self.engine.print_simple( [ "Change throw target: j", "", "" ] )

        self.engine.draw_minor_separation_line_hz ()
         
        self.engine.print_subheading_str( "Select a Defensive Situation"  )
        self.engine.print_str( "- Reset situation: L" )
        self.engine.print_str( "- Activate current situation: 'ENTER'") 
        
        ## User input  
        self.engine.print_two_same_line_li( ["You pressed:", str( self.general['defensive_sit'] ) + "  " + str( self.general['defensive_sit_text'] ) ], 0, inLine_tab, 'blue' )
        self.engine.draw_minor_separation_line_hz ()
        
        ## Launch metrics
        self.engine.print_subheading_str( "BALL LAUNCH (WASD) " )
        self.engine.print_two_same_line_li( ["Exit velo (a-d): ", str(self.ball_inputs["exit_velo"]) + " mph"],0, inLine_tab, 'blue' )
        self.engine.print_two_same_line_li( ["Launch angle (w-s)", str( self.ball_inputs["launch_angle"] ) + "°"] , 0, inLine_tab, 'blue' )
        self.engine.print_two_same_line_li( [ "Launch direction (z-x): ", str( self.ball_inputs["launch_direction"] ) + "°"], 0, inLine_tab, 'blue' )
        self.engine.draw_minor_separation_line_hz ()

        ## Runners on base  
        self.engine.print_subheading_str( "BASES" )
        self.engine.print_two_same_line_li( ["Base attained:", str( self.general['base_attained'] ) + ""], 0, inLine_tab, 'blue' )
        self.engine.draw_minor_separation_line_hz ()
        
        ## Throwing  
        self.engine.print_subheading_str( "THROW" )
        self.engine.print_two_same_line_li( ["Fielder with the ball:", str( self.general['fielder with ball'] ) + ""], 0, inLine_tab, 'blue' )
        self.engine.print_two_same_line_li( ["Target of throw:", str( self.general['throw receiver'] ) + ""], 0, inLine_tab, 'blue' )
        self.engine.draw_minor_separation_line_hz ()

        ## Ball
        self.engine.print_subheading_str( "BALL" )
        self.engine.print_simple( ["Ball launched:", self.ball_metrics["launched_toggle"], " "] )
        self.engine.print_two_same_line_li( ["Ball rolling: ", str( self.ball_metrics["rolling_toggle"] ) ], 0, inLine_tab, 'blue' )
        self.engine.print_two_same_line_li( ["# bounces: ", str( self.ball_metrics["num_bounces"] ) + ""], 0, inLine_tab, 'blue' )
        self.engine.paragraph_break()
        
        self.engine.print_two_same_line_li( [ "Ball location (L-R): ", str( self.general['ball_loc_field'] ) + ""], 0, inLine_tab, 'blue' )
        self.engine.print_two_same_line_li( [ "Ball depth: ", str( self.general['ball_depth'] ) ], 0, inLine_tab, 'blue' )
        self.engine.print_two_same_line_li( [ "Ball height:", str( int( self.ball_metrics["ball_height"] ) ) + "'"  ], 0, inLine_tab, 'blue' )

        # self.engine.print_simple( ["Max ball height:", round( self.ball_metrics["max_ball_height"], 1), "' "])
        # self.engine.print_simple( ["Ball height in pixels:", int( self.ball_metrics["ball_height_pixels"] ), " pixels"])
        # self.engine.print_simple( ["Ball 2D distance from Home:", int( self.ball_metrics["ball_distance_Home"] ), "'"])
        # self.engine.print_simple( ["Ball velocity in 3D:", int( self.ball_metrics["ball_velo"] ), " mph"])
        # self.print_coord( ["Ball 2D coord:", self.ball_metrics["ball_coord"], ""])

        self.engine.draw_minor_separation_line_hz ()


    ## Used to print a few characters next to an object for code-build. E.g., man_foundation > fielder position #; main > measuring tape data.
    def draw_text(self, string_, colour, coord, font, justification):
        text = font.render(string_, True, colour)
        text_rect = text.get_rect()
    
        text_rect.topleft = coord
    
        if justification == 2: 
            text_rect.center = coord
            
        self.screen.blit(text, text_rect)


    for june6_temp_ruler in range(1):
        def temp_display_x_ruler(self):
            #Displays a ruler atop right side to help me plan how to organize user interface 
            step = 100
            y = self.y_constant - 50
            font = pygame.font.SysFont('Arial', 11) 
            justification = 2
            for x in range(1600, 3401, step):
                pygame.draw.line(self.screen, 'grey', (x, y-5), (x, y+5), 1)
                x_str = str(x) + " pixels"
                self.draw_text(x_str, 'black', (x, y+20), font, justification )
    
 