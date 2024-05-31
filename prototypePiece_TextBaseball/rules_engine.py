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
        
        """ Previous stuff I still need """            

        self.screen_printer = ScreenPrinter(screen, self.name_map)

        ### User input stuff
        self.input_primary = None
        self.input_runner = None
        self.input_base = None


    #### Functions ####
    

    for control_baseball_actions in range(1): 
        
        def master_do_stuff(self):
            self.screen_print()


    for execute_baseball_actions in range(1): 
        pass
                

    for update_force_sitations in range(1):
        pass


    for user_input in range(1):

        
        def update_primary_user_input(self, var):
            self.input_primary = var
                    

        def update_secondary_user_input(self, var):
            
            if type(var) == str:
                self.update_runners_user_input(var)
                
            if type(var) == int:
                
                ## Directly update the state 
                if self.input_primary == 's':
                    self.update_state(var)
                    
                else: 
                    self.input_base = var 
                    

        def update_state(self, new_state):
            self.state = new_state
            
                

        def update_runners_user_input(self, runner_key):
            self.input_runner = self.name_map[runner_key]



    for functional_gets in range(1):
        pass

   
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
     
            #base_occupants = self.get_base_occupants_text()
            base_occupants = None
            #runners_out = self.get_runners_out()
            
            self.screen_printer.left_side(primary, runner, base)
            self.screen_printer.right_side(state, base_occupants)

    
        """    
        def get_base_occupants_text(self):
            #Used to print 'who's on first'.
            #Returns a Dict of only the occupied bases as keys and runner names as values

            base_runnerObject_dict, _ = self.get_occupied_bases()
            new_dict = {}
            
            for base, status in base_runnerObject_dict.items():
                if status:
                    new_dict[base] = base_runnerObject_dict[base].name

            return new_dict
             
        def get_runners_out(self):
            
            runners_out = []
            
            for runner in self.runners:
                if runner.out_status:
                    runners_out.append(runner.name)
        """
                    


""" ************************** MAIN ************************** """


for user_input_validation in range(1):
    
    alphabet_li = list('abcdefghijklmnopqrstuvwxyz')
    pg_alpha_key_dict = {}
    
    for i in range(1, 27):
        pg_alpha_key_dict[i + 96] = alphabet_li[ i - 1]


game = Game()

#dudes = {'Isaac': 2, 'Jack': 1} # , 'Josh': 0
#game.make_baserunners(dudes)


exit = False

primary_user_input = None

""" 
None = get primary user input >
's' = change state > 
    0, 1, 2 = state
'r' = tag runner > 
    str
'b' = tag base > 
    int
'o' = occupy base > 
    int
    str
'c' = create runner >
    int
'x' = reset user input > 
"""

while not exit:
    
    screen.fill('white')
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit = True
            
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                exit = True
            
            ## Primary input
            if event.key == K_x:
                game.update_primary_user_input(None)
                game.input_runner = None
                game.input_base = None

                
            if not(game.input_primary):
                if event.key in [K_s, K_r, K_b, K_o, K_c]:
                    primary_key = pg_alpha_key_dict[event.key]
                    game.update_primary_user_input(primary_key)


            ## Secondary input
            else:
                ## Base # keys and state keys
                if event.key in [K_0, K_1, K_2, K_3, K_4]:
                    int_key = event.key - 48
                    game.update_secondary_user_input(int_key)
                
                ## Baserunner keys
                if event.key in [K_i, K_j, K_d, K_r, K_c, K_s, K_p, K_b, K_k, K_f, K_l]:
                    runner_key = pg_alpha_key_dict[event.key]
                    game.update_secondary_user_input(runner_key)
            
            ## Overall
            """
            if event.key == K_SPACE:
                game.update_startStop_user_inputs('space')
            
            if event.key == K_RETURN:
                game.update_startStop_user_inputs('return')
            """

    game.master_do_stuff()
    pygame.display.update() 


# Last line