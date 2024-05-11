""" April 16, 2024 -- created this to shift my main activities into a separate module with Class(es)  
"""

import pygame
from pygame.locals import *
import math

from _ball.ball2 import Ball
from _runningMen.fielders import Fielder
from _runningMen.baserunners import Baserunner

from setup import Setup
from helpers import Helpers
from screen_printer import ScreenPrinter
from gamePlay_helpers import GameplayHelpers

pygame.init()


class GamePlay:
    
    def __init__(self, screen):
        
        self.ball = Ball(screen)
        
        self.setup = Setup()
        self.helpers = Helpers()
        self.screenPrinter = ScreenPrinter(screen)
        self.gp_helpers = GameplayHelpers(screen)

        self.screen = screen

        ### Data ### 

        for game_objects in range(1):

            self.fielder_objects = self.gp_helpers.make_fielders(Fielder) 
            self.baserunner = self.gp_helpers.make_baserunners(Baserunner) 
            self.bases_attained = {1: False, 2: False, 3: False, 4: False}
        
        for game_status_and_toggles in range(1):
            self.curr_defensive_play_ID = 0
            self.current_defensiveSit_text = ""
            self.base_attained_text = ""
            self.ball_location_text = ""
            
            self.situation_start_toggle = False
            self.situation_live_ball_toggle = False ## Only True from batted ball to end of play 

        for ball_related in range(1):
            self.prev_ticks = 0         
            self.fielder_with_ball = None
            

    for do_game_situation in range(1):
                
        def master_situation_control(self, left, right, north, south, mouse_drag_ball_toggle):
            
            if self.situation_start_toggle:
                if self.curr_defensive_play_ID in self.setup.defensive_plays:
                    self.start_situation()

            self.update_man_collisions()
            self.move_and_draw_fielders(left, right, north, south)
            self.move_and_draw_baserunners()
            
            self.move_ball_with_fielder_if()
            self.move_ball(mouse_drag_ball_toggle)
            self.ball.draw_ball()

            self.data_to_printScreen()
        
    
        def start_situation(self):  

            defensive_assignments = self.setup.defensive_plays[self.curr_defensive_play_ID]
            
            self.assign_primary_backup_fielders(defensive_assignments)

            ## Assign goals to the other 7 defensive players
            for fielder_id, fielder_positioning_id in enumerate(defensive_assignments): #[1:]
                
                #fielder_id # to match defensive_assignments, where index pos 1-9 = f1, f2, etc. 
                
                if fielder_positioning_id not in [1, 2] and isinstance(fielder_positioning_id, int): # In defensive_assignments, index 0 is a text description of the baseball situation  
                        
                    ## Assign each fielder coordinates representing standard positioning or this baseball situation
                    fielder_goal = self.setup.defensiveSit_fielder_coord[fielder_positioning_id]
                    self.fielder_objects[fielder_id].assign_goal(fielder_goal)  # +1 
        
            self.situation_start_toggle = False


        def assign_primary_backup_fielders(self, defensive_assignments):
            
            ## For now, do in reverse -- place the ball relative to the guy assigned to field it 
            ball_new_coord = self.meta_place_ball_for_situation(defensive_assignments)
            backup_coord = ( ball_new_coord[0] - 70, ball_new_coord[1] - 70 )
            
            ## Assign 1 fielder to field the ball (#1), and 1 backup (#2)
            self.fielder_objects[ defensive_assignments.index(1) ].assign_goal(ball_new_coord)
            self.fielder_objects[ defensive_assignments.index(2) ].assign_goal(backup_coord)
        

        ## Called from start_situation()
        def meta_place_ball_for_situation(self, defensive_assignments): 
            
            primary_fielder = defensive_assignments.index(1)
            x, y = self.setup.fielder_standard_coord[primary_fielder]
            ball_new_coord = (x - 150, y - 150)
            
            self.ball.update_coord_for_situation(ball_new_coord)
            
            return ball_new_coord


        for litte_situation_updates in range(1):

            def reset_play(self):
                self.reset_fielders()
                self.ball.reset_play()
        
            def reset_fielders(self):
                self.fielder_objects = self.gp_helpers.make_fielders(Fielder) # 1-9  
                
            def reset_baserunners(self):
                self.baserunner = self.make_baserunners()


    #### Ball Functions 
    # Ball movement | Ball launch and drop ball
    
    for update_ball in range(1):

        ### Ball movement
         
        def move_ball(self, mouse_drag_ball_toggle):
            
            if mouse_drag_ball_toggle:
                self.fielder_with_ball = None
                self.ball.end_launch()
                self.ball.mouse_drag_ball()
                
            else:
                self.ball.move_ball()
        
        
        def move_ball_with_fielder_if(self):
        
            if self.fielder_with_ball:   
                x, y = self.fielder_with_ball.agnostic_pos
                self.ball.update_coord_for_situation( (x, y) )
                
                
        ### Ball launch and drop ball

        ## Pass-through from main > get events 
        def send_launch_data_to_ball(self, launch_metrics_deltas):
            self.ball.receive_launch_data(launch_metrics_deltas)


        # Pass-through from main > get events 
        def launch_ball(self):
            self.fielder_with_ball = None
            self.ball.launch_ball()
            
        
        ## Called directly from main > get events 
        def drop_ball(self):
            if self.fielder_with_ball:
                self.fielder_with_ball = None
                self.ball.fielder_drop_the_ball()


    #### Man Functions
    for update_fielders_and_baserunners in range(1):

        ### Man collisions with bases, ball (and each other ... TBD)  
        
        def update_man_collisions(self):

            for fielder in self.fielder_objects.values():
                fielder.check_base_collision()
                
                if self.ball.curr_height_feet < 7 and not self.fielder_with_ball:
                    self.check_fielder_gets_ball(fielder)
                
            self.baserunner.detect_collisions(self.fielder_objects)

    
        ## Check if each fielder has just fielded or caught a batted or thrown ball 
        def check_fielder_gets_ball(self, fielder):
 
            distance_pg = self.helpers.measure_distance_in_pixels( fielder.get_centre_coord(), self.get_ball_coord() )
            
            if distance_pg < self.setup.ball_catch_proximity:
                self.fielder_with_ball = fielder
                self.ball.end_launch()

        ### Move and draw 'men'
        
        def move_and_draw_fielders(self, left, right, north, south):
            for fielder in self.fielder_objects.values():
                fielder.goal_move()
                
                if not fielder.get_goal(): 
                    fielder.move_man(left, right, north, south) ## This overrides the goal-setting animation unless only called when no goal 
                
                #fielder.draw_fielder()
                fielder.draw_man()
   
   
        def move_and_draw_baserunners(self): # left, right, north, south
            self.baserunner.move_baserunner() 
            #self.baserunner.draw_baserunner()
            self.baserunner.draw_man()


    ### Other gets / updates 
    for gets_and_updates in range(1):

        ## Called from main --> passing keyboard input to make it functional here
        def update_curr_defensiveSit(self, newSit):    
            self.curr_defensive_play_ID = newSit 

        ## Called from main --> passes bool
        def update_situation_start(self, bool_):
            self.situation_start_toggle = bool_
            self.situation_live_ball_toggle = bool_
        
        ## Called from main 
        def advance_baserunner(self):
            self.baserunner.assign_goal()

        def get_ball_coord(self):
            return self.ball.coord_2D_pg


    for send_data_to_printScreen in range(1):
        
        def data_to_printScreen(self):
            
            self.prep_screen_data()
            
            general_screen_text = {
                "defensive_sit": self.curr_defensive_play_ID,
                "defensive_sit_text": self.current_defensiveSit_text,
                "base_attained": self.base_attained_text,
                "ball_loc_field": self.ball_location_text,
            }
            
            ball_metrics_screen_text = self.ball.package_data_objects()
             
            ball_inputs_screen_text = {
                "exit_velo": self.ball.launch_velo_mph,
                "launch_angle": self.ball.launch_angle_deg,
                "launch_direction": self.ball.launch_direction_deg,        
            }
            
            self.screenPrinter.write_text_onScreen(general_screen_text, ball_metrics_screen_text, ball_inputs_screen_text)
            

        def prep_screen_data(self):
            if self.curr_defensive_play_ID in self.setup.defensive_plays:
                self.current_defensiveSit_text = self.setup.defensive_plays[self.curr_defensive_play_ID][0]
        
            base_attained = self.baserunner.get_base_attained()        
            if base_attained > 0:
                self.base_attained_text = str(base_attained) + "B" 
                
            self.ball_location_text = self.gp_helpers.interpret_ball_location( self.get_ball_coord() )


# Last line