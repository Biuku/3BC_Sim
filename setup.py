""" April 11, 2024 -- THIRD-BASE COACH SIMULATOR. A project to train 3B-C decision making in high school baseball, using PyGame.

    This module will contain the coordinates and initial positions. 
    
"""

import pygame
import numpy as np
from man import Man

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
        self.base_size = 25
        
        
        self.arrondissements_font = pygame.font.Font('freesansbold.ttf', 20)

        
    def steps_to_pos(self, old_coord, steps, steps_posNeg):
        pixels_per_step = 7
        
        over_a = np.sqrt( (steps[0] **2)/2 )
        back_a = np.sqrt( (steps[1] **2)/2 )
        
        adjust = np.array([ [over_a, over_a], [back_a, back_a]])
        
        all_xy = adjust * steps_posNeg
        
        #sum x's and y's
        x = np.sum(all_xy[:, 0])
        y = np.sum(all_xy[:, 1])
        
        # Convert to pixels
        adjust = np.array([ x, y]) * pixels_per_step
            
        # return absolute pos 
        return old_coord + adjust


    def get_pos_standard(self, base_centroids):
        inf_steps_adjust = {"f3": [(9, 12),   [(-1, -1), (1, -1)],  "one_B" ],
                            "f4": [(-5, 12),  [(1, 1), (1, -1)],    "two_B"],
                            "f5": [(7, 12),   [(1, -1), (-1, -1)],  "three_B"], 
                            "f6": [(-7, 15),  [(-1, 1), (-1, -1)],  "two_B"], 
                            }
        pos_standard = {}

        for key, value in inf_steps_adjust.items():
            steps = value[0]
            steps_posNeg = np.array(value[1])
            
            base_id = value[2]    
            old_coord = base_centroids[base_id]
            
            new_coord = self.steps_to_pos(old_coord, steps, steps_posNeg)
            
            pos_standard[key] = new_coord

        pos_standard['f1'] = base_centroids['rubber_P']
        pos_standard['f2'] = base_centroids['four_B']
        pos_standard['f7'] = self.LF
        pos_standard['f8'] = self.CF
        pos_standard['f9'] = self.RF
        
        return pos_standard
    
    
    
    def get_pos_situations(self, base_centroids):
        sprite_size = 32 - 13 # Playing with numbers to get the fielder very close to where he needs to be 
        base_offset = self.base_size//2
        
        ## Cover 1B
        f3 = base_centroids['one_B'] 
        f3 = (f3[0] - (17 + sprite_size), f3[1] - sprite_size)
        
        ## Cover 2B
        f6 = base_centroids['two_B']
        f6 = (f6[0] + (17 - sprite_size + 10), f6[1] - sprite_size)
        
        
        ## 4 cutoff to 2B -- should be based on the ball's location, but for now just static 
        f4 = base_centroids['two_B']
        steps_over = 1
        steps_back = 40
        steps_posNeg = np.array([ [1, 1], [1, -1] ])
         
        f4 = new_pos = self.steps_to_pos(f4, (steps_over, steps_back), steps_posNeg)
         
        pos_situations = {"cover_3_1B": f3, 
                          "cutoff_4_2B": f4,
                          "cover_6_2B": f6,}

        return pos_situations



    def get_boundaries(self):
        pos_boundaries = {  "lf_corner":    (103, 390), 
                             "cf_wall":     (self.x_centre_line, 35), 
                             "rf_corner":   (1780, 410), 
                             "four_B_tip":  (self.x_centre_line, 1245)
                        }
        return pos_boundaries 
        
        
        
    def get_base_centroids(self):
        base_centroids = {"one_B":  (1130, self.y_infield_middle_line),      
                        "two_B":    (self.x_centre_line, 880),
                        "three_B":  (768, self.y_infield_middle_line),
                        "four_B":   (self.x_centre_line, 1235), 
                        'rubber_P':   (self.x_centre_line, self.y_infield_middle_line - 5),
                         }
        return base_centroids

    
    
    def make_bases(self, base_centroids):

        base_offset = self.base_size // 2
        base_rects = []
        
        for base_centroid in base_centroids.values():
            # Rect = left, top, width, height
            base = pygame.Rect(base_centroid[0]-base_offset, base_centroid[1]-base_offset, self.base_size, self.base_size)
            base_rects.append(base)
        
        return base_rects
    
    
    
    def make_fielders(self, pos_standard, screen):
        fielder_ids = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9']

        fielder_objects = {}
        for fielder_id in fielder_ids:
            
            pos = pos_standard[fielder_id]
            new_pos = (pos[0] - 16, pos[1] -16) # Offset 32 pixel sprite to centre of position 
                
            fielder_objects[fielder_id] = Man(screen, new_pos, "fielder")
            
        return fielder_objects

        
   