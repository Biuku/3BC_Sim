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

pygame.init()


class GamePlay:
    
    def __init__(self, screen):
        
        self.ball = Ball(screen)
        
        self.setup = Setup()
        self.helpers = Helpers()
        self.screenPrinter = ScreenPrinter(screen)

        self.screen = screen

        ### Data ### 

        for game_objects in range(1):

            # Fielders and baserunners
            self.fielder_objects = self.make_fielders() #None # Placeholder
            self.baserunner = self.make_baserunners() #None # Placeholder
            self.bases_attained = {1: False, 2: False, 3: False, 4: False}
        
        for game_status in range(1):
            ## Game status 
            self.curr_defensiveSit = 0
            self.current_defensiveSit_text = ""
            self.base_attained_text = ""
            self.ball_location_text = ""

            #self.num_keys = [False] * 10 ## Keep track of multiple num keys pressed above the kb
            
            # Toggles
            self.situation_start_toggle = False
            self.situation_live_ball_toggle = False ## Only True from batted ball to end of play 
            
            self.drop_ball_prev_ticks = 0
        

        for ball_related in range(1):
            self.prev_ticks = 0         
            self.fielder_with_ball = None
            

    for do_game_situation in range(1):
                
        def master_situation_control(self, left, right, north, south, mouse_drag_ball_toggle):
            
            self.start_situation()
            self.interpret_ball_location()
            self.move_ball_with_fielder()
            self.check_ball_catch()

            self.update_man_collisions()
            self.move_and_draw_fielders(left, right, north, south)
            self.move_and_draw_baserunners()

            self.move_ball(mouse_drag_ball_toggle)

            self.data_to_printScreen()
        
    
        def start_situation(self):  

            if self.situation_start_toggle and self.curr_defensiveSit in self.setup.defensiveSit_plays:
                    
                defensiveSit_play = self.setup.defensiveSit_plays[self.curr_defensiveSit]
                
                # Place the ball for the current situation (for now) 
                ball_new_coord = self.meta_place_ball_for_situation()
            
                ## Assign goals to all 9 defensive players
                for fielder_id, fielder_action_id in enumerate(defensiveSit_play[1:]):
                    fielder_id += 1 
                    
                    ## Assign fielders who will field the ball and back-up that fielder
                    if fielder_action_id == 1:
                        self.fielder_objects[fielder_id].assign_goal(ball_new_coord)
                    
                    elif fielder_action_id == 2:
                        backup_coord = (ball_new_coord[0]-70, ball_new_coord[1]-70)
                        self.fielder_objects[fielder_id].assign_goal(backup_coord)
                        
                    ## Assign standard position for this baseball situation
                    else:
                        fielder_goal = self.setup.defensiveSit_fielder_coord[fielder_action_id]
                        self.fielder_objects[fielder_id].assign_goal(fielder_goal)   
            
            self.situation_start_toggle = False


        def interpret_ball_location(self):
    
            # Get ball coord
            ball_coord = self.get_ball_coord()
            centroid = self.setup.boundaries['four_B_tip'] 
            
            # Get theta of ball
            ball_theta_rad = self.helpers.coord_to_theta(centroid, ball_coord)
            ball_theta_deg = math.degrees(ball_theta_rad)
            
            # if theta is... 
            ball_loc = None
            
            if ball_theta_deg > self.setup.boundary_thetas['lf_foulPole_deg']:
                ball_loc = "Foul: left side"
            
            elif ball_theta_deg > self.setup.boundary_thetas['cf_left_deg']:
                ball_loc = "Left field"
                
            elif ball_theta_deg > self.setup.boundary_thetas['cf_right_deg']:
                ball_loc = "Centre field"
                
            elif ball_theta_deg > self.setup.boundary_thetas['rf_foulPole_deg']:
                ball_loc = "Right field"
                
            else:
                ball_loc = "Foul: right side"

            self.ball_location_text = ball_loc

        ## Called from start_situation()
        def meta_place_ball_for_situation(self): 
            if self.situation_start_toggle:
                if self.curr_defensiveSit in self.setup.defensiveSit_plays:
                
                    defensiveSit_play = self.setup.defensiveSit_plays[self.curr_defensiveSit]
                    
                    ## For now, find the guy fielding the ball and place the ball relative to him
                    for fielder_id, role in enumerate(defensiveSit_play[1:]):
                            
                        if role == 1:
                            fielder_id += 1 
                            fielder_coord = self.setup.fielder_standard_coord[fielder_id]  # pass 'f1', 'f2' etc. to get standard pos
                            
                            ball_new_coord = (fielder_coord[0] - 150, fielder_coord[1] - 150)
                            
                            self.ball.update_coord_for_situation(ball_new_coord)
                            
                            return ball_new_coord
                        

    def check_ball_catch(self):
        
        if self.ball.curr_height_feet > 7:
            return
        
        if not self.fielder_with_ball: # and self.ball.launched_toggle:
            ball_coord = self.get_ball_coord()
            proximity_threshold_pg = self.setup.ball_pickup_proximity_threshold_pg
            
            for fielder in self.fielder_objects.values():
        
                if fielder.check_ball_proximity_2D(ball_coord, proximity_threshold_pg):
                    
                    self.fielder_with_ball = fielder
                    self.ball.end_launch()
                    self.ball.update_possession(True)
                    print(f"Found a fielder: {fielder.man_id}")


    def move_ball_with_fielder(self):
       if self.fielder_with_ball:
           
           x, y = self.fielder_with_ball.agnostic_pos
           #x -= 0
           #y += 10
           
           self.ball.update_coord_for_situation( (x, y) )


    ### Ball Functions 
    for ball_stuff in range(1):

        def move_ball(self, mouse_drag_ball_toggle):
            
            if mouse_drag_ball_toggle:
                self.fielder_with_ball = None
                self.ball.end_launch()
                self.ball.mouse_drag_ball()
                
            self.ball.move_ball()
        
        
        def launch_ball(self):
            self.fielder_with_ball = None
            self.ball.launch_ball()
            
            
        ## User updates the variables affecting the launch
        def update_user_input(self, launch_metrics):
            self.ball.receive_user_input(launch_metrics)
            return
        
            ticks = pygame.time.get_ticks()  ## Number of miliseconds since pygame.init() called
            if ticks - self.prev_ticks > 30:  ## 0.04 seconds delay between updates
                self.prev_ticks = ticks
                
                self.ball.launch_velo_mph += launch_metrics['exit_velo']
                self.ball.launch_angle_deg += launch_metrics['launch_angle']
                self.ball.launch_direction_deg += launch_metrics['launch_direction']


    ### Man Functions
    for fielders_and_baserunners in range(1):
        
        def update_man_collisions(self):
        
            for fielder in self.fielder_objects.values():
                fielder.check_base_collision(self.setup.base_rects)
                
            self.baserunner.detect_collisions(self.setup.base_rects, self.fielder_objects)
    
    
        def move_and_draw_fielders(self, left, right, north, south):
            for fielder in self.fielder_objects.values():
                fielder.goal_move()
                
                if not( fielder.get_goal() ): 
                    fielder.move_man(left, right, north, south) ## This overwrites the goal-setting animation unless only called when no goal        
                
                fielder.draw_fielder()
        
        
        def move_and_draw_baserunners(self): # left, right, north, south
            self.baserunner.move_baserunner() 
            self.baserunner.draw_baserunner()
            
            
        def drop_ball(self):
            if self.fielder_with_ball:
                self.fielder_with_ball = None
                self.ball.fielder_drop_the_ball()
   

    ### Other gets / updates 
    for updateValueGetValue in range(1):
        
        def reset_play(self):
            self.reset_fielders()
            self.ball.reset_play()
    
        def reset_fielders(self):
            self.fielder_objects = self.make_fielders()  # 1-9
            
        def reset_baserunners(self):
            self.baserunner = self.make_baserunners()
                                
        ## Called from main --> passing keyboard input to make it functional here
        def update_curr_defensiveSit(self, newSit):    
            self.curr_defensiveSit = newSit 
            
        def update_situation_start(self, bool_):
            self.situation_start_toggle = bool_
            self.situation_live_ball_toggle = bool_
            
        def advance_baserunner(self):
            self.baserunner.assign_goal()

        def get_ball_coord(self):
            return self.ball.coord_2D_pg


    """ !!! YES -- COULD BE MOVED TO A COMPOSITION CLASS """
    ### Instantiate fielders and baserunners
    for make_running_men in range(1):
        
    ## Create 9 instances of 'Man' object and return in a dict with keys as integers 1 to 9 
        def make_fielders(self):

            fielder_objects = {}
            
            for fielder_id in [x for x in range(1, 10)]:
                pos = self.setup.fielder_standard_coord[fielder_id]                
                fielder_objects[fielder_id] = Fielder(self.screen, pos, fielder_id)
                
            return fielder_objects
        
        
        def make_baserunners(self):
            return Baserunner(self.screen)
           
    
    """ !!! PRINTSCREEN STUFF COULD BE MOVED TO INHERETED CLASS... BUT THAT MAY BE WORSE... IT'S NON-FUNCTIONAL AND OUT OF THE WAY... LEAVE IT... """    
    for send_data_to_printScreen in range(1):
        
        def data_to_printScreen(self):
            
            self.prep_screen_data()
            
            general_screen_text = {
                "defensive_sit": self.curr_defensiveSit,
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
            if self.curr_defensiveSit in self.setup.defensiveSit_plays:
                self.current_defensiveSit_text = self.setup.defensiveSit_plays[self.curr_defensiveSit][0]
        
            base_attained = self.baserunner.get_base_attained()        
            if base_attained > 0:
                self.base_attained_text = str(base_attained) + "B" 


# Last line