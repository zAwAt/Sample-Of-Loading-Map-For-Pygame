import sys
import os
import time
import numpy as np
import pygame as pg
import constants as c

class Font(pg.font.Font):
    def __init__(self,root,size = 20,text = "None" ,dest = (0,0)):
        super().__init__(c.PATH_FONT_LIST[0],size)
        self.root = root
        self.text = text
        self.dest = dest

    def update(self,text):
        if not text == None:
            self.text = text
        else:
            pass
        self.rendered_font = self.render(self.text,False,c.COLOR_WHITE)
        self.root.blit(self.rendered_font,self.dest)

class Player(pg.sprite.Sprite):
    def __init__(self,root,type,init_x,init_y):
        pg.sprite.Sprite.__init__(self,self.containers)
        self.image = pg.Surface(c.SIZE_PLAYER)
        self.rect = self.image.get_rect()

        self.type = type
        self.image.fill(c.COLOR_YELLOW)

        self.rect.x = init_x
        self.rect.y = init_y
        self.root = root
        self.root_rect = self.root.get_rect()
        self.vx = 5
        self.vy = 10
        self.jump_flag = False
        self.fall_flag = True

    def update(self,key,blocks):
        collide_list = pg.sprite.spritecollide(self,blocks,False)
        if len(collide_list) > 0:
            for block in collide_list:
                if self.rect.bottom >= block.rect.top:
                    self.rect.bottom = block.rect.top + 1
                    self.fall_flag = False
        elif len(collide_list) == 0:
            self.fall_flag = True

        if self.fall_flag == True:
            self.rect.bottom = self.rect.bottom + self.vy
        else:
            pass

        if key == "RIGHT":
            self.rect.centerx = self.rect.centerx + self.vx
        elif key == "LEFT":
            self.rect.centerx = self.rect.centerx - self.vx

        if self.fall_flag == False and self.jump_flag == False:
            if key == "SPACE":
                self.jump_flag = True
                self.fall_flag = False
                self.start_jump = time.clock()

        if self.jump_flag == True:
            jump_boost = 0
            if key == "SPACE":
                jump_boost = 10
            self.rect.bottom = self.rect.bottom - (self.vy + jump_boost)
            self.end_jump = time.clock()
            if (self.end_jump - self.start_jump) > 0.5:
                self.jump_flag = False
                self.fall_flag = True
        self.rect.clamp_ip(self.root_rect)

class Block(pg.sprite.Sprite):
    def __init__(self,root,type,init_x,init_y):
        pg.sprite.Sprite.__init__(self,self.containers)
        self.image = pg.Surface(c.SIZE_BLOCK)
        self.rect = self.image.get_rect()

        self.type = type
        if self.type == 1:
            self.image.fill(c.COLOR_GREEN)
        elif self.type == 2:
            self.image.fill(c.COLOR_RED)

        self.rect.x = init_x
        self.rect.y = init_y

        self.root = root
        self.root_rect = self.root.get_rect()

    def update(self):
        self.rect.clamp_ip(self.root_rect)

class PlayArea(pg.Surface):
    def __init__(self,root):
        super().__init__(c.SIZE_PLAYAREA)
        self.rect = self.get_rect()
        self.root = root
        self.root_rect = self.root.get_rect()

        self._set_holder()
        self._load_map(None,True)
        self.player = Player(self,100,50,50)

    def _set_holder(self):
        self.map_num = 0
        self.blocks = pg.sprite.Group()
        self.players = pg.sprite.Group()
        Block.containers = self.blocks
        Player.containers = self.players

    def _load_map_chip(self):
        self.loaded_map = c.MAPS[self.map_num]
        for i in range(self.loaded_map.shape[0]):
            for j in range(self.loaded_map.shape[1]):
                if self.loaded_map[i][j] == 1:
                    self.map_holder.append(Block(self,1,j*c.SIZE_BLOCK[0],i*c.SIZE_BLOCK[0]))
                if self.loaded_map[i][j] == 2:
                    self.map_holder.append(Block(self,2,j*c.SIZE_BLOCK[0],i*c.SIZE_BLOCK[0]))

    def _load_map(self,dir = None,init_flag = False):
        self.map_holder = []
        if dir == None:
            if init_flag == True:
                self._load_map_chip()
            else:
                pass
        elif dir == "RIGHT_MAP":
            self.blocks.empty()
            self.map_num += 1
            for block in self.map_holder:
                del block
            self._load_map_chip()
            self.player.rect.centerx = c.SIZE_BLOCK[0]

        elif dir == "LEFT_MAP":
            self.blocks.empty()
            self.map_num -= 1
            for block in self.map_holder:
                del block
            self._load_map_chip()
            self.player.rect.centerx = self.rect.width - c.SIZE_BLOCK[0]

    def _check_maps_loadable(self):
        load_dir = None
        if self.player.rect.right + (self.root_rect.width-self.rect.width)/2 >= self.rect.right - 10:
            if self.map_num + 1 < c.MAPS.shape[0]:
                load_dir = "RIGHT_MAP"
            else:
                load_dir = None
        elif self.player.rect.left + (self.root_rect.width-self.rect.width)/2 <= self.rect.left + 10:
            if self.map_num - 1 >= 0:
                load_dir = "LEFT_MAP"
            else:
                load_dir = None
        return load_dir

    def all_update(self,key):
        self.rect = self.root.blit(self,((self.root_rect.width-self.rect.width)/2,(self.root_rect.height-self.rect.height)/2))
        self.fill(c.COLOR_BLACK)
        self.blocks.update()
        self.blocks.draw(self)
        self.players.update(key,self.blocks)
        self.players.draw(self)
        load_dir = self._check_maps_loadable()
        self._load_map(load_dir)
