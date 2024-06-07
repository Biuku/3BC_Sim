""" MAY 29 -- Baseball rules engine

The first version of this was created May 17. It got too heavy so I went to Jupyter to get the core of the core clean. 
The core of the core clean... 
I finally did that May 28.
Now, May 29 -- JFK's birthday -- I'm going to start migrating the Jupyter code into this, keeping the nice user interface. But also adapting it for Pygame.

"""


import pygame
from pygame.locals import *
import math

#from helpers import Helpers
#from setup import Setup
from screen_printer_temp import ScreenPrinter
from baserunner import Baserunner
from RuEg_functions import ApplyForces, RemoveForces, CreateRunner, Occupy


import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(1, 30) # Opens Pygame to top-left of monitor


pygame.init()
w = 2000 #3400 #= optimal for my widescreen
h = 1350
screen = pygame.display.set_mode( (w, h) )


class Game:
    
    def __init__(self):

        """ Jupyter stuff """
        self.af = ApplyForces()
        self.rf = RemoveForces()
        self.cr = CreateRunner()
        self.oc = Occupy()
        
        self.state = -1 ## Initial state

        self.names = ['Isaac', 'Jack', 'JD', 'Romo', 'Casey', 'Sam', 'Pasma', 'Bradey', 'Kemper', 'Liam', "Leo"]
        self.name_map = {'i': 'Isaac', 'j': 'Jack', 'd': 'JD', 'r': 'Romo', 'c': 'Casey', 's': 'Sam', 'p': 'Pasma', 
                         'b': 'Bradey', 'k': 'Kemper', 'l': 'Liam', 'l': "Leo"} ## For user input
        self.runners = {} # {name: object}
        self.batter = None
        
        self.runners_out = []
        
        """ Previous stuff I still need """            

        self.screen_printer = ScreenPrinter(screen, self.name_map)

        ### User input stuff
        self.input_primary = None
        self.input_runner = None
        self.input_base = None
        self.input_state = None
        self.batter = None
        
        self.UI_submit_flag = False


    #### Functions ####

    for control_baseball_actions in range(1): 
        
        def master_do_stuff(self):
            
            if self.UI_submit_flag and self.input_primary:
                func_map = {'r': self.fielder_tags_runner, 'b': self.fielder_tags_base, 'o': self.occupy_attain_base, 
                        's': self.change_state, 'c': self.create_runner}
                
                key = self.input_primary
                func_map[key]()  # Call the function associated with the key
                
                self.UI_submit_flag = False
                self.reset_user_input()

            self.screen_print()


        def change_state(self):
            if type(self.input_state) == str:
                return 

            self.state = self.input_state
            
            if self.state == 0:
                print("State updated to 0: Pre-pitch")
                self.state = 0
                
            elif self.state <= 2:
                
                self.state_12()
                    
                if self.state == 1: # 1 = BIP
                    print("State updated to 1: BIP")
                    self.runners = self.af.apply_forces(self.batter, self.runners)

                elif self.state == 2: # 2 = FBC
                    self.state_fbc()
                    
            
        def state_12(self):
            
            ## All BR de-occupy their base
            for name, runner in self.runners.items():
                runner.occupied_base = None

            ## Instantiate a batter at base 0
            name = self.names.pop(0)
            self.batter = self.cr.create_batter(name)
            self.runners[name] = self.batter

            
        def state_fbc(self):
            print("Sub-state updated to: FBC", end = " | ")

            self.put_out(self.batter)
            
            for runner in self.runners.values():
                runner.tagup_base = runner.attained_base


        def create_runner(self):
            name = self.names.pop(0)
            base = self.input_base
            
            runner = self.cr.create_runner(name, base)
            self.runners[name] = runner 
            

    for execute_baseball_actions in range(1): 
    
               
        def fielder_tags_runner(self):
            name = self.input_runner
            runner = self.runners[name]

            out_tracer = False

            if not(runner.occupied_base):
                self.put_out(runner)
                out_tracer = True

            print(f"\nFielder tagged {name} for Out = {out_tracer}")
                
               
        def fielder_tags_base(self):
            tagged_base = self.input_base
        
            for runner in self.runners.values():
                if runner.f2_base == tagged_base or runner.tagup_base == tagged_base:
                    self.put_out(runner)
                    print(f"Fielder tagged {tagged_base} to put {runner.name} out.")
                    
                    return


        def occupy_attain_base(self):
            
           if self.runners:
               self.runners = self.oc.occupy_attain_base(self.input_runner, self.input_base, self.runners)


        def put_out(self, runner_out):
            """ Pass the runner object being put out """
                    
            self.runners = self.rf.remove_forces(runner_out, self.runners) # Remove forces for preceding BR        
            del self.runners[runner_out.name] # Delete runner from list of runners
            self.names.append(runner_out.name) # Recycle the name
            self.runners_out.append(runner_out)

            print(f"{runner_out.name} is Out.\n")


    for user_input in range(1):

        def update_primary_user_input(self, var):
            self.input_primary = var


        def update_secondary_user_input(self, var):
            
            ## Directly update the state 
            if self.input_primary == 's':
                self.input_state = var
                 
            elif type(var) == int: 
                self.input_base = var
                
            elif type(var) == str:
                self.input_runner = self.name_map[var]


        def reset_user_input(self):
            self.input_primary = None
            self.input_runner = None
            self.input_base = None
            self.input_state = None


    for screen_print in range(1):

        def screen_print(self): 
            primary_map = {'s': 'State', 'r': "Tag runner", 'b': 'Tag base', 'o': 'Occupy base', 'c': 'Create baserunner'}
            
            ## Setup stuff
            primary = None
            if self.input_primary:
                primary = primary_map[self.input_primary]
                
            runner = self.input_runner
            base = self.input_base
            state = self.state
            runners_out = self.runners_out
            base_occupants = self.get_base_occupants_text()
            runner_status = self.get_runner_status_text()
    

            self.screen_printer.left_side(primary, runner, base)
            self.screen_printer.right_side(state, base_occupants, runner_status, runners_out)


        def get_base_occupants_text(self):

            bases = {0: None, 1: None, 2: None, 3: None}

            for name, runner in self.runners.items():
                base = runner.attained_base
                bases[base] = name 
                
            return bases
        
        
        def get_runner_status_text(self):
            
            temp_runners = {}
            
            ## Build a dictionary of attributes (as str's) for each runner
            for name, runner in self.runners.items():
                sub_dict = {}
                
                sub_dict["Attained"] = runner.attained_base
                sub_dict["Occupied"] = runner.occupied_base
                sub_dict["Forced-to"] = runner.f2_base
                sub_dict["Tag-up"] = runner.tagup_base
                
                ## If the base is not None, add "B", else, make it "-"
                for key, value in sub_dict.items():
                    if value:
                        sub_dict[key] = str(value) + "B" 
                    else:
                        sub_dict[key] = "-"
                        
                temp_runners[name] = sub_dict

            return temp_runners


