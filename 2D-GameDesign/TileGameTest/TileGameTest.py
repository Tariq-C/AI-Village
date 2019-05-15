#Credit @KidsCanCode https://www.youtube.com/watch?v=Eltz-XJMxuU&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=2
# Tutorial Followed to create pygame template

# This is the starting code for a new game
import pygame as pg
import random as rdm
import sys
from GameSettings import *
from Agent import *
from Food import *

class Game:
    def __init__(self):
        # Initialize game window
        self.running = True

        pg.init()  # initializes Pygame
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # Game Window

        pg.display.set_caption("This Is A Test Game")  # Sets the title on Game Window
        self.clock = pg.time.Clock()  # Game Clock

    def run(self):
        # Game Loop
        self.inGame = True
        while self.inGame:
            # Keep game running at our defined FPS
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop Update
        self.resources.update()
        self.all_agents.update()

    def events(self):
        # Process input(events)
        for event in pg.event.get():  # All events are stored in pg.event
            if event.type == pg.QUIT:  # pg.QUIT == red x on top right of screen
                if self.inGame:
                    self.inGame = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.agent1.move(dy=-1)
                if event.key == pg.K_a:
                    self.agent1.move(dx=-1)
                if event.key == pg.K_s:
                    self.agent1.move(dy=1)
                if event.key == pg.K_d:
                    self.agent1.move(dx=1)

    def draw(self):
        # Game Loop Events

        self.screen.fill(BLACK)
        self.draw_grid()
        self.resources.draw(self.screen)
        self.all_agents.draw(self.screen)
        pg.display.flip()  # Make sure to do this after Double buffer

    def draw_grid(self):
        for x in range(GUIY, WIDTH-GUIX+1, TILESIZE):
            pg.draw.line(self.screen, WHITE, (x, GUIY), (x,HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, WHITE, (0, y), (WIDTH-GUIX, y))

    def new(self):
        #Starts Game
        self.resources = pg.sprite.Group()
        self.all_agents = pg.sprite.Group()
        self.food1 =  Food(self, 3, 3)
        self.agent1 = Agent(self, 1, 1)
        self.resources.add(self.food1)
        self.all_agents.add(self.agent1)
        self.run()


g = Game()

while g.running:
    g.new()

pg.quit()