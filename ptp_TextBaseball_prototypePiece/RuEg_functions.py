import pygame
from pygame.locals import *
import math

from baserunner import Baserunner


pygame.init()


class ApplyForces:
    
    def apply_forces(self, batter, runners):
        
        f2bases = {1: batter, 2: False, 3: False, 4: False}
        
        for base in [1, 2, 3]:
        
            for runner in runners.values():
                attained = runner.attained_base
            
                if base == attained and f2bases[base]:
                    f2bases[ base + 1 ] = runner
                    runner.f2_base = base + 1
        
        return runners



class RemoveForces:
    
    def remove_forces(self, runner_out, runners):
        kill_force_base = runner_out.f2_base ## This is the base the 'runner_out' is forced to
        
        if kill_force_base:
        
            for base in range(kill_force_base, 5):

                for runner in runners.values():

                    if base == runner.f2_base:
                        runner.f2_base = None
            
        return runners



class CreateRunner:

    def create_batter(self, name):
        batter = self.create_runner(name, 0)
        batter.f2_base = 1
        
        return batter
        
        
    def create_runner(self, name, base):
        runner = Baserunner(name, base)
        print(f"Created {name} on {base}B")
        
        return runner



class Occupy:
    
    def occupy_attain_base(self, name, base, runners):
        runner = runners[name]

        print(f"\n{name} is attempting to occupy {base}B")

        ## Reject if base is too far away
        attained = runner.attained_base
        if abs(attained - base) > 1:
            print(f"{name} has attained {attained} and cannot occupy {base} because it's too far away")
            return runners

        ## Reject if base is occupied
        for br in runners.values():
            if br.occupied_base == base:
                print(f"Sorry, {base}B is occupied")
                return runners

        print(f"Woo hoo! {base}B is free.")

        ## Else, occupy & attain base 
        runner.attained_base = runner.occupied_base = base

        ## Clear taggable bases
        if runner.f2_base == base:
            runner.f2_base = None

        if runner.tagup_base == base:
            runner.tagup_base = None

        return runners


## Last line