""" March 22, 2024 """


import pygame

class Ball:
    
    def __init__(self, win):
        pygame.init()
        self.win = win
        self.ball = pygame.image.load("baseball.jpg")
        
    def draw_ball(self, coord):
        ball = pygame.image.load("objects/baseball.jpg")
        
        ## Shrink ball
        ball_size = ball.get_size()
        factor = 0.15
        smaller_ball = ( int(ball_size[0]*factor), int(ball_size[1]*factor) ) 
        ball2 = pygame.transform.scale(ball, smaller_ball)
        
        self.win.blit(ball2, coord)
