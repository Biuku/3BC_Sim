""" April 11, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

    This module will contain the coordinates and initial positions. 
    
"""

import pygame
import numpy as np
from man import Man

pygame.init()

class Setup:
    def __init__(self):
        
        #Boundaries
        self.x_centre_line = 950
        self.lf_corner = (103, 390)
        self.cf_wall = (self.x_centre_line, 35)
        self.rf_corner = (1780, 410)
        self.four_B_tip = (self.x_centre_line, 1245)

        ## OF positions
        self.mid_depth_OF = 550
        self.LF = (550, self.mid_depth_OF)
        self.CF = (self.x_centre_line, 350)
        self.RF = (1350, self.mid_depth_OF)
        
        ## IN coordinates
        self.y_infield_middle_line = 1055
        self.base_size = 10  ## 10 this is much smaller than diamond.png shows the bases, but converts to 3.6' square
        
        ## Conversion factors
        self.pixels_per_foot = 2.8088 ## Calculated in Google Sheets by averaging distance between 1B-3B and 2B-Home 
        self.pixels_per_step = self.pixels_per_foot * 2.5 
     
        
        self.font14 = pygame.font.Font(None, 14)
        self.font15 = pygame.font.Font('freesansbold.ttf', 15)
        
    ## Hard coded coordinates for the OF corners, CF wall, and tip of home plate
    def get_boundaries(self):
        pos_boundaries = {  "lf_corner":    (103, 390), 
                             "cf_wall":     (self.x_centre_line, 35), 
                             "rf_corner":   (1780, 410), 
                             "four_B_tip":  (self.x_centre_line, 1245)
                        }
        return pos_boundaries 
        
        
    ## Hard coded coordinates for the centre-of-mass of each of the 4 bases    
    def get_base_centroids(self):
        
        base_centroids = {"one_B":  (1130, self.y_infield_middle_line),      
                        "two_B":    (self.x_centre_line, 880),
                        "three_B":  (768, self.y_infield_middle_line),
                        "four_B":   (self.x_centre_line, 1235), 
                        'rubber_P':   (self.x_centre_line, self.y_infield_middle_line - 5),
                         }
        
        return base_centroids


    ## Build the Rects for collision detection at the 4 bases 
    def make_bases(self, base_centroids):

        base_offset = self.base_size // 2
        base_rects = []
        
        for base_centroid in base_centroids.values():
            
            # Rect = left, top, width, height
            base = pygame.Rect(base_centroid[0]-base_offset, base_centroid[1]-base_offset, self.base_size, self.base_size)
            base_rects.append(base)
        
        return base_rects
    
   
    def get_pos_standard(self, base_centroids):
        
        """ Baseball strategies, ABA, p.229 --> NW, NE
        3: 9 over, 12 back --> (9, 12)
        4: 5 over, 15 back --> (-5, 12)
        5: 7 over, 12 back --> (12, 7)
        6: 7 over, 15 back --> (15, -7)
        """              
        
        ## Get pos for INF f3 - f6 
        inf_steps_adjust = {"f3": [(9, 12), "one_B" ],
                            "f4": [(-5, 12), "two_B"],
                            "f5": [(12, 7), "three_B"], 
                            "f6": [(15, -7), "two_B"], 
                            }

        pos_standard = {}
        
        for key, value in inf_steps_adjust.items():
            steps = value[0]            
            base_id = value[1]    
            old_coord = base_centroids[base_id]
            
            new_coord = self.convert_steps_to_pos(old_coord, steps) 
            
            pos_standard[key] = new_coord


        ## Get pos for f1, f2
        pos_standard['f1'] = base_centroids['rubber_P']
        pos_standard['f2'] = base_centroids['four_B']
        
        ## Get pos for OF
        pos_standard['f7'] = self.LF
        pos_standard['f8'] = self.CF
        pos_standard['f9'] = self.RF
        
        return pos_standard
  
    
    ## Create 9 instances of 'Man' object and return in a dict -- f1 to f9 
    def make_fielders(self, pos_standard, screen):
        fielder_ids = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9']

        fielder_objects = {}
        
        for fielder_id in fielder_ids:
        
            pos = pos_standard[fielder_id]                
            fielder_objects[fielder_id] = Man(screen, pos, fielder_id, "fielder")
            
        return fielder_objects

    
    def get_pos_situations(self, base_centroids):
        sprite_size = 32 - 13 # Playing with numbers to get the fielder very close to where he needs to be 
        base_offset = self.base_size//2
        B1 = base_centroids['one_B'] 
        B2 = base_centroids['two_B']
        B3 = base_centroids['three_B']
        rubber = base_centroids['rubber_P']
                
        ## Cover 1B
        cover_1B = (B1[0] - (17 + sprite_size), B1[1] - sprite_size)
        
        ## Cover 2B
        cover_2B = (B2[0] + (17 - sprite_size + 10), B2[1] - sprite_size)
        
        ## 4 cutoff to 2B -- should be based on the ball's location, but for now just static 
        steps = (-1, 40) #NW, NE
        cutoff_9_4 = self.convert_steps_to_pos(B2, steps) 
        
        ## 5 covers 3B
        cover_3B = (B3[0] , B3[1] - sprite_size)
        
        ## 1 backs up 2B
        steps = ( 12, 4 ) #NW, NE
        backup_1_2B = self.convert_steps_to_pos(rubber, steps)   #(B2[0] -30, B2[1] + 55)

        ## 7 backs up 2B from RF throw
        steps = (20, -15)  #NW, NE
        backup_7_2B = self.convert_steps_to_pos(B2, steps) 

        ## Catcher trails the runner to 1B 
        trail_runner_1B = (B1[0] + 25, B1[1] + 45)
                
         
        pos_situations = {"cover_3_1B": cover_1B, 
                          "cutoff_4_2B": cutoff_9_4,
                          "cover_6_2B": cover_2B, 
                          "backup_1_2B": backup_1_2B,
                          'trailRunner_2_1B': trail_runner_1B,
                          'cover_5_3B': cover_3B,
                          "backup_7_2B": backup_7_2B,              
                          }

        return pos_situations
   
                
    ## Do trionometry to convert 'steps over' and 'steps back' in baseball to Pygame coordinates   
    def convert_steps_to_pos(self, old_coord, steps): 
        
        # 1. Get delta_x and delta_y for 'steps over' and same for 'steps back' -- ignore direction for now / only positive 
        nw_feet_abs = np.sqrt( (steps[0] **2)/2 )
        ne_feet_abs = np.sqrt( (steps[1] **2)/2 )
        
        # 2. Package these deltas into an np array
        feet_abs = np.array([ [nw_feet_abs, nw_feet_abs], [ne_feet_abs, ne_feet_abs] ])
           
        # 3. Apply direction to all 4 deltas  
        direction_constants = np.array([ [-1, -1 ],  [1, -1] ])    # NW = -x, -y | NE = x, y
        
        NW_direct = np.sign( steps[0] )
        NE_direct = np.sign( steps[1] )
        step_directions = np.array([ [NW_direct, NW_direct], [NE_direct, NE_direct] ])
                                             
        direction_factors = step_directions * direction_constants
      
        all_delta_xy = feet_abs * direction_factors
            
        # 4. Sum x's and y's to get one delta for each -- superposition
        x = np.sum(all_delta_xy[:, 0])
        y = np.sum(all_delta_xy[:, 1])
        
        # 5. Recombine and convert to pixels 
        super_deltas = np.array([ x, y]) * self.pixels_per_step        
        
        # 6. Return absolute pos
        return old_coord + super_deltas
    