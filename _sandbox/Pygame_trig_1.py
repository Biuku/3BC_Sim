
import pygame
from pygame.locals import *
pygame.init()
import math
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(1, 30) # Opens Pygame to top-left of monitor

#### Setup #### 
## Basic setup ##
for false_loop in range(1):
    w, h = 2000, 1350
    right_divider_x = w-200
    screen = pygame.display.set_mode((w, h))

    clock = pygame.time.Clock()
    fps = 15
    theta_deg = 45
    
    med_font = pygame.font.SysFont('Arial', 14)
    small_font = pygame.font.SysFont('Arial', 10)
    

## Trig setup ##
F = origin = ( right_divider_x//2, h//2 + 1)  # Fixed position
Q = (F[0] + 300, F[1] + 300) # Moveable pos

ball_x = origin[0]
ball_y = origin[1]
ball_move_toggle= False

#### Helper function(s) ####
def draw_text(screen, string_, coord, font):
    
    text = font.render(string_, True, 'black')
    text_rect = text.get_rect( )
    
    text_rect.topleft = coord
            
    screen.blit(text, text_rect)

def draw_coord_lines():
    pygame.draw.line(screen, 'black', (0, 0), (w, 0), 3) # Top of the screen
    pygame.draw.line(screen, 'black', (right_divider_x, 0), (right_divider_x, h), 3) # Right divider
    
    #Draw Circle around origin
    radius = h/2 - 2
    pygame.draw.circle(screen, 'grey', origin, radius, 1)        
    
    ## Draw axes through origin

    h_y = origin[1]
    v_x = origin[0]
    hz_line =  [ (v_x - radius + 2, h_y), (v_x + radius - 2, h_y) ] # (right_divider_x-2, h_y) ]
    vt_line = [ (v_x, h_y - radius + 2), (v_x, h_y + radius - 2) ]
    
    for coord in [ hz_line, vt_line ]:
        pygame.draw.line(screen, 'grey', coord[0], coord[1], 1) 
        
   
### Trig -- basic stuff ###
def get_right_corner(F, Q):
    return (Q[0], F[1])# Get the right angle corner of the triangle

def get_delta_xy(F, Q):
    dx = Q[0] - F[0]
    dy = Q[1] - F[1]
    dy = -1 * dy # Reverse to fit Pygame y coord system
    
    return dx, dy


### Trig -- harder stuff ###

## Draw a line -- angle determined by up/down arrows 
def draw_line_from_deg(theta_deg, length):
    length = h/2 - 2
    theta_rad = math.radians(theta_deg)
    end_x = origin[0] + length * math.cos(theta_rad)
    end_y = origin[1] - length * math.sin(theta_rad) # Negative because Pygame Y axis
    
    pygame.draw.line(screen, 'blue', origin, (end_x, end_y), 4)

def move_ball(ball_x, ball_y, theta_deg):
    speed = 4
    theta_rad = math.radians(theta_deg)
    
    ball_x += speed * math.cos(theta_rad)
    ball_y -= speed * math.sin(theta_rad)
      
    return ball_x, ball_y
  
def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, 'red', (ball_x, ball_y), 12 )
    

def get_theta_rad(adj, opp):
    return math.atan2(opp, adj)
    

""" *** META GOALS *** """
"""
1. DONE! -- Get and print the length of opp and adj
2. DONE! -- Ensure I have a unique degree value that spans LF to RF out of bounds lines
3. DONE! -- Build an ability to enter degree and send Q to the circle edge in that direction
4. DONE! -- Using 3, build ability to move a simple object (small circle) in a direction
"""

exit = False

while not exit:
    clock.tick(fps)
    screen.fill('white')
    draw_coord_lines()

    ### Get events ###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
            
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit = True
                
            if event.key == K_UP:
                theta_deg += 5
                
            if event.key == K_DOWN:
                theta_deg -= 5
                
            if event.key == K_SPACE:
                ball_move_toggle= not(ball_move_toggle)

    # Make Q move with the mouse
    Q = pygame.mouse.get_pos()

    """ TRIG STUFF """

    ### Trig - Basic stuff ###
    RC = get_right_corner(F, Q)
    dx, dy = get_delta_xy(F, Q) #Get Delta x and Delta y
    adj = dx 
    opp = dy  
    
    ### Trig -- medium stuff ###
    hyp = math.sqrt(adj**2 + opp**2)
    
    #theta_rad = math.acos(adj/hyp)
    theta_rad = get_theta_rad(adj, opp) 
    theta_deg = round(math.degrees(theta_rad), 1)
    
    ### Draw the triange
    pygame.draw.polygon(screen, 'grey', (F, Q, RC) )
    
    ### Trig -- harder stuff
    draw_line_from_deg(theta_deg, dx) # dx = length of the line
    
    if ball_move_toggle:
        ball_x, ball_y = move_ball(ball_x, ball_y, theta_deg)
    
    draw_ball(ball_x, ball_y)
 
    """ Draw stuff to screen """
    
    for false_loop in range(1): ## This lets me hide this in Visual Studio
        
        ## Annotate "Theta"
        draw_text(screen, "Theta", ( F[0]+5, F[1] + 5 ), small_font )

        #### TEXT -- Print key data on right side ####
        coord_text = "COORDINATES:"
        F_text = "F: " + str(F)
        Q_text  = "Q: " + str(Q)
        RC_text = "RC: " + str(RC)
        
        length_text = "LENGTHS:"
        
        hyp_text = "HYP: " + str( int(hyp) )
        adj_text = "ADJ / dx: " + str( int(adj) )
        opp_text = "OPP / dy: " + str( int(opp) )
        
        angle_text = "ANGLES"
        
        #theta_deg = round(math.degrees(theta_rad), 1)
        theta_text = "Theta: " + str(theta_deg) + "\u00b0"

    
        texts = [coord_text, F_text, Q_text, RC_text, " ", length_text, hyp_text, adj_text, opp_text, " ", angle_text, theta_text ]
        
        start_y = 100
        for y, text in enumerate(texts):         
            draw_text(screen, text, (right_divider_x+30, start_y + (y*20) ), med_font)
        
        
    pygame.display.update()