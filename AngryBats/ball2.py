""" MAY 4 -- Updating to rename 'y' as 'z' prior to integrating into top-down legacy program """


import pygame
from pygame.locals import *
import math
import random
from helpers_angryBats import Helpers
from setup_angryBats import Setup
from ball_shadow import Shadow


pygame.init()


class Ball: 
    
    def __init__(self, screen, w, h, fps):
        for _ in range(1):
            self.screen = screen
            self.fps = fps
            
            self.setup = Setup(self.screen, w, h)
            self.helpers = Helpers(self.screen)
            
            ## Ball constants
            self.ball_radius = 6
            self.ball_edge_thickness = 2
            self.shadow = Shadow(self.screen, w, h, self.ball_radius)
            
            ## Ball control -- coord and speed
            self.master_coord = (self.setup.launchZone_start_x - 100, self.setup.top_of_floor - self.ball_radius)  
            self.prev_coord = self.master_coord #For measuring ball velo 
            self.velocity_x_pg = 0
            self.velocity_z_pg = 0
        
            ## Functional kinetic variables
            self.curr_height_feet = 0
            self.curr_velo_mph = 0
            self.prev_ticks = 0
            
            ## Ball launch 
            self.launched_toggle = False
            self.launch_start_coord = ( self.setup.launchZone_start_x,  self.setup.ball_launch_z) ## Update for thrown balls
            #self.launch_vector_y = 0
            self.launch_vector_x = 0
            
            ## Tracers to calibrate gravity, mph conversion, friction lossy, etc.
            self.launch_start_ms = 0
            self.flight_duration_s = 0  
            self.total_duration_s = 0  
            self.max_height_feet = 0  
            self.curr_distance_from_home_x_feet = 0
                    
        self.gravity = 7 / 1000 # 8 worked well for high, short fly ball
        self.mph_to_pg = 31 / 1000 # 28 worked well for high, short fly ball  
        
        # Ground proximity
        self.ball_y_on_the_ground = self.setup.top_of_floor - self.ball_radius
        self.ground_proximity_threshold = 2
        self.ground_proximity = self.ball_y_on_the_ground - self.ground_proximity_threshold

        # Bounce
        self.bounce_toggle = False
        self.bounce_lossy_z = 0.4 ## 35% = 65% loss per bounce
        self.bounce_lossy_x = 0.8 ## 80% = 20% loss per bounce
        self.bounce_count = 0

        ### Rolling        
        self.rolling_toggle = False
        self.jitter = 1 # Number of z pixels the ball hops (randomly) when rolling  
        self.rolling_lossy_x = 4 / 1000 # 7
        self.speed_stop_rolling_pg = 5 / 1000 # 0.01  # Speed in pg


        """   UPDATE HERE   """

        ### *** TEMP STUFF -- TO BUILD AND TEST *** ###
        self.launch_angle_leftward = 25 # degrees 
        self.launch_velo_mph = 65 # MPH


    #### Functions ####
    def launch_ball(self):
        self.launched_toggle = True
        self.rolling_toggle = False
        self.bounce_toggle = False
        
        self.bounce_count = 0
        self.flight_duration_s = 0
        self.max_height_feet = 0
        
        self.master_coord = self.launch_start_coord
        self.launch_start_ms = pygame.time.get_ticks()
        
        self.velocity_z_pg  = -1 * (math.sin(self.launch_angle_rad) * self.launch_velo_pg)
        self.velocity_x_pg  = math.cos(self.launch_angle_rad) * self.launch_velo_pg

    ### 1. Primary movement functions 
    def move_ball(self):
                
        if self.launched_toggle:
            ## Update variables 
            self.total_duration_s = self.helpers.get_total_time_seconds(self.launch_start_ms)
            
            ## Check state 
            self.check_end_motion()  ## Only checks if rolling = True
            self.check_bounce_roll()
        
            ## Calculate new coord
            new_x = self.move_ball_in_x()
            new_z = self.move_ball_in_z()
            
            ## Track prev coord to derive total velocity in MPH (vs last frame)    
            self.prev_coord = self.master_coord       
            self.master_coord = (new_x, new_z)

        self.update_deltas()
        self.check_collisions() 
        self.do_shadow()


    def move_ball_in_x(self):
            
        if self.rolling_toggle:
            temp_velo = self.velocity_x_pg + self.rolling_lossy_x
            self.velocity_x_pg = min(temp_velo, 0)
        
        return self.master_coord[0] + self.velocity_x_pg


    def move_ball_in_z(self):
        
        # Only incorporate launch velo and gravity if the ball is not rolling
        
        jitter_y = 0
        
        if not(self.rolling_toggle):
            if not(self.bounce_toggle):
                
                ## Pre-bounce / first flight
                self.velocity_z_pg += self.gravity
            
            elif self.bounce_toggle:
                ## snap the ball to the ground so it doesn't appear to hover (ground proximity is necessary to determine it's above 'rolling')
                # This makes the transition from the last bounces to rolling appear more natural
                new_z = self.master_coord[1] + self.ground_proximity_threshold
                self.master_coord = (self.master_coord[0], new_z)
                
                self.velocity_z_pg *= -1 * self.bounce_lossy_z # Bounce = change direction, lose some z velocity  
                self.velocity_x_pg *= self.bounce_lossy_x # A one-time x speed reduction at the moment of impact 
                self.bounce_toggle = False
        
        elif self.rolling_toggle:
            ## If the ball is rolling, only add hoppy shakes when above X mph
            if self.curr_velo_mph > 15:
                jitter_y = random.randrange(-self.jitter, self.jitter)
            
        return self.master_coord[1] + self.velocity_z_pg + jitter_y
    
     
    ### 2. Supporting movement functions         
    def check_bounce_roll(self):

        if self.master_coord[1] > self.ground_proximity:

            # Coming in hot = bounce
            if self.velocity_z_pg > 0.2:
                
                ## On first bounce, capture flight duration for tracer
                if self.bounce_toggle == False:
                    self.flight_duration_s = self.total_duration_s
            
                self.bounce_toggle = True
                self.bounce_count += 1

            ## Else, it's coming down slow = rolling
            elif self.velocity_z_pg >= 0:
                self.rolling_toggle = True
                self.bounce_toggle = False
                self.velocity_z_pg = 0
                self.master_coord = (self.master_coord[0], self.ball_y_on_the_ground) # Snap to the ground
                    

    def check_end_motion(self):
        if self.rolling_toggle:
            if abs(self.velocity_x_pg) < self.speed_stop_rolling_pg:
                self.end_launch()
                

    def end_launch(self):
        self.launched_toggle = False
        self.rolling_toggle = False
        self.bounce_toggle = False
        
        #self.master_coord = (self.master_coord[0], self.ball_y_on_the_ground)
        
        self.velocity_x_pg = 0
        self.velocity_z_pg = 0


    def update_deltas(self):
        
        ticks = pygame.time.get_ticks()
        
        if ticks - self.prev_ticks > 75:
            self.prev_ticks = ticks
        
            self.update_distance_from_home_feet()
            self.update_height_feet()
            self.update_velo_mph()
        
        ## Convert new raw angle and exit velo into pygame data 
        self.update_user_inputs()
        
    ### Keep ball in-bounds, and draw ball 
    def check_collisions(self):
        x, z = self.master_coord
        
        x = min(x, (self.setup.launchZone_start_x ) ) # Right edge
        x = max(x, self.setup.wall_thickness + self.ball_radius) # Left edge
        z = min(z, self.ball_y_on_the_ground) # bottom
        z = max(z, self.setup.wall_thickness//2 + self.ball_radius + 1) # Top
        
        self.master_coord = (x, z)


    def draw_ball(self):
        pygame.draw.circle(self.screen, self.setup.extremely_light_gray, self.master_coord, self.ball_radius)
        pygame.draw.circle(self.screen, self.setup.med_gray_c, self.master_coord, self.ball_radius, self.ball_edge_thickness)
        
        ## Call the shadow after drawing the ball makes it certain they are aligned, and that the shadow is drawn on top of the background, like the ball 
        self.do_shadow()


    def do_shadow(self):
        x = self.master_coord[0]
        self.shadow.update_shadow(self.curr_height_feet, x)
        
        
    def update_user_inputs(self):
        self.launch_angle_rad = math.radians(180 - self.launch_angle_leftward)
        self.launch_velo_pg = self.launch_velo_mph * self.mph_to_pg


    ### 4. Updates and gets
    def mouse_drag_ball(self):
        self.prev_coord = self.master_coord
        self.master_coord = pygame.mouse.get_pos()
        self.launched_toggle = False
        self.rolling_toggle = False
        
    def update_height_feet(self):
        
        ## Patch a bug where the height increases below the floor... don't know why
        end_z = min(self.setup.top_of_floor, self.master_coord[1])
        end_coord = (self.master_coord[0], end_z)
        
        start_coord = (self.master_coord[0], self.setup.top_of_floor)
        self.curr_height_feet = self.helpers.measure_distance_in_feet(start_coord, end_coord) 
        
        self.max_height_feet = max(self.max_height_feet, self.curr_height_feet)

    def update_distance_from_home_feet(self):
        start_coord = (self.setup.launchZone_start_x, self.master_coord[1])
        self.curr_distance_from_home_x_feet = self.helpers.measure_distance_in_feet(start_coord, self.master_coord) 
 
    def update_velo_mph(self):
        ## Velocity in all directions
        frame_dx_feet_moved  = self.helpers.measure_distance_in_feet(self.prev_coord, self.master_coord)
        feet_per_second =  frame_dx_feet_moved  * self.fps # Game runs at 1/fps, so 45 frames is 1 IRL second
        curr_velo_mph = feet_per_second * (3600/5280)
        

        self.curr_velo_mph = curr_velo_mph
    
    
