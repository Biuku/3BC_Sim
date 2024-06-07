""" MAY 17 -- Baseball rules engine

Want to isolate just baserunning rules that are relevant to this. Basically, how to encode force-play rules and other complexities of baserunning.

After I get it working here, I may embed the functionality in each baserunner 

"""


import pygame
from pygame.locals import *
import math

#from helpers import Helpers
#from setup import Setup
from screen_printer_temp import ScreenPrinter
from temp_baserunner import Baserunner


import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(1, 30) # Opens Pygame to top-left of monitor


pygame.init()
w = 2000 #3400 #= optimal for my widescreen
h = 1350
screen = pygame.display.set_mode( (w, h) )



class Game:
    
    def __init__(self):

        self.screenPrinter = ScreenPrinter(screen)
        
        self.runners = []
        self.runners_who_scored = []
        self.tagable_bases_dict = {1: False, 2: False, 3: False}
    
        ### User input stuff
        
        self.input_primary = None
        self.input_secondary = None
        
        self.runners_to_act = []
        self.runner_direction = None
        
        self.player_out_flag = False
        
        self.game_state = 0 
        self.game_state_index = {0: "Pre pitch", 1: "Start bip", 2: "BIP", 3: "Finish bip" }
        
        
        self.prev_ticks = 0


    #### Functions ####
    
    ## Instantiate
    
    def make_baserunners(self, dudes):
        self.runners = [Baserunner(name, base) for name, base in dudes.items()]
        self.refresh_runner_rights()


    for control_baseball_actions in range(1): 
        
        def master_do_stuff(self):
            
            self.refresh_runner_rights()
            
            self.start_bip() # Game state 1
            self.in_bip() # Game state 2
            self.finish_bip() # Game state 3 
            
            self.screen_print()

            """if pygame.time.get_ticks() - self.prev_ticks > 500:
                    self.prev_ticks = pygame.time.get_ticks()"""


        def start_bip(self):
            if not self.game_state == 1:
                return

            self.update_forced()
            self.game_state = 2
        
        
        def in_bip(self):
            if not self.game_state == 2:
                return
            
            if self.player_out_flag and self.runners_to_act:
                for runner in self.runners:
                    if runner.name in self.runners_to_act:
                        runner.out_status = True
                
                self.player_out_flag = False
            

        def finish_bip(self):
            if not self.game_state == 3:
                return
            
            self.advance_runners()
            self.refresh_runner_rights()
            self.reset_situation()


    for execute_baseball_actions in range(1): 
                
        def advance_runners(self):

            self.refresh_runner_rights()
            
            for base in [3, 2, 1]:
                
                for runner in self.runners:
                    
                    if base == runner.prev_occupied:

                        potential_run_flag = False

                        if runner.forced_status:
                            runner.attain_base(base + 1) ## Force a forced runner to the next base, starting with the lead runner
                            potential_run_flag = True

                        elif runner.name in self.runners_to_act:  
                            
                            runner.advance_fwd()   ## For now, ignore which direction -- assume fwd
                            potential_run_flag = True

                        if potential_run_flag:  
                            if runner.scored_status:
                                self.runners_who_scored.append(runner) 
                                self.runners.remove(runner)

                    self.refresh_runner_rights()

        
        def refresh_runner_rights(self):
            
            self.remove_forces()
            
            base_runnerObject_dict, bases_with_runner_li = self.get_occupied_bases()
            
            for base in [3, 2, 1]:
                runner = base_runnerObject_dict[base]
                if runner:
                    runner.update_rights(bases_with_runner_li)

        
    for update_force_sitations in range(1):

        def update_forced(self):
            base_runnerObject_dict, bases_with_runner_li = self.get_occupied_bases()
            bases_forced_to = {1: True, 2: False, 3: False, 4: False}
            
            self.reset_bases()
            
            # 1. Apply forces where applicable 
            for base in range(1, 4):
                runner = base_runnerObject_dict[base]
                if runner:
                    if bases_forced_to[base]:
                        
                        bases_forced_to[base + 1] = True
                        self.apply_force(runner, base + 1)


        def apply_force(self, runner, forced_base):
            runner.apply_force(forced_base)

            if forced_base in self.tagable_bases_dict:
                self.tagable_bases_dict[forced_base] = runner.name

        
        def remove_forces(self):
            #Always remove all forces between plays -- i.e., at state 0 = pre-pitch
            base_runnerObject_dict, bases_with_runner_li = self.get_occupied_bases()
            
            for runner in self.runners:
                runner.remove_force(bases_with_runner_li)


    for user_input in range(1):
        
        def update_primary_user_input(self, var):
            self.input_primary = var


        def update_secondary_user_input(self, var):
            self.input_secondary = var
            
            if var in list("ijd"):
                self.update_runners_to_act_user_input(var)
                
            if var in [0, 9]:
                self.runner_direction = var

            
        def update_runners_to_act_user_input(self, var):
            lookup = {'i': "Isaac", 'j': "Jack", 'd': "Josh"}
            new_runner = lookup[var]
            
            if new_runner in self.runners_to_act: ## Prevent adding same guy twice
                return
            
            self.runners_to_act.append( new_runner )


        def update_startStop_user_inputs(self, var):
            
            ## Turn on the flag to start a play -- ball in play so forced runners lose right to occupied base 
            if var == 'space':
                self.game_state = 1

            ## Turn on flag to finish a play -- everyone reaches bases they had the rights to 
            if var == 'return':
                self.game_state = 3 

            ## Reset situation 
            if var == 'r':
                self.reset_situation()
                
            if var == 'o':
                print("you pressed O")
                self.player_out_flag = True


    for reset_stuff in range(1):

        def reset_bases(self):
            self.tagable_bases_dict = {1: False, 2: False, 3: False}

        def reset_situation(self):
            self.input_primary = None
            self.input_secondary = None
            self.runners_to_act = []
            self.game_state = 0


    for functional_gets in range(1):

        def get_occupied_bases(self):
            
            """ Obtains info directly from runners (Runners = source of truth). Returns: 
            a) A Dict of bases 1-4 where values are either False for empty base or the runner object
            b) A list with an integer for each attained base """
            
            base_runnerObject_dict = {1: False, 2: False, 3: False, 4: False}
            bases_with_runner_li = []
            
            for runner in self.runners:
                if runner.occupied:
                    base_runnerObject_dict[runner.prev_occupied] = runner ## a dict with the runner objects at the correct base  
                    bases_with_runner_li.append(runner.prev_occupied) ## a list of only the bases that have a runner
            
            return base_runnerObject_dict, bases_with_runner_li

   
    for screen_print in range(1):

        def screen_print(self):  
            
            ## Setup stuff      
            primary = self.input_primary
            secondary = self.input_secondary
            sit_state = self.game_state_index[self.game_state]
            scored = self.runners_who_scored
            
            base_occupants = self.get_base_occupants_text()
            runner_rights = self.get_runner_rights_text()
            runners_out = self.get_runners_out()
            
            screen_printer.left_side(primary, secondary, self.runners_to_act)
            screen_printer.right_side(sit_state, base_occupants, scored, runners_out, runner_rights, self.tagable_bases_dict)
    
    
        def get_base_occupants_text(self):
            """ 
            Used to print 'who's on first'.
            Returns a Dict of only the occupied bases as keys and runner names as values
            """
            base_runnerObject_dict, _ = self.get_occupied_bases()
            new_dict = {}
            
            for base, status in base_runnerObject_dict.items():
                if status:
                    new_dict[base] = base_runnerObject_dict[base].name

            return new_dict
            

        def get_runner_rights_text(self):
            
            runner_rights = {}
            
            for runner in self.runners:
                name = runner.name
                forced_status = runner.forced_status
                
                rights_string = ""
                
                for base, right in runner.master_rights.items():
                    if right and base > 0:
                        rights_string += str(base) + "B "
                        
                runner_rights[name] = {"Rights": rights_string, "Forced status": forced_status}
                
            return runner_rights 
            
        def get_runners_out(self):
            
            runners_out = []
            
            for runner in self.runners:
                if runner.out_status:
                    runners_out.append(runner.name)

