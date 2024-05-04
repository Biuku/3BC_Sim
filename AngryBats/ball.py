import pygame
from pygame.locals import *
import math
import random
from helpers_angryBats import Helpers
from setup_angryBats import Setup


pygame.init()


class Ball: 
    
    def __init__(self, screen, w, h, fps):
        self.screen = screen
        self.fps = fps
        
        self.setup = Setup(self.screen, w, h)
        self.helpers = Helpers(self.screen)
        
        #### *** Ball constants and state variables ***  ####
        ## Ball constants
        self.ball_radius = 8
        self.ball_edge_thickness = 2
        
        ## Ball coord
        self.master_coord = (200, self.setup.screen_h - 200) 
        self.prev_coord = self.master_coord #For measuring ball velo 
        
        ## CALCULATED BALL VARIABLES
        self.curr_height_feet = 0
        self.curr_distance_from_home_x_feet = 0
        self.curr_velo_mph = 0


        #### *** Ball kinetic variables ***  ####
        ## Ball launch 
        self.launched_toggle = False
        self.launch_start_coord = ( self.setup.launchZone_start_x,  self.setup.ball_launch_y) ## Updatefor thrown balls
        
        # Gravity
        self.gravity = 120   # with gravity of 120, launch velo of 360 mimics about 95 mph | Gravity is always positive y
        self.gravity_dy = 0
        self.launch_start_ms = 0
        self.duration_since_launch_s = 0
        
        ### Rolling
        self.bounce_or_roll_toggle = False
        
        self.rolling_toggle = False
        self.jitter = 1 # Number of pixels the ball hops (randomly) when rolling  
        self.rolling_drag_factor = 40 # "40" is for 45 fps # | drag force/factor is always positive x. Not a lossy %, a gravity-like force rightward
        self.rolling_dx = 0
        self.rolling_start_ms = 0
        self.rolling_duration_s = 0
        self.speed_stop_rolling = 8 # Speed in mph, below which the ball just comes to a stop (to avoid infinite slowing) 
        
        # Ground proximity
        self.ball_y_on_the_ground = self.setup.top_of_floor - self.ball_radius
        ground_threashold_pg = 5  ## How many pixels away from the ground the ball is before it's considered rolling
        self.ground_proximity = self.ball_y_on_the_ground - ground_threashold_pg

        # Bounce
        self.bounce_toggle = False
        self.bounce_lossy_y = 0.8 ## 80% = 20% loss
        self.bounce_drag_factor = 40
        self.bounce_dx = 0
        self.bounce_start_ms = 0
        self.bounce_duration_s = 2 ## Needs to be greater than 1 to enable sequential bounces
        self.y_vector_velo_mph = 0
        self.bounce_velo_y_pg = 0

        ### *** TEMP STUFF -- TO BUILD AND TEST *** ###
        self.launch_angle_westward = 45 # degrees 
        self.launch_velo_mph = 65
        
        self.launch_angle_rad = math.radians(180 - self.launch_angle_westward)
        launch_velo_realism_factor = 3.7
        self.launch_velo_pg = self.launch_velo_mph * launch_velo_realism_factor

        self.bounce_vector_y = 0


    #### Functions ####

    def launch_ball(self):
        self.launched_toggle = True
        self.rolling_toggle = False
        self.launch_start_ms = pygame.time.get_ticks()
        self.master_coord = self.launch_start_coord


    def move_ball(self):

        self.check_stopped_rolling()  ## Only checks if rolling = True

        if self.launched_toggle:
            ## Update variables 
            self.update_deltas()            
            self.check_ground_impact()

            new_y = self.move_ball_in_y()
            new_x = self.move_ball_in_x()
            
            self.prev_coord = self.master_coord
            self.master_coord = (new_x, new_y)


    def move_ball_in_x(self):

        ## DX-1 -- Get new x position due to x vector of launch velocity 
        launch_vector_x = math.cos(self.launch_angle_rad) * self.launch_velo_pg
        dx = launch_vector_x * self.duration_since_launch_s

        ## DX-2 -- If rolling, reduce speed and add hoppiness (jitter)
        if self.bounce_or_roll_toggle:
            dx += self.rolling_dx
        
        #if self.bounce_toggle:
        #    dx += self.rolling_dx #self.bounce_dx
        
        #if self.rolling_toggle:
        #    dx += self.rolling_dx
         
        return self.launch_start_coord[0] + dx


    def move_ball_in_y(self):
        start_y = self.launch_start_coord[1]
        
        # 1a) dy for bounce
        if self.bounce_toggle:
            start_y = self.ball_y_on_the_ground

            bounce_vector_y = -1 * 1 * self.bounce_velo_y_pg * self.bounce_lossy_y
            up_dy = bounce_vector_y * self.bounce_duration_s  ## Judt for screen data reporting
            
            return start_y + up_dy + self.helpers.get_gravity_delta_y(self.gravity, self.bounce_duration_s)

        
        elif self.rolling_toggle:
            jitter_y = random.randrange(-self.jitter, self.jitter)
            
            return self.ball_y_on_the_ground + jitter_y
        
        # 1b) dy for launch
        else:
            launch_vector_y = -1 * (math.sin(self.launch_angle_rad) * self.launch_velo_pg)
            up_dy =  launch_vector_y * self.duration_since_launch_s

            return start_y + up_dy + self.gravity_dy

                
    def check_ground_impact(self):
        if self.rolling_toggle:
            return
        
        if self.duration_since_launch_s > 1 and self.bounce_duration_s > 1: ## we shouldn't reset the bounce until it comes back down
            if self.master_coord[1] > self.ground_proximity:
                             
                ## Coming in hot -- start a new bounce
                if self.y_vector_velo_mph > 3: ## The variable is positive for downward velo, negative for upward velo
                    self.bounce_toggle = True
                    self.bounce_start_ms = pygame.time.get_ticks()  ## only used for y axis movement
                    self.bounce_velo_y_pg = self.y_vector_velo_mph * self.helpers.pixels_per_foot ## Need to initiate ... basically a new launch straight up
                    
                    if self.bounce_or_roll_toggle == False:
                        self.bounce_or_roll_toggle = True
                        self.rolling_start_ms = pygame.time.get_ticks()
                
                ## Else, it's coming down at only 0-2.99 mph
                elif self.y_vector_velo_mph >= 0: 
                    self.rolling_toggle = True
                    self.bounce_toggle = False
                    #self.rolling_start_ms = pygame.time.get_ticks() ## Need to account for edge case where it rolls without bouncing 
                            

    def check_stopped_rolling(self):
        if self.rolling_toggle:
            if self.curr_velo_mph < self.speed_stop_rolling:  ## Around 2 or so creates problems
                self.end_launch()
                

    def end_launch(self):
        self.launched_toggle = False
        self.rolling_toggle = False
        self.bounce_toggle = False
        self.bounce_or_roll_toggle = False
        
        self.rolling_duration_s = 0
        self.duration_since_launch_s = 0
        
        self.master_coord = (self.master_coord[0], self.ball_y_on_the_ground)


    def update_deltas(self):
        
        self.duration_since_launch_s = self.helpers.get_total_time_seconds(self.launch_start_ms)
        
        if self.bounce_or_roll_toggle:
            self.rolling_duration_s = self.helpers.get_total_time_seconds(self.rolling_start_ms)
    
        if self.bounce_toggle:
            self.bounce_duration_s = self.helpers.get_total_time_seconds(self.bounce_start_ms)
        
        self.gravity_dy = self.helpers.get_gravity_delta_y(self.gravity, self.duration_since_launch_s)
        self.rolling_dx = self.helpers.get_gravity_delta_y(self.rolling_drag_factor, self.rolling_duration_s)  ## Re-purposing the math for gravity. Drag is a force the other way 
        #self.bounce_dx = self.helpers.get_gravity_delta_y(self.bounce_drag_factor, self.rolling_duration_s) ## Use a constant time variable for the entire 'drag' period (but different drag factors)
        
        self.update_distance_from_home_feet()
        self.update_height_feet()
        self.update_velo_mph()
        self.update_y_vector_velo_mph()
        

    ## RKeep ball within the playing area
    def check_collisions(self):
        x, y = self.master_coord
        
        x = min(x, (self.setup.launchZone_start_x - (self.setup.wall_thickness/2) + 1 - self.ball_radius) ) # Right edge
        x = max(x, self.setup.wall_thickness + self.ball_radius) # Left edge
        y = min(y, self.ball_y_on_the_ground) # bottom
        y = max(y, self.setup.wall_thickness//2 + self.ball_radius + 1) # Top
        
        self.master_coord = (x, y)


    def draw_ball(self):
        pygame.draw.circle(self.screen, self.setup.extremely_light_gray, self.master_coord, self.ball_radius)
        pygame.draw.circle(self.screen, self.setup.med_gray_c, self.master_coord, self.ball_radius, self.ball_edge_thickness)


    ## Updates and gets
    def mouse_drag_ball(self):
        self.master_coord = pygame.mouse.get_pos()
        self.launched_toggle = False
        self.rolling_toggle = False
        
    def get_master_coord(self):
        return self.master_coord

    def update_height_feet(self): 
        start_coord = (self.master_coord[0], self.setup.top_of_floor)
        self.curr_height_feet = self.helpers.measure_distance_in_feet(start_coord, self.master_coord) 

    def update_distance_from_home_feet(self):
        start_coord = (self.setup.launchZone_start_x, self.master_coord[1])
        self.curr_distance_from_home_x_feet = self.helpers.measure_distance_in_feet(start_coord, self.master_coord) 
 
    def update_velo_mph(self):
        ## Velocity in all directions
        frame_dx_feet_moved  = self.helpers.measure_distance_in_feet(self.prev_coord, self.master_coord)
        feet_per_second =  frame_dx_feet_moved  * self.fps # Game runs at 1/fps, so 45 frames is 1 IRL second
        self.curr_velo_mph = feet_per_second * (3600/5280)

    def update_y_vector_velo_mph(self):
        delta_y_pg = self.master_coord[1] - self.prev_coord[1]
    
        frame_dy_feet_moved = delta_y_pg / self.helpers.pixels_per_foot 
        
        feet_per_second = frame_dy_feet_moved * self.fps # Game runs at 1/fps, so 45 frames is 1 IRL second
        self.y_vector_velo_mph = feet_per_second * (3600/5280)

    
