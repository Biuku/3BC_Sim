""" MAY 10 -- Creating this to shift some non-core code out of the bloated ball2.py module """


import pygame
from pygame.locals import *
import math

from helpers import Helpers
from setup import Setup


pygame.init()


class BallHelpers: 
    
    def __init__(self, screen):
        
        self.setup = Setup() 
        self.helpers = Helpers()

        self.screen = screen
        
        self.master_z = 0    
        self.coord_3D_pg = (0,0,0)    

        # Distance tracers
        self.curr_distance_from_home_feet = 0
        self.curr_height_feet = 0       
        self.max_height_feet = 0
        
        # Current velocity
        self.curr_velo_mph = 0 
        self.prev_coord_3D = self.coord_3D_pg  ## For measuring distance travelled per frame
        self.prev_coord_3D_2 = self.coord_3D_pg 
        self.prev_ticks = 0
        self.tick_duration = 0.1 # Avoid division by zero initially

     
    #### Functions ####
        
    def update_kpi_metrics(self, master_z, coord_3D_pg):
        self.master_z = master_z
        self.coord_3D_pg = coord_3D_pg
        
        ## Force a delay in updating mph, height etc., so it updates slow enough to be readable
        ticks = pygame.time.get_ticks()
        
        if ticks - self.prev_ticks > 100: ## 40 = 0.04 seconds delay between updates
            self.prev_coord_3D_2 = self.prev_coord_3D 
            self.prev_coord_3D = self.coord_3D_pg
            self.tick_duration = ticks - self.prev_ticks ## To calculate mph
            self.prev_ticks = ticks
            
            self.update_velo_mph()
            self.update_2D_distance_from_home_feet()
            self.update_height()
        
        packaged_returnable = {"velo": self.curr_velo_mph, "distance": self.curr_distance_from_home_feet, "height": self.curr_height_feet, "max height":  self.max_height_feet}
        
        return packaged_returnable

    ## Velocity in 3 directions
    def update_velo_mph(self): 
        
        duration_seconds = self.tick_duration / 1000
        
        distance_pixels = self.helpers.measure_3D_distance_in_pixels( self.prev_coord_3D, self.prev_coord_3D_2  ) 
        distance_feet = distance_pixels / self.setup.pixels_per_foot

        feet_per_second = distance_feet * (1 / duration_seconds) # It's running about 0.110 seconds between duration intervals, so about 9*the distance = the distance in 1 second
        self.curr_velo_mph = feet_per_second * (3600/5280)
        
        
    def update_2D_distance_from_home_feet(self):
        start_coord = self.setup.base_centroids[4]
        end_coord = self.coord_3D_pg[:2]
        self.curr_distance_from_home_feet = self.helpers.measure_distance_in_feet(start_coord, end_coord)
        

    def update_height(self):
        self.curr_height_feet = self.master_z / self.setup.pixels_per_foot
        self.max_height_feet = max(self.max_height_feet, self.curr_height_feet)



    ## something I used to help configure bounces off the OF wall 
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


    # Last line