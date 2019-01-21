import sys
import os
import time
import pygame as pg
import constants as c
from game_objects import *

class Game:
    def __init__(self):
        pg.init()
        self.root = pg.display.set_mode(c.SIZE_DISPLAY)
        pg.display.set_caption("Sample Of Loading Map For Pygame")
        self.running = True

        self.clock = pg.time.Clock()
        self.fps = 30
        self._set_params()
        self._rungame()

    def _set_params(self):
        self.game_state = True
        self.playarea = PlayArea(self.root)
        self.title = Font(self.root,36,"Sample Of Loading Map For Pygame",(5,100))
        self.show_fps = Font(self.root,30)

    def _rungame(self):
        while self.running:
            self.fps_counter_A = time.clock()
            self.clock.tick(self.fps)#base
            self.key = self._keyhandler()#base
            self._eventhandler()#base
            self._set_state()
            self._draw() #UPDATE PLAYAREA
            self.fps_counter_B = time.clock()
            self.show_fps.update("fps:" + str(round(1/(self.fps_counter_B - self.fps_counter_A),2)))
            pg.display.update()#base

    def _set_state(self):
        if self.key == "RETURN" and self.game_state == False:
            self.game_state = True
        elif self.key == "RETURN" and self.game_state == True:
            self.game_state = False

    def _draw(self):
        if self.game_state == True:
            self.root.fill(c.COLOR_GREEN)
            self.title.update(None)
        elif self.game_state == False:
            self.root.fill(c.COLOR_BLUE)
            self.playarea.all_update(self.key)

    def _keyhandler(self):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_LEFT]:pressed_key = "LEFT"
        elif pressed[pg.K_RIGHT]:pressed_key = "RIGHT"
        elif pressed[pg.K_UP]:pressed_key = "UP"
        elif pressed[pg.K_DOWN]:pressed_key = "DOWN"
        elif pressed[pg.K_RETURN]:pressed_key = "RETURN"
        elif pressed[pg.K_SPACE]:pressed_key = "SPACE"
        else:pressed_key = None
        return pressed_key

    def _eventhandler(self): #exit handleer
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
                pg.quit()
                sys.exit()
        pg.event.clear()

Game()
