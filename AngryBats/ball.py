import pygame
from pygame.locals import *
import math
from helpers_angryBats import Helpers
from setup_angryBats import Setup



pygame.init()


class Ball: 
    
    def __init__(self, screen, w, h, fps):
        self.screen = screen
        self.screen_w = w
        self.screen_h = h
        self.fps = fps
        
        self.setup = Setup(self.screen, self.screen_w, self.screen_h)
        self.helpers = Helpers(self.screen)
        
        ### 
        ## Ball constants
        self.ball_radius = 8
        self.ball_edge_thickness = 2
        
        ## Ball coord
        self.master_coord = (200, self.screen_h - 200) 
        self.start_coord = self.master_coord
        self.prev_coord = self.master_coord #For measuring ball velo 
        
        
        ## CALCULATED BALL VARIABLES
        self.curr_height_feet = 0
        self.curr_distance_from_home_x_feet = 0
        self.curr_velo_mph = 0


        ## GAME DELTAS AND GAME CONTROL VAR'S
        
        # Gravity
        self.gravity = 90   # with gravity of 120, launch velo of 360 mimics about 95 mph | Gravity is always positive y
        self.gravity_dy = 0
        self.launch_start_ms = 0
        self.duration_since_launch_s = 0
        
        # Rolling
        self.ground_drag_factor = 40 # | drag force/factor is always positive x
        self.rolling_dx = 0
        self.rolling_start_ms = 0
        self.duration_rolling_s = 0
        
        ## Ball launch 
        self.launched_toggle = False
        self.launch_start_coord = ( self.setup.launchZone_start_x,  self.setup.ball_launch_y) ## Updatefor thrown balls
        
        ## Ground proximity
        ground_proximity_threashold_pg = 20         ## How many pixels away from the ground the ball is before it's considered rolling
        self.ground_proximity = self.setup.top_of_floor - self.ball_radius - ground_proximity_threashold_pg
        self.rolling_toggle = False
        self.ball_x_on_the_ground = self.setup.top_of_floor + self.ball_radius

        ### Temp stuff to test the build         
        self.launch_angle_westward = 13 # degrees 
        self.launch_velo_mph = 105
        
        self.launch_angle_deg = 180 - self.launch_angle_westward
        self.launch_angle_rad = math.radians(self.launch_angle_deg)
        
        launch_velo_realism_factor = 3.7
        self.launch_velo_pg = self.launch_velo_mph * launch_velo_realism_factor


    #### Functions ####


    def launch_ball(self):
        self.launched_toggle = True
        self.rolling_toggle = False
        self.launch_start_ms = pygame.time.get_ticks()
        self.master_coord = self.launch_start_coord


    def move_ball_in_air(self):
        
        if self.launched_toggle:
            
            ## First, check if the ball is rolling. If it has stopped rolling, set launched_toggle to False

            if not(self.rolling_toggle):
                self.check_rolling()
            else:
                self.check_stopped_rolling()
                if not(self.launched_toggle):
                    return
            
            ## Set up some variables
            start_x, start_y = self.launch_start_coord
            self.update_deltas()

            # Delta x 
            new_x = self.move_ball_in_x(start_x, self.duration_since_launch_s)

            ## Delta y 
            # DY-1 -- updward velo from launch
            launch_vector_y = -1 * (math.sin(self.launch_angle_rad) * self.launch_velo_pg)
            launch_delta_y =  launch_vector_y * self.duration_since_launch_s

            # DY-2 -- gravity 
            new_y = start_y + launch_delta_y + self.gravity_dy
            # Add a jitter for y for bumps... if rolling??
            
            self.prev_coord = self.master_coord
            self.master_coord = (new_x, new_y)
            
            #show_theta_line(angle_deg, (start_x, start_y)   )


    def move_ball_in_x(self, start_x, duration_s):

        ## DX-1 -- Get new x position due to x vector of launch velocity 
        launch_vector_x = math.cos(self.launch_angle_rad) * self.launch_velo_pg
        delta_x = launch_vector_x * duration_s
        
        ## DX-2 -- Reduce speed if rolling
        if self.rolling_toggle:
            delta_x += self.rolling_dx
        
        return start_x + delta_x          
        
                     
    def update_deltas(self):
        self.duration_since_launch_s = self.helpers.get_total_time_seconds(self.launch_start_ms)
        self.duration_rolling_s = self.helpers.get_total_time_seconds(self.rolling_start_ms)
        self.gravity_dy = self.helpers.get_gravity_delta_y(self.gravity, self.duration_since_launch_s)
        self.rolling_dx = self.helpers.get_gravity_delta_y(self.ground_drag_factor, self.duration_rolling_s)
        
        self.update_distance_from_home_feet()
        self.update_height_feet()
        self.update_velo()
        

    ## RKeep ball within the playing area
    def check_collisions(self):
        x, y = self.master_coord
        
        x = min(x, (self.setup.launchZone_start_x - (self.setup.wall_thickness/2) + 1 - self.ball_radius) ) # Right edge
        x = max(x, self.setup.wall_thickness + self.ball_radius) # Left edge
        y = min(y, self.setup.top_of_floor - self.ball_radius) # bottom
        y = max(y, self.setup.wall_thickness//2 + self.ball_radius + 1) # Top
        
        self.master_coord = (x, y)


    def check_rolling(self):
        if self.duration_since_launch_s > 1:
            if self.master_coord[1] > self.ground_proximity:
                self.rolling_toggle = True
                self.master_coord = (self.master_coord[0], self.ball_x_on_the_ground) ## Snap the ball to the ground if it's close
                self.rolling_start_ms = pygame.time.get_ticks()


    def check_stopped_rolling(self):
        if self.rolling_toggle:
            if self.curr_velo_mph < 5:  ## Around 2 or so creates problems
                self.end_launch()
                

    def end_launch(self):
        self.launched_toggle = False
        self.rolling_toggle = False
        
        self.duration_rolling_s = 0
        self.duration_since_launch_s = 0


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
 
    def update_velo(self):
        frame_dx_feet_moved  = self.helpers.measure_distance_in_feet(self.prev_coord, self.master_coord)
        feet_per_second =  frame_dx_feet_moved  * self.fps # Game runs at 1/fps, so 45 frames in 1 IRL second
        self.curr_velo_mph = feet_per_second * (3600/5280)
    