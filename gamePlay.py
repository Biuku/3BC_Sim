""" April 16, 2024 -- created this to shift my main activities into a separate module with Class(es)  

"""

import pygame
from pygame.locals import *
import math

from setup import Setup
from ball import Ball
from helpers import Helpers

##### ***** INITIALIZE PYGAME ***** #####

pygame.init()


class GamePlay:
    
    def __init__(self, screen):
        
        self.screen = screen

        self.setup = Setup(screen)
        self.ball = Ball(screen, (200, 200) )
        self.helper = Helpers(screen)

        ### Data ### 
        ## Collections of coordinates
        self.boundary_coords = self.setup.get_boundaries()  # lf_corner, cf_wall, rf_corner, four_B_tip
        
        self.boundary_thetas = self.setup.get_boundary_thetas()
                
        self.base_centroids = self.setup.base_centroids  # one_B, two_B, three_B, four_B, rubber_P
        self.fielder_standard_coord = self.setup.get_fielder_standard_coord(self.base_centroids) # Standard fielder pre-pitch coordinates: 1-9
        self.defensiveSit_fielder_coord = self.setup.get_defensiveSit_fielder_coord(self.base_centroids)
        
        ## Collections of game-play objects
        self.base_rects = self.setup.make_bases(self.base_centroids) # Dict of base rects -- collision objects
        self.defensiveSit_plays = self.setup.get_defensiveSit_plays(self.defensiveSit_fielder_coord)
        
        # Fielders and baserunners
        self.fielder_objects = self.setup.make_fielders(self.fielder_standard_coord, self.screen) #None # Placeholder
        self.baserunner = self.setup.make_baserunners(self.screen) #None # Placeholder
        self.bases_attained = {1: False, 2: False, 3: False, 4: False}
        
        ## Game status 
        self.curr_defensiveSit = 0
        self.num_keys = [False] * 10 ## Keep track of multiple num keys pressed above the kb
        
        #Toggles
        self.situation_start = False
        
        ## On-screen instructions
        self.instructions_x = self.instructions_master_x = 1400
        self.instructions_y = self.instructions_master_y = 850

    
    def choose_situation(self): #curr_defensiveSit, num_keys, defensiveSit_plays
        
        #     self.print_instructions() # Static instructions
        
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

        self.print_situation_choice() # Dynamic instructions -- update each game loop if user enters a choice
            

    def print_instructions(self): 
        ### Write static game instructions to the screen
        
        text_indent = 30
         
        instruction_text = [
            "INSTRUCTIONS",
            "Press 'B' to show Boundary Markers",
            "Press 'D' to show Defensive Situation Markers",
            "Select a Defensive Situation: ",
        ]
        
        self.instructions_y = self.helper.print_instruction_iterable(instruction_text, self.instructions_x, self.instructions_y)
        
        ## Indent text
        self.instructions_x += text_indent
        
        instruction_text = [
            "- Press 'C' to reset situations",
            "- Press 'S' to activate current situation",
        ]
        
        self.instructions_y = self.helper.print_instruction_iterable(instruction_text, self.instructions_x, self.instructions_y)
        
        self.instructions_x -= text_indent


    def print_situation_choice(self):
        
        ### Write instructions: key assignments for coverage situations 
        self.instructions_y += 10 # Create an extra break before displaying the choice
        x, y = self.instructions_x, self.instructions_y 
 
        self.helper.draw_text("You pressed: ", 'black', (x, y), self.setup.font20, 1)
        
        x += 120
        self.helper.draw_text(str(self.curr_defensiveSit), 'black', (x, y), self.setup.font20, 1)

        ## If they entered a valid defensive play, show it
        x += 40
        if self.curr_defensiveSit in self.defensiveSit_plays:
            text = self.defensiveSit_plays[self.curr_defensiveSit][0]
            self.helper.draw_text(text, 'black', (x, y), self.setup.font20, 1)
    
        ## Move the cursor down for the Base Attained instruction 
        self.instructions_y += 30
        
    
    def print_baserunner_status(self):
        #return
        ### Meta -- display the latest base attained
        base_attained = self.baserunner.get_base_attained()
        x, y = self.instructions_x, self.instructions_y
        
        self.helper.draw_text("BASES", 'black', (x, y), self.setup.font20, 1)
        
        y += 20
        
        text = "No bases attained"
                
        if base_attained > 0:
            text = "Highest base attained: " + str(base_attained) + "B" 
        
        self.helper.draw_text(text, 'black', (x, y), self.setup.font20, 1)
        
    ## Print the ball's location in baseball terms. Called from Main  > interpret_ball_location 
    def print_ball_loc(self, text2):
        x, y = self.instructions_x, self.instructions_y
        
        y += 60
        text1 = "BALL LOCATION:"
        self.helper.draw_text(text1, 'black', (x, y), self.setup.font20, 1)
        y += 20
        self.helper.draw_text(text2, 'black', (x, y), self.setup.font20, 1)
         
        
        
    ## After each game loop I need to return the coord of instructions to its start
    def reset_instructionCoord(self):
        self.instructions_x = self.instructions_master_x
        self.instructions_y = self.instructions_master_y
        
    
    def do_situation(self): #curr_defensiveSit, defensiveSit_plays, defensiveSit_fielder_coord, situation_start, ball_coord        

        if self.situation_start:

            if self.curr_defensiveSit in self.defensiveSit_plays:
                
                # For now, set the ball's coord relative to the active fielder's coord
                self.set_ball_coord()
                ball_coord = self.ball.get_coord()
                
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
                        self.ball.update_coord(new_ball_coord)
    
    
    def move_ball(self, moving_ball_bool):
        if moving_ball_bool:
            self.ball.click_move_ball()
    
        self.ball.draw_ball()

    
    def move_fielders(self, left, right, north, south):
        for fielder in self.fielder_objects.values():
            fielder.goal_move()
            
            if not( fielder.get_goal() ): 
                fielder.move_man(left, right, north, south) ## This overwrites the goal-setting animation unless only called when no goal
            fielder.detect_collisions(self.base_rects)
            
            fielder.draw_fielder()
    
    
    def move_baserunners(self, left, right, north, south):
        self.baserunner.move_baserunner(left, right, north, south)
        
        self.baserunner.detect_collisions(self.base_rects, self.fielder_objects)
        
        self.baserunner.draw_baserunner()
        
        self.print_baserunner_status()
        

### Update value, get value... ### 
    
    def reset_fielders(self):
        self.fielder_objects = self.setup.make_fielders(self.fielder_standard_coord, self.screen)  # 1-9
        
    def reset_baserunners(self):
        self.baserunner = self.setup.make_baserunners(self.screen)
                            
    def update_numkeys(self, key): 
        self.num_keys[key] = True    
    
    def reset_numkeys(self): 
        self.num_keys = [False] * 10
        
    def reset_numkeys(self): 
        self.num_keys = [False] * 10
        
    def update_curr_defensiveSit(self, newSit): 
        self.curr_defensiveSit = newSit 
        
    def update_situation_start(self, bool_):
        self.situation_start = bool_
        
    def advance_baserunner(self):
        self.baserunner.assign_goal()
        
    def get_ball_coord(self):
        return self.ball.get_coord()