""" MAY 4 -- Updating to rename 'y' as 'z' prior to integrating into top-down legacy program """


import pygame
from pygame.locals import *
import math
import random
from helpers import Helpers
from setup import Setup
from ball_shadow import Shadow


pygame.init()


class Ball: 
    
    def __init__(self, screen, w, h, fps, user_interface_start_x):
        
        self.screen = screen
        self.fps = fps
        
        self.setup = Setup(self.screen, w, h)
        self.helpers = Helpers(self.screen)
        
        #### Ball constants
        for constants in range(1):
            self.master_ball_radius = 5
            self.ball_radius = self.master_ball_radius
            self.ball_edge_thickness = 2
            self.shadow = Shadow(self.screen, w, h, self.ball_radius)
            self.user_interface_start_x = user_interface_start_x
        
        for launch_calibrations in range(1):
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
            self.curr_distance_from_OF_wall_centroid = 0
            self.bounce_off_OF_wall_lossy_xy = 20/100 

            # Rolling        
            self.rolling_toggle = False
            self.jitter = 3 # Number of z pixels the ball hops (randomly) when rolling  
            self.rolling_lossy_pct = 99.5 / 100  # 99.5% = 0.5% loss per frame
            
            ## Tracers for calibrations
            # Time tracers
            self.launch_start_ms = 0
            self.flight_duration_s = 0  
            self.total_duration_s = 0  
            # Distance tracers
            self.curr_distance_from_home_feet = 0
            self.max_height_feet = 0

        for coord in range(1):
            #### Master coord -- single source of truth
            self.master_x = self.setup.four_B_tip[0]
            self.master_y = self.setup.four_B_tip[1]
            self.master_z = 3 * 2.8  ## This is the height in pixels above the AngryBats screen_h - floor_width
            
            # Cord tubles 
            self.coord_2D_pg = (self.master_x, self.master_y)
            self.coord_3D_pg = (self.master_x , self.master_y,  self.master_z)
        
        for metrics in range(1):
            ####Metrics
            # Current velocity
            self.curr_velo_mph = 0 
            self.prev_coord_3D = self.coord_3D_pg  ## For measuring distance travelled per frame
            self.prev_coord_3D_2 = self.coord_3D_pg 
            self.prev_ticks = 0
            self.tick_duration = 0.1 # Avoid division by zero initially

            # Height above the ground 
            self.curr_height_feet = 0        
 
        """   UPDATE HERE   """
        self.launch_velo_mph = 80 # MPH
        self.launch_angle_deg = 20 # degrees 
        self.launch_direction_deg = 45 ## 90 = straight at 2B | 135 = 3B | 45 = 1B 
        
        """   ^^^^^^^^^^^^  """


    #### Functions ####

    def launch_ball(self):
        self.reset_play()
        
        self.launched_toggle = True
        self.super_OF_wall_toggle = True
        
        self.launch_start_ms = pygame.time.get_ticks()
        
        self.velocity_z_pg = self.launch_velo_pg * math.sin(self.launch_angle_rad)
        self.velocity_xy_pg = self.launch_velo_pg * math.cos(self.launch_angle_rad)
        #self.update_xy_vectors()
        

        ### 1. Primary movement functions 
    
    
    for ball_movement in range(1):
        
        def move_ball(self):
                    
            if self.launched_toggle:
                ## Update variables 
                self.total_duration_s = self.helpers.get_total_time_seconds(self.launch_start_ms)
                
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
            self.draw_ball()
            #self.temp_of_wall_angle_tracer()
            

        def move_ball_in_xy(self):

            if self.rolling_toggle:
                self.velocity_xy_pg *= self.rolling_lossy_pct
           
            ## Bounce off the OF wall
            if self.OF_wall_toggle:

                ## The OF wall is line a parabola facing the plate, so a batted ball should bounce straight back 
                self.launch_direction_deg += 180
                self.velocity_xy_pg *= self.bounce_off_OF_wall_lossy_xy
                
                self.update_for_user_inputs() ## Need to convert master degrees to master radians
                self.update_xy_vectors() ## Need to vectorize xy into x and y 
                
            
            new_x = self.master_x + self.velocity_x_pg
            new_y = self.master_y + self.velocity_y_pg

            return new_x, new_y

        def temp_of_wall_angle_tracer(self):
            
            modifier_deg = 180
            juicer = 300
            
            velocity_xy_pg = self.launch_velo_pg * math.cos(self.launch_angle_rad)
            
            launch_direction_rad = math.radians(self.launch_direction_deg + modifier_deg)  ## At launch, radius is calculated using 180- deg... so... have to account for that here too.

            x_vector = velocity_xy_pg * math.cos(launch_direction_rad) * juicer
            y_vector = velocity_xy_pg * math.sin(launch_direction_rad) * juicer
            
            """
            ## Get point on the OF Wall 
            best_coord = (0, 0)
            delta = 10000
            centroid = self.setup.main_centroid
            
            
            ### Get the coord where the measuring tape would intersect the OF wall
            for distance in range(1176, 1274):
                from_home_coord = self.helpers.theta_to_endCoord(centroid, self.launch_angle_deg, distance)
                
                ## get distance to that coord from the centroid
                from_centroid_distance = self.helpers.measure_distance_in_pixels( centroid, from_home_coord)
                
                temp_delta = abs(from_centroid_distance - self.setup.main_centroid_radius)
                
                if temp_delta < delta:
                    best_coord = from_home_coord
                    delta = temp_delta
            """

            start_coord = self.setup.cf_wall #best_coord 
            end_x = start_coord[0] + x_vector
            end_y = start_coord[1] + y_vector
            end_coord = (end_x, end_y)
            
            pygame.draw.line(self.screen, 'blue', start_coord, end_coord, 3)
            pygame.draw.circle(self.screen, 'black', end_coord, 4)
            
            print( self.launch_direction_deg, int(x_vector), int(y_vector) )


        def move_ball_in_z(self):

            if not(self.rolling_toggle):
                if not(self.bounce_toggle):
                    
                    ## Pre-bounce / first flight
                    self.velocity_z_pg -= self.gravity
                
                ## Bounce
                elif self.bounce_toggle:
            
                    self.velocity_z_pg *= -1 # Bounce = change direction 
                    self.velocity_z_pg *= self.bounce_lossy_z # Bounce = lose some z velocity 
                    
                    self.velocity_xy_pg *= self.bounce_lossy_xy # A once-per-bounce xy speed reduction at the moment of impact
                    
                    ## Add some inpredictability to the hop  
                    bounce_jitter = (random.randrange(-self.jitter, self.jitter))/100
                    self.velocity_xy_pg *= (1 - bounce_jitter )
      
                    self.bounce_toggle = False
   
            elif self.rolling_toggle:

                ## Add jitter if the ball is rolling with some speed
                if self.curr_velo_mph > 15:
                    self.master_x += random.randrange(-self.jitter, self.jitter)
                    self.master_y += random.randrange(-self.jitter, self.jitter)
            
            ## If the ball collides off the OF wall, take some z velo off (lol, almost said 'zelo' ... )
            if self.OF_wall_toggle:
                
                #self.velocity_z_pg = -1 * abs(self.velocity_z_pg) ## Ensure it's going down off the wall
                self.velocity_z_pg *= self.bounce_lossy_z ## Take off some z velo
                
                self.OF_wall_toggle = False
            
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
            

    for checks_end_and_draw_ball in range(1):    

        def check_bounce_roll(self):
            
            if self.master_z < 0: 

                # Coming in hot = bounce
                if self.velocity_z_pg < -0.2:
                    
                    ## On first bounce, capture flight duration for tracer
                    if self.bounce_toggle == False:
                        self.flight_duration_s = self.total_duration_s
                
                    self.bounce_toggle = True
                    self.bounce_count += 1

                ## Else, it's coming down slow = rolling
                elif self.velocity_z_pg <= 0:
                    self.rolling_toggle = True
                    self.bounce_toggle = False
                    self.velocity_z_pg = 0
                    self.master_z = 0 # Snap to the ground


        def check_end_motion(self):
            speed_stop_rolling_pg = 0.08
                
            if self.rolling_toggle:
                if abs(self.velocity_xy_pg) < speed_stop_rolling_pg:
                    self.end_launch()


        def check_collisions(self):           
            edge_buffer = 20
            
            self.master_x = min(self.master_x, self.user_interface_start_x) 
            self.master_x = max(self.master_x, edge_buffer) # Left edge
            self.master_y = min(self.master_y, self.setup.screen_h - edge_buffer) # bottom
            self.master_y = max(self.master_y, edge_buffer) # Top

            ### Check collision with OF wall
            if self.super_OF_wall_toggle:
                ## If you are on the circle that describes the OF wall bounce off the wall 
                radius = self.setup.main_centroid_radius - self.ball_radius ## The radias is to the inside of the OF wall (its thickness is added when it's drawn) 
                if self.curr_distance_from_OF_wall_centroid >= radius: 
                    self.OF_wall_toggle = True
                    self.super_OF_wall_toggle = False ## Never check a second time
                    print("Turn on wall-bounce flag")
       

        def end_launch(self):
            self.launched_toggle = False
            self.rolling_toggle = False
            self.bounce_toggle = False
            
            self.velocity_x_pg = 0
            self.velocity_y_pg = 0
            self.velocity_z_pg = 0


        def reset_play(self):
            self.end_launch()
            
            self.master_x = self.setup.four_B_tip[0]
            self.master_y = self.setup.four_B_tip[1]
            self.master_z = 3*2.8 # 3' off the ground
            
            self.bounce_count = 0
            self.flight_duration_s = 0
            self.max_height_feet = 0


        def draw_ball(self): 

            self.shadow.update_shadow(self.curr_height_feet, self.coord_2D_pg)
            self.embiggen_ball_for_height()
            
            pygame.draw.circle(self.screen, self.setup.extremely_light_gray, self.coord_2D_pg, self.ball_radius)
            pygame.draw.circle(self.screen, self.setup.med_gray_c, self.coord_2D_pg, self.ball_radius, self.ball_edge_thickness)


    for update_metrics in range(1):
        
        def update_metrics_for_movement(self):
            self.update_for_user_inputs()  ## if launch data has been updated, need to update conversion to radians, etc.
            
            ## Check collisions must happen before the coord's are packed as tuples 
            self.check_collisions()
            
            ## Back coord as tuples for each management
            self.coord_3D_pg = (self.master_x, self.master_y, self.master_z) ## Package it up neatly for measurements
            self.coord_2D_pg = (self.master_x, self.master_y)
            
            self.update_xy_vectors()
            self.update_distance_from_main_centroid()
            
            ticks = pygame.time.get_ticks()
            if ticks - self.prev_ticks > 100: ## 40 = 0.04 seconds delay between updates
                self.prev_coord_3D_2 = self.prev_coord_3D 
                self.prev_coord_3D = self.coord_3D_pg
                self.tick_duration = ticks - self.prev_ticks ## To calculate mph
                self.prev_ticks = ticks
                
                self.update_velo_mph()
                self.update_2D_distance_from_home_feet()
                self.update_height()


        def update_xy_vectors(self):
            ## Vectorize self.velocity_xy_pg for x and y vectors
            self.velocity_x_pg = self.velocity_xy_pg * math.cos(self.launch_direction_rad)
            self.velocity_y_pg = self.velocity_xy_pg * math.sin(self.launch_direction_rad)
            

        def update_for_user_inputs(self):
            self.launch_angle_rad = math.radians(180 - self.launch_angle_deg)
            self.launch_direction_rad = math.radians(180 - self.launch_direction_deg)
            
            self.launch_velo_pg = self.launch_velo_mph * self.mph_to_pg
            
            ### Tracer to confirm the right angle
            start = self.setup.base_centroids['four_B']
            deg = self.launch_direction_deg
            length = 100
            end = self.helpers.theta_to_endCoord(start, deg, length)
            
            pygame.draw.line(self.screen, 'grey', start, end, 2)


        def update_height(self):
            
            self.curr_height_feet = self.master_z / self.setup.pixels_per_foot
            self.max_height_feet = max(self.max_height_feet, self.curr_height_feet)


        def update_2D_distance_from_home_feet(self):
            start_coord = self.setup.base_centroids['four_B']
            self.curr_distance_from_home_feet = self.helpers.measure_distance_in_feet(start_coord, self.coord_2D_pg)
            
            
        def update_distance_from_main_centroid(self):
            self.curr_distance_from_OF_wall_centroid = self.helpers.measure_distance_in_pixels(self.setup.main_centroid, self.coord_2D_pg)
    
    
        def update_velo_mph(self):
            ## Velocity in 3 directions
            
            duration_seconds = self.tick_duration / 1000
            
            distance_pixels = self.helpers.measure_3D_distance_in_pixels( self.prev_coord_3D, self.prev_coord_3D_2  ) 
            distance_feet = distance_pixels / self.setup.pixels_per_foot

            feet_per_second = distance_feet * (1 / duration_seconds) # It's running about 0.110 seconds between duration intervals, so about 9*the distance = the distance in 1 second
            self.curr_velo_mph = feet_per_second * (3600/5280)


    ## Gameplay updates coord 
    def update_coord_for_situation(self, coord):
        self.master_x = coord[0]
        self.master_y = coord[1]
    
