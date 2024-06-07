""" MAY 20 -- Baseball rules engine

Separating out the baserunner class -- it was getting cumbersome

"""


import pygame
from pygame.locals import *
import math


pygame.init()


class Baserunner:
    
    def __init__(self, name, curr_base = 0):
        
        self.name = name
        
        ## Base info
        self.occupied = curr_base
        self.prev_occupied = curr_base
        
        self.forced_status = False
        self.master_rights = {0: False, 1: False, 2: False, 3: False, 4: False}
        
        self.scored_status = False
        self.out_status = False


    for update_status in range(1):
        
        def reset_master_rights(self):
            self.master_rights = {0: False, 1: False, 2: False, 3: False, 4: False}

        ## Only update rights upon attaining a new base
        def update_rights(self, bases_with_runner_li):
            
            if self.forced_status:
                return

            self.reset_master_rights()
            curr = self.prev_occupied
            
            for base in [curr - 1, curr, curr + 1]:
                if base not in bases_with_runner_li:
                    self.master_rights[base] = True
                    
            ## If I'm not in the middle of a force play, or the guy behind me hasn't taken my base  
            if self.occupied:
                self.master_rights[self.occupied] = True


    for runner_actions in range(1):
        
        def advance_fwd(self):
            next_base = self.prev_occupied + 1
            
            if self.master_rights[next_base]:
                self.attain_base(next_base)


        def attain_base(self, base):
            if base == 4:
                self.score_run()
                return

            self.occupied = base
            self.prev_occupied = base


        def score_run(self):
            self.reset_master_rights()
            self.scored_status = True


        def apply_force(self, forced_base):
            self.forced_status = True
            
            self.reset_master_rights()           
            self.master_rights[forced_base] = True
            
            ## By definition, "forced" means there is only 1 base the runner has a right to
            self.occupied = None  ## This is actually not correct in FB situations -- R2 has still attained 2B. Unsure if that affects functionality
            
            
        def remove_force(self, bases_with_runner_li):
            self.forced_status = False
            self.update_rights(bases_with_runner_li)
            
            if self.master_rights[self.prev_occupied]: ## If I have the right to my old attained base (not occupied), make it my currently attained base
                self.occupied = self.prev_occupied

