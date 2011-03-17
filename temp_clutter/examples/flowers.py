#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clutter
import math
import random
import time
from clutter import CairoTexture
import gobject
import cairo

'''
Pretty cairo flower hack.
'''

PETAL_MIN = 20
PETAL_VAR = 40
N_FLOWERS = 40 # reduce if you have a small card


class Flower(CairoTexture):
    colors = (
        (0.71, 0.81, 0.83, 0.5),
        (1.0,  0.78, 0.57, 0.5),
        (0.64, 0.30, 0.35, 0.5),
        (0.73, 0.40, 0.39, 0.5),
        (0.91, 0.56, 0.64, 0.5),
        (0.70, 0.47, 0.45, 0.5),
        (0.92, 0.75, 0.60, 0.5),
        (0.82, 0.86, 0.85, 0.5),
        (0.51, 0.56, 0.67, 0.5),
        (1.0, 0.79, 0.58, 0.5),
    )
    
    def __init__(self, x, y, translation_velocity, rotation_velocity):
        '''
        Make flower actor.
        No science here, just a hack from toying.
        '''
        self.x = x
        self.y = y
        self.rot = 0
        self.v = translation_velocity
        self.rv = rotation_velocity
        
        petal_size = PETAL_MIN + random.randint(0, PETAL_VAR)
        size = petal_size * 8
        n_groups = random.randint(1, 3) # Num groups of petals 1-3
        
        CairoTexture.__init__(self, size, size)
        cr = self.cairo_create()
        
        cr.set_tolerance(0.1)
        
        # Clear
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        
        cr.translate(size//2, size//2)
        
        last_color = None
        for group_i in range(n_groups):
            n_petals = random.randint(4, 8) # num of petals 4 - 8
            cr.save()
            
            cr.rotate(random.randint(0, 5))
            
            random_color = last_color
            while random_color == last_color:
                random_color = random.choice(self.colors)
            
            cr.set_source_rgba(*random_color)
            last_color = random_color
            
            # some bezier randomness
            pm1 = random.randint(0, 19)
            pm2 = random.randint(0, 3)
            
            for petal_i in range(n_petals + 1):
                cr.save()
                cr.rotate(((2 * math.pi) / n_petals) * petal_i)
                
                # Petals are made up beziers
                cr.new_path()
                cr.move_to(0, 0)
                cr.rel_curve_to(petal_size, petal_size,
                                (pm2+2)*petal_size, petal_size,
                                (2*petal_size) + pm1, 0)
                cr.rel_curve_to(0 + (pm2*petal_size), -petal_size,
                                -petal_size, -petal_size,
                                -((2*petal_size) + pm1), 0)
                cr.close_path()
                cr.fill()
                cr.restore()
            
            petal_size -= random.randint(0, size/8)
            cr.restore()
        
        # Finally draw flower center
        random_color = last_color
        while random_color == last_color:
            random_color = random.choice(self.colors)
        
        if petal_size < 0:
            petal_size = random.randint(0, 9)
        
        cr.set_source_rgba(*random_color)
        
        cr.arc(0, 0, petal_size, 0, math.pi * 2)
        cr.fill()
        
        del cr
    
    def tick(self, max_width, max_height):
        self.y += self.v
        self.rot += self.rv
        
        if self.y > max_height:
            self.y = -self.get_height()
            
        self.set_position(self.x, self.y)
        
        self.set_rotation(clutter.Z_AXIS, self.rot,
                          self.get_width()/2, self.get_height()/2,
                          0)

def tick(flowers, width, height):
    for flower in flowers:
        flower.tick(width, height)
    return True

if __name__ == '__main__':
    stage_color = clutter.Color(0x0, 0x0, 0x0, 0xff)
    random.seed(time.time())
    
    stage = clutter.Stage()
    stage.set_color(stage_color)
    stage.set_fullscreen(True)
    
    flowers = list()
    for flower_i in range(N_FLOWERS):
        flower = Flower(
            random.randint(0, stage.get_width()) - (PETAL_MIN+PETAL_VAR)*2,
            random.randint(0, stage.get_height()),
            random.randint(2, 11),
            random.randint(1, 5)
        )
        stage.add(flower)
        flower.set_position(flower.x, flower.y)
        flowers.append(flower)

    gobject.timeout_add(50, tick, flowers, stage.get_width(), stage.get_height())
    
    stage.show_all()
    stage.connect('key-press-event', clutter.main_quit)
    
    clutter.main()
