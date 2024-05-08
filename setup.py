""" April 11, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

    This module will contain the coordinates and initial positions. 
    
"""

import pygame
import numpy as np

from ffielder import Fielder
from bbaserunner import Baserunner
from helpers import Helpers

pygame.init()

class Setup:
    def __init__(self, screen, w, h):
        
        self.screen = screen
        self.helpers = Helpers(screen)        
        self.screen_w = w
        self.screen_h = h

        ## Conversion factors
        self.pixels_per_foot = 2.8088 ## Calculated in Google Sheets by averaging distance between 1B-3B and 2B-Home 
        self.pixels_per_step = self.pixels_per_foot * 2.5 

        for boundaries in range(1):
            #Boundary coord
            self.x_centre_line = 950
            self.lf_foulPole = (58, 356) #(103, 390) <-- this was the warning track ...
            self.cf_wall = (self.x_centre_line, 35)
            self.rf_foulPole = (1839, 355) #(1780, 410)
            self.four_B_tip = (self.x_centre_line, 1245)
            self.main_centroid = (950, 1430) # This is the centre of the circle describing the OF wall / warning track (Not useful for foul lines)
            self.main_centroid_radius = self.helpers.measure_distance_in_pixels(self.main_centroid, self.cf_wall)

            # Boundary thetas -- from Home in degrees
            self.lf_foulPole_deg = 135
            self.cf_deg = 90
            self.rf_foulPole_deg = 45
            self.cf_left_deg = 105
            self.cf_right_deg = 75

        for field_positions in range(1):
            ## OF positions
            self.mid_depth_OF = 550
            self.LF = (550, self.mid_depth_OF)
            self.CF = (self.x_centre_line, 350)
            self.RF = (1350, self.mid_depth_OF)
            
            ## INF coordinates
            self.y_infield_middle_line = 1055
            self.base_size = 10  ## 10 this is much smaller than diamond.png shows the bases, but converts to 3.6' square
            self.base_centroids = self.get_base_centroids()
        
        for fonts_and_colours in range(1):  
            self.font12 = pygame.font.SysFont('Arial', 12) 
            self.font15 = pygame.font.SysFont('Arial', 15) #pygame.font.Font('freesansbold.ttf', 15)
            self.font20 = pygame.font.SysFont('Arial', 18)
            
            self.extremely_light_gray = (240, 240, 240)
            self.med_gray_c = (128, 128, 128)
            self.dark_gray_c = (47,47,47)
            self.green_grass_c = (65,152,10)
            self.extremely_light_blue_c = (225, 245, 245) 
        
        for ball_data in range(1): 
            self.top_of_floor = 1350 - 17
            self.ball_launch_z = self.top_of_floor - (4 * self.pixels_per_foot) ## 4'


    #### MAIN FUNCTIONS

    for boundaries in range(1):

        ## Hard coded coordinates for the OF corners, CF wall, and tip of home plate
        def get_boundaries(self):
            pos_boundaries = {  "lf_foulPole":    self.lf_foulPole, 
                                "cf_wall":     (self.x_centre_line, 35), 
                                "rf_foulPole":   self.rf_foulPole, 
                                "four_B_tip":  (self.x_centre_line, 1245),
                                "main_centroid": self.main_centroid,
                            }
            return pos_boundaries 
            

        def get_boundary_thetas(self):
            boundary_thetas = {
                                "lf_foulPole_deg": self.lf_foulPole_deg, 
                                "cf_deg": self.cf_deg,
                                "rf_foulPole_deg": self.rf_foulPole_deg,
                                "cf_left_deg": self.cf_left_deg,
                                "cf_right_deg": self.cf_right_deg,
                            }
            return boundary_thetas


    for field_positions in range(1):

        ## Hard coded coordinates for the centre-of-mass of each of the 4 bases    
        def get_base_centroids(self):
            
            base_centroids = {"one_B":  (1130, self.y_infield_middle_line),      
                            "two_B":    (self.x_centre_line, 880),
                            "three_B":  (768, self.y_infield_middle_line),
                            "four_B":   (self.x_centre_line, 1235), 
                            'rubber_P':   (self.x_centre_line, self.y_infield_middle_line - 5),
                            }
            
            return base_centroids

        def get_fielder_standard_coord(self, base_centroids):
            fielder_standard_coord = {}

            ## Coord for INF
            fielder_standard_coord[3] = (1144, 950) #fielder ID: 3  |  new_coord: (1144, 950)
            fielder_standard_coord[4] = (1034, 845) #fielder ID: 4  |  new_coord: (1034, 845)
            fielder_standard_coord[5] = (743, 960)  #fielder ID: 5  |  new_coord: (743, 960)
            fielder_standard_coord[6] = (840, 840)  #fielder ID: 6  |  new_coord: (840, 840)
            
            ## Get coord for f1, f2
            fielder_standard_coord[1] = base_centroids['rubber_P']
            fielder_standard_coord[2] = base_centroids['four_B'][0], base_centroids['four_B'][1]+40
            
            ## Get coord for OF
            fielder_standard_coord[7] = self.LF
            fielder_standard_coord[8] = self.CF
            fielder_standard_coord[9] = self.RF
            
            return fielder_standard_coord


    for make_objects in range(1):
        
        ## Build the Rects for collision detection at the 4 bases 
        def make_bases(self, base_centroids):

            base_offset = self.base_size // 2
            base_rects = {}
            
            for key, base_centroid in base_centroids.items():
                
                # Rect = left, top, width, height
                base = pygame.Rect(base_centroid[0]-base_offset, base_centroid[1]-base_offset, self.base_size, self.base_size)
                base_rects[key] = base
            
            return base_rects
        
        
        ## Create 9 instances of 'Man' object and return in a dict with keys as integers 1 to 9 
        def make_fielders(self, fielder_standard_coord, screen):

            fielder_objects = {}
            
            for fielder_id in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                pos = fielder_standard_coord[fielder_id]                
                fielder_objects[fielder_id] = Fielder(screen, pos, fielder_id)
                
            return fielder_objects
        
        
        def make_baserunners(self, screen):
            return Baserunner(screen, self.base_centroids)


    for defensive_sit in range(1):
        
        def get_defensiveSit_fielder_coord(self, base_centroids):
            sprite_size = 32 - 13 # Playing with numbers to get the fielder very close to where he needs to be 
            B1 = base_centroids['one_B'] 
            B2 = base_centroids['two_B']
            B3 = base_centroids['three_B']
            B4 = base_centroids['four_B']
            rubber = base_centroids['rubber_P']

            # 100   | 1 backs up 2B
            _100 = (B2[0] -40, B2[1] + 90)

            # 101      | Catcher trails the runner to 1B 
            _101 = (B1[0] + 25, B1[1] + 45)

            # 102   | 3 covers 1B
            _102 = (B1[0] - (17 + sprite_size), B1[1] - sprite_size)
            
            # 103   | 4 cutoff to 2B 
            _103 = (B2[0] + 200, B2[1] - 200)
            
            # 104   | 5 covers 3B
            _104 = (B3[0] , B3[1] - sprite_size)
    
            # 105   | 6 covers 2B
            _105= (B2[0] + (17 - sprite_size + 10), B2[1] - sprite_size)
            
            # 106   | 7 backs up 2B from RF throw
            _106 = (B2[0] - 180, B2[1] - 30)

            # 107    | cover_4_2B
            _107 = _105
            
            # 108    | cutoff_6_2B_CF
            _108 = (940, 670)
            
            # 109    | cutoff_6_2B_LF
            _109 = (750, 800)
            
            # 110    | backup_1_3B
            _110 = (775, 1085 )
            
            # 111    | cover_2_home
            _111 = B4

            # 112    | cutoff_4_3B
            _112 = (1070, 880)
            
            # 113    | cutoff_6_3B_CF
            _113 = (880, 700)
            
            # 114    | cutoff_6_3B_LF
            _114 = (620, 750)
            
            # 115    | backup_9_2B
            _115 = (1160, 880)
            
            # 116    | backup_1_home
            _116 = (950, 1300)
                
            # 117    | cutoff_3_home_CF
            _117 = (1000, 910)
            
            # 118    | cutoff_3_home_RF
            _118 = (1080, 980)
            
            # 119    | cutoff_5_home
            _119 = (840, 1030)
            
            # 120    | cover_6_3B
            _120 = _104
            
            # 121    | backup_7_3B
            _121 = (675, 1025)                

            
            """A Google Sheets file links it all together as follows:
                - There are about 15 Trosky plays. Each one prescribes an action for each defensive player
                - There's a lot of overlap, so I wrote down each action, numbering them from 100 onwards
                - The numbering has no significance -- the Google Sheets index is the menu
                - I manually found the coordinates for each defensive coverage action 
                - I will ultimately encode each defensive play, picking from this menu of actions 
            
            """ 

            defensiveSit_fielder_coord = {    
                    100: _100, 101: _101, 102: _102, 103: _103, 104: _104, 105: _105, 106: _106,
                    107: _107, 108: _108, 109: _109, 110: _110, 111: _111, 112: _112, 113: _113,
                    114: _114, 115: _115, 116: _116, 117: _117, 119: _118, 119: _119, 120: _120,
                    121: _121             
                    }

            """
            defensiveSit_fielder_coord = {    
                            100: _100,
                            1000: _1000,
                            103: _103,
                            1003: _1003,                         
                            106: _106,
                            1006: _1006,
                            }
            """
            return defensiveSit_fielder_coord


        def get_defensiveSit_plays(self):
        
            # Below, each defensive play is a key, and the list of 0-9 provides plays for all defensive players
            # 1 = field the ball
            # 2 = back up the guy fielding the ball
            # 0th position is the string description of the play
            
            defensiveSit_plays = {3: ["Nobody on, single to LF", 100, 101, 102, 107, 104, 109, 1, 2, 115],
                                4: ["Nobody on, single to CF", 100, 101, 102, 107, 104, 108, 2, 1, 2],
                                5: ["Nobody on, single to RF", 100, 101, 102, 103, 104, 105, 106, 2, 1],
                                6: ["R1, single to LF", 110, 111, 102, 107, 104, 114, 1, 2, 115],
                                7: ["R1, single to CF", 110, 111, 102, 107, 104, 113, 2, 1, 2],
                                8: ["R1, single to RF", 110, 111, 102, 112, 104, 105, 106, 2, 1],
                                9: ["R2, single to LF", 116, 111, 102, 107, 119, 120, 1, 2, 115],
                                10: ["R2, single to CF", 116, 111, 117, 107, 104, 113, 2, 1, 2],
                                11: ["R2, single to RF", 116, 111, 118, 112, 104, 105, 121, 2, 1],           
            }
                
            return defensiveSit_plays
