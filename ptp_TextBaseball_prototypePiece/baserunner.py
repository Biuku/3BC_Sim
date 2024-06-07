""" MAY 20 -- Baseball rules engine

Separating out the baserunner class -- it was getting cumbersome

"""


import pygame
from pygame.locals import *
import math


pygame.init()


class Baserunner:
    
    def __init__(self, name, base = 0):
        
        self.name = name
        
        self.occupied_base = base
        self.attained_base = base
        
        self.f2_base = None
        self.tagup_base = None

