""" MAY 4 -- Updating to rename 'y' as 'z' prior to integrating into top-down legacy program """


import pygame
from pygame.locals import *
import math
import random

from helpers import Helpers
from setup import Setup
from _ball.ball_shadow import Shadow
from _ball.ball2_helpers import BallHelpers 


pygame.init()


class Ball: 
    
    def __init__(self, screen):
        
        self.setup = Setup() 
        self.helpers = Helpers()
        self.ball_helpers = BallHelpers(screen)

        self.screen = screen
        
        #### Ball constants
        for constants in range(1):
            self.master_ball_radius = 5
            self.ball_radius = self.master_ball_radius
            self.ball_edge_thickness = 2
            
            self.shadow = Shadow(screen, self.ball_radius)

            self.user_interface_start_x = self.setup.user_interface_start_x
        
        for calibrations_and_collisions in range(1):
            #### Ball launch 
            self.launched_toggle = False
            self.velocity_x_pg = 0
            self.velocity_y_pg = 0
            self.velocity_xy_pg = 0
            self.velocity_z_pg = 0

            #### Calibrations
            self.gravity = 7 / 1000 # 8 worked well for high, short fly ball
            self.mph_to_pg = 31 / 1000 # 28 worked well for high, short fly ball  
            
            # Bounce
            self.bounce_toggle = False
            self.bounce_lossy_z = 50 / 100 ## 35% = 65% loss per bounce
            self.bounce_lossy_xy = 80 / 100 ## 96% = 4% loss per bounce
            self.bounce_count = 0
            
            # Bounce off OF wall
            self.OF_wall_toggle = False
            self.super_OF_wall_toggle = True # Can be turned False, can never be turned True during a play
            self.bounce_off_OF_wall_lossy_xy = 20 / 100 

            # Rolling        
            self.rolling_toggle = False
            self.rolling_lossy_pct = 99.5 / 100  # 99.5% = 0.5% loss per frame
            
        for coord in range(1):
            #### Master coord -- single source of truth
            self.master_x = self.setup.four_B_tip[0]
            self.master_y = self.setup.four_B_tip[1]
            self.master_z = 3 * 2.8  ## This is the height in pixels above the AngryBats screen_h - floor_width
            
            # Cord tuples 
            self.coord_2D_pg = (self.master_x, self.master_y)
            self.coord_3D_pg = (self.master_x , self.master_y,  self.master_z)

        for metrics in range(1):
            # Velocity
            self.curr_velo_mph = 0 
            self.prev_coord_3D = self.coord_3D_pg  ## For measuring distance travelled per frame
            self.prev_coord_3D_2 = self.coord_3D_pg 
            self.prev_ticks = 0
            self.tick_duration = 0.1 # Avoid division by zero initially

            # Distance 
            self.curr_distance_from_home_feet = 0
            self.curr_height_feet = 0    
            self.max_height_feet = 0


        """   UPDATE START DATA HERE   """

        self.launch_velo_mph = 70 # MPH
        self.launch_angle_deg = self.master_launch_angle_deg = 35 # degrees 
        self.launch_direction_deg = self.master_launch_direction_deg = 90 ## 90 = straight at 2B | 135 = 3B | 45 = 1B 

        """   ^^^^^^^^^^^^  """


    #### Functions ####
    
    def batted_launch(self):
        self.reset_play()
        
        self.thrown_launch()
        
    
    def thrown_launch(self):
        self.end_launch()
        
        self.launched_toggle = True
        self.super_OF_wall_toggle = True
        
        self.velocity_z_pg = self.launch_velo_pg * math.sin(self.launch_angle_rad)
        self.velocity_xy_pg = self.launch_velo_pg * math.cos(self.launch_angle_rad)


    for ball_movement in range(1):
        
        def move_ball(self):
                    
            if self.launched_toggle:

                ## Check state 
                self.check_end_motion()  ## Only checks if rolling = True
                self.check_bounce_roll()
            
                ## Calculate new coord
                new_x, new_y = self.move_ball_in_xy()
                new_z = self.move_ball_in_z()
                
                self.master_x = new_x
                self.master_y = new_y
                self.master_z = new_z

            self.update_metrics_for_movement()


        def move_ball_in_xy(self):

            if self.rolling_toggle:
                self.velocity_xy_pg *= self.rolling_lossy_pct
           
            if self.OF_wall_toggle:
                self.bounce_off_OF_wall()

            new_x = self.master_x + self.velocity_x_pg
            new_y = self.master_y + self.velocity_y_pg

            return new_x, new_y


        def bounce_off_OF_wall(self):

            self.launch_direction_deg += 180   # The OF wall is line a parabola facing the plate, so a batted ball should bounce straight back 
            self.velocity_xy_pg *= self.bounce_off_OF_wall_lossy_xy
                
            self.update_for_user_inputs() ## Need to convert master degrees to master radians
            self.update_xy_vectors() ## Need to vectorize xy into x and y 
            
            self.OF_wall_toggle = False


        def move_ball_in_z(self):

            if not self.rolling_toggle:
                if not self.bounce_toggle:
                    self.velocity_z_pg -= self.gravity  ## No bounce
                
                ## Bounce
                elif self.bounce_toggle:
            
                    self.velocity_z_pg *= -1 * self.bounce_lossy_z # Change direction AND lose some z velocity  
                    self.velocity_xy_pg *= self.bounce_lossy_xy # A once-per-bounce xy speed reduction at the moment of impact
                    
                    self.bounce_toggle = False
            
            return self.master_z + self.velocity_z_pg 


        def embiggen_ball_for_height(self):
            amplifed_factor = self.shadow.master_ball_height_pct * 1.6
            only_big_factor = max(amplifed_factor, 0.15) - 0.15  ## Set the factor_pct to zero if it's close to zero -- don't fuss near the ground 
            self.ball_radius = self.master_ball_radius * (1 + only_big_factor)


        def mouse_drag_ball(self):
            self.master_x, self.master_y = pygame.mouse.get_pos()
            self.launched_toggle = False
            self.rolling_toggle = False
            
            self.update_metrics_for_movement()


    for ball_movement_support in range(1):

        def update_xy_vectors(self):
                ## Vectorize self.velocity_xy_pg for x and y vectors
                self.velocity_x_pg = self.velocity_xy_pg * math.cos(self.launch_direction_rad)
                self.velocity_y_pg = self.velocity_xy_pg * math.sin(self.launch_direction_rad)


        def update_metrics_for_movement(self):
            self.update_for_user_inputs()  ## if launch data has been updated, need to update conversion to radians, etc.
            self.update_xy_vectors()
            
            ## Check collisions must happen before the coord's are packed as tuples 
            self.check_collisions()
            
            ## Pack coord as tuples for easy measurements
            self.coord_3D_pg = (self.master_x, self.master_y, self.master_z)
            self.coord_2D_pg = (self.master_x, self.master_y)

            ## Update the more tedius metrics in 'ball_helpers' sub-module
            packaged_returnable = self.ball_helpers.update_kpi_metrics(self.master_z, self.coord_3D_pg)
            
            self.curr_velo_mph = packaged_returnable['velo']
            self.curr_distance_from_home_feet = packaged_returnable['distance']
            self.curr_height_feet = packaged_returnable['height']
            self.max_height_feet = packaged_returnable['max height']


    for ball_collisions in range(1):
        
        def check_collisions(self):           
            edge_buffer = 20
            
            self.master_x = min(self.master_x, self.user_interface_start_x) 
            self.master_x = max(self.master_x, edge_buffer) # Left edge
            self.master_y = min(self.master_y, self.setup.screen_h - edge_buffer) # bottom
            self.master_y = max(self.master_y, edge_buffer) # Top

            ### Check collision with OF wall
            self.check_OF_wall_collision()


        def check_OF_wall_collision(self):
           
            if self.super_OF_wall_toggle:
                                
                ball_dist_from_main_centroid_pg = self.helpers.measure_distance_in_pixels(self.setup.main_centroid, self.coord_2D_pg) - self.ball_radius
                
                if ball_dist_from_main_centroid_pg >= self.helpers.main_centroid_radius:
                    self.OF_wall_toggle = True ## Tells the xy movement function to reverse xy direction
                    self.super_OF_wall_toggle = False ## Never check for OF bounce a second time ... let the ball get clear of the OF wall


    for checkEnd_and_drawBall in range(1):

        def check_bounce_roll(self):
            
            if self.master_z < 1: 

                # Coming in hot = bounce
                if self.velocity_z_pg < -0.2:
                    self.bounce_toggle = True
                    self.bounce_count += 1

                ## Else, it's coming down slow = rolling
                elif self.velocity_z_pg <= 0:
                    self.rolling_toggle = True
                    self.bounce_toggle = False
                    self.velocity_z_pg = 0
                    self.master_z = 0 # Snap to the ground


        ## Called from ball.move_ball() -- when launched_toggle is true
        def check_end_motion(self):
            speed_stop_rolling_pg = 0.08
                
            if self.rolling_toggle:
                if abs(self.velocity_xy_pg) < speed_stop_rolling_pg:
                    self.end_launch()


        def end_launch(self):
            
            if self.launched_toggle: ## If the actual end of the play, do this. If resetting the start of a play, don't
                self.launch_angle_deg = self.master_launch_angle_deg
                self.launch_direction_deg = self.master_launch_direction_deg

            self.launched_toggle = False
            self.rolling_toggle = False
            self.bounce_toggle = False
            
            self.velocity_x_pg = 0
            self.velocity_y_pg = 0
            self.velocity_z_pg = 0
            
            self.bounce_count = 0


        def reset_play(self):
            
            self.end_launch()
            
            self.master_x = self.setup.four_B_tip[0]
            self.master_y = self.setup.four_B_tip[1]
            self.master_z = 3*2.8 # 3' off the ground
            
            self.max_height_feet = 0



        def draw_ball(self): 

            self.shadow.update_shadow(self.curr_height_feet, self.coord_2D_pg)
            self.embiggen_ball_for_height()
            
            pygame.draw.circle(self.screen, self.setup.extremely_light_gray, self.coord_2D_pg, self.ball_radius)
            pygame.draw.circle(self.screen, self.setup.med_gray_c, self.coord_2D_pg, self.ball_radius, self.ball_edge_thickness)


    for update_metrics in range(1):

        # Modify launch data -- for user updates to contact settings 
        def receive_launch_deltas(self, launch_metrics):

            self.launch_velo_mph += launch_metrics['exit_velo']
            self.launch_angle_deg += launch_metrics['launch_angle']
            self.launch_direction_deg += launch_metrics['launch_direction']
                
            self.update_for_user_inputs()
            
            
        # Replace current launch data -- for throws
        def receive_new_launch_deta(self, launch_metrics):

            self.launch_velo_mph = launch_metrics['exit_velo']
            self.launch_angle_deg = launch_metrics['launch_angle']
            self.launch_direction_deg = launch_metrics['launch_direction']
                
            self.update_for_user_inputs()


        def update_for_user_inputs(self):
            self.launch_velo_pg = self.launch_velo_mph * self.mph_to_pg
            self.launch_angle_rad = math.radians(180 - self.launch_angle_deg)
            self.launch_direction_rad = math.radians(180 - self.launch_direction_deg)
            
            ### Tracer to show the launch angle with a line 
            start = self.setup.base_centroids[4]
            end = self.helpers.theta_to_endCoord(start, self.launch_direction_deg, 50)
            pygame.draw.line(self.screen, 'grey', start, end, 2)


    ## Gameplay updates coord 
    def update_coord_for_situation(self, coord):
        self.master_x = coord[0]
        self.master_y = coord[1]


    ## When a fielder drops the ball they should fling it far enough away that they don't immediately pick it back up
    def fielder_drop_the_ball(self):
        
        dist_pg = 1.3 * self.setup.ball_catch_proximity ## Drop the ball just a little further than your pickup range 
        theta = 225
        
        self.master_x, self.master_y = self.helpers.theta_to_endCoord( self.coord_2D_pg, theta, dist_pg)

        self.update_metrics_for_movement() ## Update the packaged coord used to detect collisions


    ## Send ball date to gamePlay for screen printng
    def package_data_objects(self):
        
        ball_metrics_screen_text = {   
                "ball_height": self.curr_height_feet,
                "max_ball_height": self.max_height_feet,
                "ball_height_pixels": self.master_z,
                "ball_distance_Home": self.curr_distance_from_home_feet,
                "ball_velo": self.curr_velo_mph,
                "ball_coord": self.coord_2D_pg,
                "launched_toggle": self.launched_toggle,
                "rolling_toggle": self.rolling_toggle,
                "num_bounces": self.bounce_count,
            }

        return ball_metrics_screen_text

# Last line