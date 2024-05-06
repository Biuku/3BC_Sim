""" April 16, 2024 -- created this to shift my main activities into a separate module with Class(es)  

"""

import pygame
from pygame.locals import *
import math

from setup import Setup
from ball2 import Ball
from helpers import Helpers
from helpers import ScreenPrinter

##### ***** INITIALIZE PYGAME ***** #####

pygame.init()


class GamePlay:
    
    def __init__(self, screen, w, h, fps, user_interface_start_x):
        
        self.screen = screen

        self.setup = Setup(screen, w, h)
        self.ball = Ball(screen, w, h, fps, user_interface_start_x)
        self.helper = Helpers(screen)
        self.screenPrinter = ScreenPrinter(screen, user_interface_start_x)

        ### Data ### 
        for coordinates in range(1):
            self.boundary_coords = self.setup.get_boundaries()  # lf_corner, cf_wall, rf_corner, four_B_tip
            self.boundary_thetas = self.setup.get_boundary_thetas()
                    
            self.base_centroids = self.setup.base_centroids  # one_B, two_B, three_B, four_B, rubber_P
            self.fielder_standard_coord = self.setup.get_fielder_standard_coord(self.base_centroids) # Standard fielder pre-pitch coordinates: 1-9
            self.defensiveSit_fielder_coord = self.setup.get_defensiveSit_fielder_coord(self.base_centroids)
        
        for game_objects in range(1):
            ## Collections of game-play objects
            self.base_rects = self.setup.make_bases(self.base_centroids) # Dict of base rects -- collision objects
            self.defensiveSit_plays = self.setup.get_defensiveSit_plays()
            
            # Fielders and baserunners
            self.fielder_objects = self.setup.make_fielders(self.fielder_standard_coord, self.screen) #None # Placeholder
            self.baserunner = self.setup.make_baserunners(self.screen) #None # Placeholder
            self.bases_attained = {1: False, 2: False, 3: False, 4: False}
        
        for game_status in range(1):
            ## Game status 
            self.curr_defensiveSit = 0
            self.current_defensiveSit_text = ""
            self.base_attained_text = ""
            self.ball_location_text = ""
            self.num_keys = [False] * 10 ## Keep track of multiple num keys pressed above the kb
        
        for ball_related in range(1):
            self.launch_velo_increment = False
            self.launch_velo_decrement = False
            self.launch_angle_increment = False
            self.launch_angle_decrement = False
            self.launch_direction_increment = False
            self.launch_direction_decrement = False
            self.prev_ticks = 0
            
        #Toggles
        self.situation_start = False
        
        ## On-screen instructions
        self.instructions_x = self.instructions_master_x = 1400
        self.instructions_y = self.instructions_master_y = 850


    ### Game situation function
    def do_situation(self): #curr_defensiveSit, defensiveSit_plays, defensiveSit_fielder_coord, situation_start, ball_coord        

        if self.situation_start:

            if self.curr_defensiveSit in self.defensiveSit_plays:
                
                # For now, set the ball's coord relative to the active fielder's coord
                ball_coord = self.set_ball_coord()
                self.ball.master_x, self.ball.master_y = ball_coord

                """ BALL ^^^^^^^^^^^^ BALL """
                
                defensiveSit_play = self.defensiveSit_plays[self.curr_defensiveSit]
            
                ## Assign goals to all 9 defensive players. This requires ball_coord
                for fielder_id, fielder_action_id in enumerate(defensiveSit_play[1:]):
                    fielder_id += 1 
                    
                    if fielder_action_id == 1:
                        self.fielder_objects[fielder_id].assign_goal(ball_coord)
                    
                    elif fielder_action_id == 2:
                        backup_coord = (ball_coord[0]-70, ball_coord[1]-70)
                        self.fielder_objects[fielder_id].assign_goal(backup_coord)
                        
                    else:
                        fielder_goal = self.defensiveSit_fielder_coord[fielder_action_id]
                        self.fielder_objects[fielder_id].assign_goal(fielder_goal)   
        
        # Reset initiation of a new situation
        self.situation_start = False


    ### Ball Functions 
    for ball in range(1):
        
        def set_ball_coord(self): #curr_defensiveSit, defensiveSit_plays, fielder_standard_coord, ball_coord
            if self.situation_start:
                if self.curr_defensiveSit in self.defensiveSit_plays:
                
                    defensiveSit_play = self.defensiveSit_plays[self.curr_defensiveSit]
                    
                    ## For now, find the guy fielding the ball and place the ball relative to him
                    for fielder_id, role in enumerate(defensiveSit_play[1:]):
                            
                        if role == 1:
                            fielder_id += 1 
                            fielder_coord = self.fielder_standard_coord[fielder_id]  # pass 'f1', 'f2' etc. to get standard pos
                            
                            new_ball_coord = (fielder_coord[0] - 150, fielder_coord[1] - 150)
                            self.ball.update_coord_for_situation(new_ball_coord) ## INTEGRATED - DONE
                            
                            return new_ball_coord[0], new_ball_coord[1]
                        

        def move_ball(self, mouse_drag_ball_toggle):
            if mouse_drag_ball_toggle:
                self.ball.end_launch()
                self.ball.mouse_drag_ball()
                
            self.ball.move_ball()
        
        
        def launch_ball(self):
            self.ball.launch_ball()
            

        def update_ball_height(self, dz):
            self.ball.master_z += dz


        ## User updates the variables affecting the launch
        def update_launch_properties(self):
            ticks = pygame.time.get_ticks()  ## Number of miliseconds since pygame.init() called
            if ticks - self.prev_ticks > 40:  ## 0.04 seconds delay between updates
                self.prev_ticks = ticks
            
                if self.launch_angle_increment:
                    self.ball.launch_angle_deg += 1
                if self.launch_angle_decrement:
                    self.ball.launch_angle_deg -= 1
                    
                if self.launch_velo_increment:
                    self.ball.launch_velo_mph += 1
                if self.launch_velo_decrement:
                    self.ball.launch_velo_mph -= 1
                    
                if self.launch_direction_increment:
                    self.ball.launch_direction_deg += 2          
                if self.launch_direction_decrement:
                    self.ball.launch_direction_deg -= 2


        def get_ball_coord(self):
            return self.ball.coord_2D_pg

    ### Man Functions
    for fielders_and_baserunners in range(1):
    
        def move_fielders(self, left, right, north, south):
            for fielder in self.fielder_objects.values():
                fielder.goal_move()
                
                if not( fielder.get_goal() ): 
                    fielder.move_man(left, right, north, south) ## This overwrites the goal-setting animation unless only called when no goal
                fielder.detect_collisions(self.base_rects)
                
                #fielder.draw_fielder()
        
        
        def move_baserunners(self, left, right, north, south):
            self.baserunner.move_baserunner(left, right, north, south)
            
            self.baserunner.detect_collisions(self.base_rects, self.fielder_objects)
            
            #self.baserunner.draw_baserunner()
            
            
        def draw_players(self):
            self.baserunner.draw_baserunner()
            
            for fielder in self.fielder_objects.values():
                fielder.draw_fielder()
            
    
    ## Let user choose a defensive situation -- for testing during code build 
        def choose_situation(self): #curr_defensiveSit, num_keys, defensiveSit_plays
                
            ## Let the user enter 2 digits
            for i, val in enumerate(self.num_keys):
                if val:
                    if self.curr_defensiveSit == 0: 
                        self.curr_defensiveSit = i
                    
                    elif self.curr_defensiveSit < 10: 
                        self.curr_defensiveSit =  self.curr_defensiveSit * 10 + i # Tens
                        
                    ## else you're trying to add a third digit after reaching a 2 digit # 
                    else:
                        self.curr_defensiveSit = i ## Roll over if you tried entering too high a 
            
            self.reset_numkeys()


    ### Print to screen ###
    for printScreen_false_loop in range(1):
        
        """ ANGRYBATS PRINTSCREEN FUNCTIONS """
        def write_text_onScreen(self):
            
            ### PREP
            self.prep_screen_data()
            self.screenPrinter.draw_demarcation_line()
            self.screenPrinter.new_frame() ## Reset y for start row of printing on screen


            ### STATIC INSTRUCTIONS
            self.screenPrinter.print_simple( ["INSTRUCTIONS", "", ""] )
            self.screenPrinter.print_simple( ["Press 'b' to show Boundary Markers", "", ""] )
            self.screenPrinter.print_simple( ["Press 't' to show Defensive Situation Markers", "", ""] )
            self.screenPrinter.print_simple( ["Press 'r' to advance the baserunner", "", ""] )
            self.screenPrinter.print_simple( ["Press 'SPACE' to launch a baseball", "", ""] )
            self.screenPrinter.paragraph_break()
            
            self.screenPrinter.print_simple( ["Select a Defensive Situation:", "", ""] )
            self.screenPrinter.print_simple_tabbed( ["- Press 'c' to reset situations", "", ""] )
            self.screenPrinter.print_simple_tabbed( ["- Press 'y' to activate current situation", "", ""] )            
            
            ## User input  
            self.screenPrinter.print_user_input( ["You pressed:", self.curr_defensiveSit, self.current_defensiveSit_text] )
            self.screenPrinter.paragraph_break()
 
            ## Baseball status  
            self.screenPrinter.print_simple( ["BASES:", "", ""] )
            self.screenPrinter.print_simple( ["Highest base attained:", self.base_attained_text, ""] )
            self.screenPrinter.paragraph_break()
   
            self.screenPrinter.print_simple( ["BALL LOCATION:", "", ""] )
   
            self.screenPrinter.print_simple( [self.ball_location_text, "", ""] )
            self.screenPrinter.print_int( ["Ball height:", self.ball.curr_height_feet, "' "])
            #self.screenPrinter.print_rounded( ["Max ball height:", self.ball.max_height_feet, "' "], 1)
            #self.screenPrinter.print_int( ["Ball height in pixels:", self.ball.master_z, " pixels"])
            #self.screenPrinter.print_int( ["Ball 2D distance from Home:", self.ball.curr_distance_from_home_feet, "'"])
            self.screenPrinter.print_int( ["Ball velocity in 3D:", self.ball.curr_velo_mph, " mph"])
            #self.screenPrinter.print_coord( ["Ball 2D coord:", self.ball.coord_2D_pg, ""])
            self.screenPrinter.paragraph_break()
            
            self.screenPrinter.print_simple( ["Ball launched:", self.ball.launched_toggle, " "] )
            self.screenPrinter.print_simple( ["Ball rolling", self.ball.rolling_toggle, " "] )
            #self.screenPrinter.print_simple( ["Total time:", self.ball.total_duration_s, " "] )                        
            #self.screenPrinter.print_simple( ["Flight time", self.ball.flight_duration_s, " "] )
            self.screenPrinter.print_simple( ["# bounces", self.ball.bounce_count, " "] )
            self.screenPrinter.paragraph_break()
            self.screenPrinter.paragraph_break()
            
            self.screenPrinter.print_simple( ["BALL LAUNCH (WASD)", "", ""] )
            self.screenPrinter.print_simple( ["Exit velo", self.ball.launch_velo_mph, " mph"] )
            self.screenPrinter.print_simple( ["Launch angle", self.ball.launch_angle_deg, "°"] )
            self.screenPrinter.print_simple( ["Launch direction", self.ball.launch_direction_deg, "°"] )
            self.screenPrinter.paragraph_break()


        def prep_screen_data(self):
            if self.curr_defensiveSit in self.defensiveSit_plays:
                self.current_defensiveSit_text = self.defensiveSit_plays[self.curr_defensiveSit][0]
        
            base_attained = self.baserunner.get_base_attained()        
            if base_attained > 0:
                self.base_attained_text = str(base_attained) + "B" 
            

    ### Other gets / updates 
    for updateValueGetValue in range(1):
        
        def reset_play(self):
            self.reset_fielders()
            self.reset_numkeys()
            self.ball.reset_play()
    
        def reset_fielders(self):
            self.fielder_objects = self.setup.make_fielders(self.fielder_standard_coord, self.screen)  # 1-9
            
        def reset_baserunners(self):
            self.baserunner = self.setup.make_baserunners(self.screen)
                                
        def update_numkeys(self, key): 
            self.num_keys[key] = True    
        
        def reset_numkeys(self): 
            self.num_keys = [False] * 10
            
            
        def update_curr_defensiveSit(self, newSit): 
            self.curr_defensiveSit = newSit 
            
        def update_situation_start(self, bool_):
            self.situation_start = bool_
            
        def advance_baserunner(self):
            self.baserunner.assign_goal()
            
        def remove_baserunner_goal(self):
            self.baserunner.remove_goal()
            
        def update_ball_situational_location(self, location_text):
            self.ball_location_text = location_text