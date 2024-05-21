""" MAY 10 -- Creating this to shift some non-core code out of the bloated ball2.py module """


import pygame
from pygame.locals import *
import math

from helpers import Helpers
from setup import Setup


pygame.init()


class GameplayHelpers: 
    
    def __init__(self, screen):

        self.setup = Setup() 
        self.helpers = Helpers()
        self.screen = screen


    #### Functions ####


    for _init_ in range(1):

        def make_fielders(self, Fielder_object):

            fielder_objects = {}
            num_fielders = 1

            for fielder_id in [x for x in range(1, num_fielders + 1)]:
                coord = self.setup.fielder_standard_coord[fielder_id]                
                fielder_objects[fielder_id] = Fielder_object(self.screen, coord, fielder_id)

            return fielder_objects


        def make_baserunners(self, Baserunner_object):
            r1 = 1
            return Baserunner_object(self.screen, r1)


    for do_game_situation in range(1): 
        
        def give_primary_defensive_assignments(self, defensive_assignments, fielder_objects):
            
            ## For now, do in reverse -- place the ball relative to the guy assigned to field it
            ball_new_coord = self.meta_place_ball_for_situation(defensive_assignments)
            
            backup_dx = -70
            backup_dy = -70

            backup_coord = ( ball_new_coord[0] + backup_dx , ball_new_coord[1] + backup_dy )

            ## Assign 1 fielder to field the ball (#1), and 1 backup (#2)
            fielder_objects[ defensive_assignments.index(1) ].assign_goal(ball_new_coord)
            fielder_objects[ defensive_assignments.index(2) ].assign_goal(backup_coord)
            
            return fielder_objects, ball_new_coord ## Must return the ball coord to pass them to the ball


        def give_secondary_defensive_assignments(self, defensive_assignments, fielder_objects):
            for fielder_id, fielder_positioning_id in enumerate(defensive_assignments): 
            
                if fielder_positioning_id not in [1, 2] and isinstance(fielder_positioning_id, int): # In defensive_assignments, index 0 is a text description of the baseball situation  
                        
                    ## Assign each fielder coordinates representing standard positioning for this baseball situation
                    fielder_goal = self.setup.defensiveSit_fielder_coord[fielder_positioning_id]
                    fielder_objects[fielder_id].assign_goal(fielder_goal)
                    
            return fielder_objects


        def meta_place_ball_for_situation(self, defensive_assignments): 
            primary_fielder = defensive_assignments.index(1)
            x, y = self.setup.fielder_standard_coord[primary_fielder]
            ball_new_coord = (x - 150, y - 150)
            
            return ball_new_coord
                
            #self.ball.update_coord_for_situation(ball_new_coord)


    for update_ball in range(1):
        
        def move_ball(self, ball, mouse_drag, curr_fielder, prev_fielder):
            
            if curr_fielder:
                self.move_ball_with_fielder(ball, curr_fielder)
            
            if mouse_drag:
                curr_fielder, prev_fielder = self.mouse_drag_ball(ball)
                
            else:
                ball.move_ball()
                
            return curr_fielder, prev_fielder
        

        def mouse_drag_ball(self, ball):
            curr_fielder = None
            prev_fielder = None
            ball.end_launch()
            ball.mouse_drag_ball()
            
            return curr_fielder, prev_fielder


        def move_ball_with_fielder(self, ball, curr_fielder):
            
            ## Get coord from fielder, send to ball
            fielder_centre_coord = curr_fielder.get_centre_coord()
            ball.update_coord_for_situation( fielder_centre_coord )


    for throw in range(1):
        
        def change_throw_receiver(self, fielder_objects, throw_receiver):
            
            if not throw_receiver:
                receiver_id = 4   # Default to second baseman 
                throw_receiver = self.new_throw_receiver(receiver_id, fielder_objects)

            else:
                throw_receiver.update_throw_receiver(False) # Cancel the current receiver's status
                
                receiver_id = throw_receiver.get_id() + 1

                if receiver_id > 9:
                    receiver_id = 1

                throw_receiver = self.new_throw_receiver(receiver_id, fielder_objects)
        
            return throw_receiver
        

        def new_throw_receiver(self, receiver_id, fielder_objects):
            
            throw_receiver = fielder_objects[receiver_id]
            throw_receiver.update_throw_receiver(True)
            
            return throw_receiver
            
            #theta = self.get_throw_theta(self.curr_fielder_with_ball, self.throw_receiver)
            #self.send_throw_data_to_ball(theta)



    for update_fielders_and_baserunners in range(1):
        
        def move_and_draw_fielders(self, fielder_objects, keyboard_arrow_input):

            for fielder in fielder_objects.values():
                fielder.goal_move() 

                if not fielder.get_goal():
                    fielder.move_man(keyboard_arrow_input) ## This overrides the goal-setting animation unless only called when no goal 

                fielder.draw_man()
             
            #return fielder_objects


        def move_and_draw_baserunners(self, baserunners): 
            baserunners.move_baserunner() 
            baserunners.draw_man()

        
    def get_throw_theta(self, thrower_object, receiver_object):

        start_coord = thrower_object.get_centre_coord()
        end_coord = receiver_object.get_centre_coord()

        theta_rad = self.helpers.coord_to_theta(start_coord, end_coord)

        return math.degrees(theta_rad)

# Last time