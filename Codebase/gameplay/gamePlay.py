""" April 16, 2024 -- created this to shift my main activities into a separate module with Class(es)  
"""

import pygame
from pygame.locals import *
import math

from _ball.ball2 import Ball
from _runningMen.fielders import Fielder
from _runningMen.baserunners import Baserunner


from gameplay.gamePlay_helpers import GameplayHelpers
from gameplay.interpret_situation import InterpretSituation


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
        self.gp_helpers = GameplayHelpers(screen)
        self.interpret_situation = InterpretSituation()

        self.screen = screen

        ### Data ### 

        for game_objects in range(1):

            self.fielder_objects = self.gp_helpers.make_fielders(Fielder) 
            self.baserunners = self.gp_helpers.make_baserunners(Baserunner) 
            self.throw_receiver = None
            self.keyboard_arrow_input = [False, False, False, False] #left, right, north, south

        for tracers in range(1):
            
            self.curr_defensive_play_ID = 0
            self.current_defensiveSit_text = ""
            self.base_attained_text = ""
            self.ball_direction_text = ""
            self.ball_depth_text = ""
            self.throw_receiver_id_text = ""
            self.fielder_with_ball_text = ""
        
        for situation_control in range(1):    
            self.situation_start_toggle = False
            
        for ball_control in range(1):
            ## General
            self.ball_coord_2D_pg = None

            ## Throw
            self.throw_toggle = False

            ## Ball exchange
            self.ball_exchange_toggle = False
            self.ball_catch_timeStamp = 0
            self.EXCHANGE_DURATION = 0.5 * 1000 ## 0.5 seconds delay from receiving a ball to being ready to throw it
            
            ## Ball location 
            self.ball_depth_index = 0
            self.mouse_drag_ball_toggle = False

        for ball_related in range(1):
            self.curr_fielder_with_ball = None
            self.prev_fielder_with_ball = None


    """ ***** FUNCTIONS ***** """


    def master_gameplay_control(self):
        
        self.master_updates_and_gets()

        self.start_situation()

        ## Fielders and baserunners
        self.update_man_collisions()
        self.move_and_draw_fielders()
        self.move_and_draw_baserunners()
        
        ## Ball
        self.update_ball_exchange()
        self.move_ball_with_fielder()
        self.move_ball()
        self.ball.draw_ball()

        self.data_to_printScreen()
            
    
    """ The whole gain situation initialization could be pushed down a level """
    
    for do_game_situation in range(1): 
    
        def start_situation(self):
            
            if not self.situation_start_toggle:
                return
            
            if self.curr_defensive_play_ID not in self.setup.defensive_plays:
                return 
    
            defensive_assignments = self.setup.defensive_plays[self.curr_defensive_play_ID]
            self.give_primary_defensive_assignments(defensive_assignments)  
            self.give_secondary_defensive_assignments(defensive_assignments)  ## Assign goals to the other 7 defensive players
          
            self.situation_start_toggle = False


        def give_primary_defensive_assignments(self, defensive_assignments):
            
            
            ## For now, do in reverse -- place the ball relative to the guy assigned to field it 
            ball_new_coord = self.meta_place_ball_for_situation(defensive_assignments)
            backup_coord = ( ball_new_coord[0] - 70, ball_new_coord[1] - 70 )
            
            ## Assign 1 fielder to field the ball (#1), and 1 backup (#2)
            self.fielder_objects[ defensive_assignments.index(1) ].assign_goal(ball_new_coord)
            self.fielder_objects[ defensive_assignments.index(2) ].assign_goal(backup_coord)


        def give_secondary_defensive_assignments(self, defensive_assignments):
            for fielder_id, fielder_positioning_id in enumerate(defensive_assignments): 
            
                if fielder_positioning_id not in [1, 2] and isinstance(fielder_positioning_id, int): # In defensive_assignments, index 0 is a text description of the baseball situation  
                        
                    ## Assign each fielder coordinates representing standard positioning for this baseball situation
                    fielder_goal = self.setup.defensiveSit_fielder_coord[fielder_positioning_id]
                    self.fielder_objects[fielder_id].assign_goal(fielder_goal)  


        ## Called from start_situation()
        def meta_place_ball_for_situation(self, defensive_assignments): 
            
            primary_fielder = defensive_assignments.index(1)
            x, y = self.setup.fielder_standard_coord[primary_fielder]
            ball_new_coord = (x - 150, y - 150)
            
            self.ball.update_coord_for_situation(ball_new_coord)
            
            return ball_new_coord


    #### Ball Functions: Ball movement | Ball launch and drop ball
    for update_ball in range(1):

        ### Ball movement

        def move_ball(self):
            
            if self.mouse_drag_ball_toggle:
                self.curr_fielder_with_ball = None
                self.prev_fielder_with_ball = None
                self.ball.end_launch()
                self.ball.mouse_drag_ball()
                
            else:
                self.ball.move_ball()


        def move_ball_with_fielder(self):
            
            if not self.curr_fielder_with_ball:
                return 

            ## Get coord from fielder, send to ball
            fielder_centre_coord = self.curr_fielder_with_ball.get_centre_coord()
            self.ball.update_coord_for_situation( fielder_centre_coord )


        ## Throws -- called whenever the throw receiver changes
        def send_throw_data_to_ball(self, direction_deg):
            
            throw_velo_mph = 65
            launch_angle_deg = 12
            
            throw_metrics = {
                "exit_velo": throw_velo_mph,
                "launch_angle": launch_angle_deg,
                "launch_direction": direction_deg,
                    }
            
            self.ball.receive_throw_data(throw_metrics)


    # Ball throwing 
    for throwing in range(1):

        ## Called from 'master functional control'    
        def update_ball_exchange(self):
            
            if not self.ball_exchange_toggle:
                return
                
            time_since_catch = pygame.time.get_ticks() - self.ball_catch_timeStamp
            
            if time_since_catch >= self.EXCHANGE_DURATION:
                self.ball_exchange_toggle = False
                
                if self.curr_fielder_with_ball:
                    self.curr_fielder_with_ball.update_ball_possession(True, False)  ## Possession = True, Exchange = False 


        def change_throw_receiver(self):
            
            if not self.curr_fielder_with_ball:
                return
            
            ## If there isn't one, pick the best one
            if not self.throw_receiver:
                self.new_throw_receiver(4) # Default to 4 / second baseman 

            else:
                self.throw_receiver.update_throw_receiver(False) # Cancel the current receiver's status
                
                receiver_id = self.throw_receiver.get_id() + 1

                if receiver_id > 9:
                    receiver_id = 1

                self.new_throw_receiver(receiver_id)


        def new_throw_receiver(self, receiver_id):
            self.throw_receiver = self.fielder_objects[receiver_id]
            self.throw_receiver.update_throw_receiver(True)
            
            theta = self.gp_helpers.get_throw_theta(self.curr_fielder_with_ball, self.throw_receiver)
            self.send_throw_data_to_ball(theta)
            

    #### Man Functions
    for update_fielders_and_baserunners in range(1):

        ### Man collisions with bases, ball (and each other ... TBD)  
        def update_man_collisions(self):
            
            for fielder in self.fielder_objects.values():
                fielder.check_base_collision()                            
                self.check_fielder_gets_ball(fielder)
                
            self.baserunners.detect_collisions(self.fielder_objects)

        
        ## Check if each fielder has just fielded or caught a batted or thrown ball 
        def check_fielder_gets_ball(self, fielder):
            
            ## Check that a catch is possible
            distance_pg = self.helpers.measure_distance_in_pixels( fielder.get_centre_coord(), self.ball_coord_2D_pg )
            
            if distance_pg > self.setup.ball_catch_proximity: # xy axes
                return
            
            if self.ball.get_curr_height_feet() > 7: # z axis  
                return 
            
            if self.curr_fielder_with_ball: # Don't catch a ball if someone already possess it (e.g., 2 fielders cross paths)
                return
            
            if fielder == self.prev_fielder_with_ball: # Prevent a ball being caught by the thrower a milisecond after release 
                return
            
            self.assign_ball_to_fielder(fielder)
            
        
        def assign_ball_to_fielder(self, fielder):
            
            ## The ball is caught / fielded        
            self.curr_fielder_with_ball = fielder
            self.prev_fielder_with_ball = fielder
            
            # Exchange
            self.ball_exchange_toggle = True  # Start ball exchange
            self.ball_catch_timeStamp = pygame.time.get_ticks() 
            
            # Objects
            self.ball.end_launch()
            self.curr_fielder_with_ball.update_ball_possession(True, True) # possession = True, exchange = True
            
            ## Throw related
            self.throw_toggle = False

            if self.throw_receiver:
                self.throw_receiver.update_throw_receiver(False) ## NON FUNCTIONAL / CHANGE COLOUR
                self.throw_receiver = None


        ### Move and draw 'men' ### 
        
        def move_and_draw_fielders(self):
            
            for fielder in self.fielder_objects.values():
                fielder.goal_move() 
                
                if not fielder.get_goal():
                    fielder.move_man(self.keyboard_arrow_input) ## This overrides the goal-setting animation unless only called when no goal 
                
                fielder.draw_man()
   
   
        def move_and_draw_baserunners(self): 
            self.baserunners.move_baserunner() 
            self.baserunners.draw_man()


    for pass_throughs in range(1):
        """ ********************************
        BELOW ARE FUNCTIONS CALLED FROM MAIN 
        OR THAT CALL BALL, FIELDER OR BASERUNNER -- 
        LOW OR NO INTERDEPENDENCY WITH GAMEPLAY
        ******************************** """

        ### Other gets / updates 
        for gets in range(1):
            
            def master_updates_and_gets(self):
                
                self.ball_coord_2D_pg = self.ball.get_ball_coord_2D_pg()  ## Do this first
                
                ## Ball
                self.ball_direction_text = self.interpret_situation.get_ball_direction( self.ball_coord_2D_pg ) ## This is both the functional direction and the tracer
                self.ball_depth_int = self.interpret_situation.get_ball_depth( self.ball_coord_2D_pg ) ## This is just the functional depth 


        for actions_called_by_main in range(1):
            
            ## Called from Main > Get Events 
            def throw_ball(self):
                
                if self.ball_exchange_toggle:
                    return
                
                if not self.curr_fielder_with_ball:
                    return
                
                ## We're throwing the ball
                else:
                    if not self.throw_receiver:
                        self.change_throw_receiver()

                    self.throw_toggle = True
                    self.curr_fielder_with_ball.update_ball_possession(False, False)
                    self.curr_fielder_with_ball = None ## Prev_fielder_with_ball remains 
                    self.ball.thrown_launch()
                

            # Called from Main > Get Events 
            def batted_launch(self):
                self.curr_fielder_with_ball = None
                self.ball.batted_launch()
                
            
            ## Called from Main > Get Events 
            def drop_ball(self):
                if self.curr_fielder_with_ball:
                    self.curr_fielder_with_ball = None
                    self.prev_fielder_with_ball = None
                    self.ball.fielder_drop_the_ball()


            ## Called from main -- hit L to reset the situation
            def reset_play(self):
                self.fielder_objects = self.gp_helpers.make_fielders(Fielder) # 1-9  
                self.ball.reset_play()
                #self.baserunners = self.make_baserunners() # THIS WOULD PRODUCE AN ERROR IF IT WAS CALLED


        for updates_from_main in range(1):

            ## Called from main --> passing keyboard input to make it functional here
            def packaged_updates(self, keyboard_input, mouse_drag_ball_toggle):
                self.keyboard_arrow_input = keyboard_input 
                self.mouse_drag_ball_toggle = mouse_drag_ball_toggle

            ## Pass-through from main > get events 
            def send_launch_deltas_to_ball(self, launch_metrics_deltas):
                self.ball.receive_launch_deltas(launch_metrics_deltas)

            ## Called from main  
            def update_curr_defensiveSit(self, newSit):    
                self.curr_defensive_play_ID = newSit 

            ## Called from main --> passes bool
            def update_situation_start(self, bool_):
                self.situation_start_toggle = bool_
            
            ## Called from main 
            def advance_baserunner(self):
                self.baserunners.assign_goal()


    for send_data_to_printScreen in range(1):

        def data_to_printScreen(self):

            self.prep_screen_data()

            general_screen_text = {
                "defensive_sit": self.curr_defensive_play_ID,
                "defensive_sit_text": self.current_defensiveSit_text,
                "base_attained": self.base_attained_text,
                "ball_loc_field": self.ball_direction_text,
                "ball_depth":  self.ball_depth_text,
                "fielder with ball": self.fielder_with_ball_text,
                "throw receiver": self.throw_receiver_id_text
            }

            ball_metrics_screen_text, ball_launch_data_text = self.ball.package_data_objects()

            self.screenPrinter.write_text_onScreen(general_screen_text, ball_metrics_screen_text, ball_launch_data_text)


        def prep_screen_data(self):
            
            if self.curr_defensive_play_ID in self.setup.defensive_plays:
                self.current_defensiveSit_text = self.setup.defensive_plays[self.curr_defensive_play_ID][0]

            """ Each of these three could be pushed down a level """

            ## Get the ID of the player with the ball (if any)
            if self.curr_fielder_with_ball:
                self.fielder_with_ball_text = self.curr_fielder_with_ball.get_id()
            
            else:
                self.fielder_with_ball_text = None

            ## Throw target (if any)
            if not self.throw_receiver:
                self.throw_receiver_id_text = None

            else:
                self.throw_receiver_id_text = self.throw_receiver.get_id()

            ## Highest base attained
            base_attained = self.baserunners.get_base_attained()        

            if base_attained > 0:
                self.base_attained_text = str(base_attained) + "B" 

            else:
                self.base_attained_text = "None"

            self.ball_depth_text = self.interpret_situation.ball_depth_index[self.ball_depth_int]


# Last line