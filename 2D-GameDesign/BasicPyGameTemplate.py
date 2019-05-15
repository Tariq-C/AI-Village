#Credit @KidsCanCode https://www.youtube.com/watch?v=Eltz-XJMxuU&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=2
# Tutorial Followed to create pygame template

# This is the starting code for a new game
import pygame as pg
import random as rdm


# Cosntants for the game screen

WIDTH = 720
HEIGHT = 720
FPS = 60

# Colour Definitions

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pg.init()   # initializes Pygame
screen = pg.display.set_mode((WIDTH, HEIGHT)) #Game Window

pg.display.set_caption("This Is A Test Game")   #Sets the title on Game Window
clock = pg.time.Clock() #Game Clock

all_agents = pg.sprite.Group()
# Game Loop
running = True

while running:
    #keep game running at our defined FPS
    clock.tick(FPS)
    #Process input(events)
    for event in pg.event.get(): #All events are stored in pg.event
        if event.type == pg.QUIT: #pg.QUIT == red x on top right of screen
            print("game over")
            running = False
    #Update
    all_agents.update()
    #Display
    screen.fill(BLACK)
    all_agents.draw(screen)
    pg.display.flip() #Make sure to do this after Double buffer