""" ************************** MAIN ************************** """


for user_input_validation in range(1):
    
    alphabet_li = list('abcdefghijklmnopqrstuvwxyz')
    pg_alpha_key_dict = {}
    
    for i in range(1, 27):
        pg_alpha_key_dict[i + 96] = alphabet_li[ i - 1]

game = Game()
exit = False

while not exit:
    
    screen.fill('white')
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit = True
            
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                exit = True

            if event.key == K_x:
                game.reset_user_input()

            ## Primary input
            if not(game.input_primary):
                
                if event.key in [K_s, K_r, K_b, K_o, K_c]:
                    primary_key = pg_alpha_key_dict[event.key]
                    game.update_primary_user_input(primary_key)
                    print(f"Primary key: {primary_key}")

            ## Secondary input
            else:
                ## Base and state keys -- int
                if event.key in [K_0, K_1, K_2, K_3, K_4]:
                    int_key = event.key - 48
                    game.update_secondary_user_input(int_key)
                    print(f"secondary key: {int_key}")
                
                ## Baserunner keys -- str
                if event.key in [K_i, K_j, K_d, K_r, K_c, K_s, K_p, K_b, K_k, K_f, K_l]:
                    chr_key = pg_alpha_key_dict[event.key]
                    game.update_secondary_user_input(chr_key)
                    print(f"secondary key: {chr_key}")

            ## Submit UI flag
            if event.key == K_SPACE:
                game.UI_submit_flag = True

    game.master_do_stuff()
    pygame.display.update() 

# Last line