""" ************************** MAIN ************************** """



for user_input_validation in range(1):
    
    ## a = 97 > start at 
    alpha_zero = 96
    alphabet_li = list('abcdefghijklmnopqrstuvwxyz')
    pg_alpha_key_dict = {}
    
    for i in range(1, 27):
        pg_alpha_key_dict[i + alpha_zero] = alphabet_li[ i - 1]


game = Game()

dudes = {'Isaac': 2, 'Jack': 1} # , 'Josh': 0
game.make_baserunners(dudes)


screen_printer = ScreenPrinter(screen)


exit = False

while not exit:
    
    screen.fill('white')
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit = True
            
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                exit = True
            
            ## Primary input
            if event.key in [K_c, K_a, K_f]:
                primary_key = pg_alpha_key_dict[event.key]
                game.update_primary_user_input(primary_key)

            ## Secondary input
            if event.key in [K_0, K_1, K_2, K_3, K_8, K_9]:
                runner_key = event.key - 48
                game.update_secondary_user_input(runner_key)
                
            if event.key in [K_i, K_j, K_d]:
                runner_key = pg_alpha_key_dict[event.key]
                game.update_secondary_user_input(runner_key)
            
            ## Overall    
            if event.key == K_SPACE:
                game.update_startStop_user_inputs('space')
            
            if event.key == K_RETURN:
                game.update_startStop_user_inputs('return')
            
            if event.key == K_r:
                game.update_startStop_user_inputs('r')
                
            if event.key == K_o:
                game.update_startStop_user_inputs('o')


    game.master_do_stuff()
    pygame.display.update() 


# Last line

