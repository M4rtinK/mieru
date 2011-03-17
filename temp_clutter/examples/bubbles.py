#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clutter
from clutter import CairoTexture
import math
import time
import random

import cairo


N_BUBBLES = 50
BUBBLE_R = 128
SCREEN_W = 640
SCREEN_H = 480

def create_bubble():
    bubble = CairoTexture(BUBBLE_R*2, BUBBLE_R*2)
    cr = bubble.cairo_create()
    
    cr.set_operator(cairo.OPERATOR_CLEAR)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVER)
    
    cr.arc(BUBBLE_R, BUBBLE_R, BUBBLE_R, 0.0, 2*math.pi)
    
    pattern = cairo.RadialGradient(BUBBLE_R, BUBBLE_R, 0,
                            BUBBLE_R, BUBBLE_R, BUBBLE_R)
    pattern.add_color_stop_rgba(0, 0.88, 0.95, 0.99, 0.1)
    pattern.add_color_stop_rgba(0.6, 0.88, 0.95, 0.99, 0.1)
    pattern.add_color_stop_rgba(0.8, 0.67, 0.83, 0.91, 0.2)
    pattern.add_color_stop_rgba(0.9, 0.5, 0.67, 0.88, 0.7)
    pattern.add_color_stop_rgba(1.0, 0.3, 0.43, 0.69, 0.8)
    
    cr.set_source(pattern)
    cr.fill_preserve()
    
    del pattern
    
    pattern = cairo.LinearGradient(0, 0, BUBBLE_R*2, BUBBLE_R*2)
    pattern.add_color_stop_rgba(0.0, 1.0, 1.0, 1.0, 0.0)
    pattern.add_color_stop_rgba(0.15, 1.0, 1.0, 1.0, 0.95)
    pattern.add_color_stop_rgba(0.3, 1.0, 1.0, 1.0, 0.0)
    pattern.add_color_stop_rgba(0.7, 1.0, 1.0, 1.0, 0.95)
    pattern.add_color_stop_rgba(1.0, 1.0, 1.0, 1.0, 0.0)
    
    cr.set_source(pattern)
    cr.fill()
    
    del pattern
    del cr
    
    return bubble

class BubbleClone(clutter.Clone):
    
    linear = 0
    angular = 0
    
    def __init__(self, texture, x, y):
        clutter.Clone.__init__(self, texture)
        self.x, self.y = x, y
        self.set_position(self.x, self.y)
        self.linear = 0
        self.angular = 0
    
    def notify_y(self, pspec, stage):
        if self.get_y() > -self.get_height():
            return
        
        size = random.randint(BUBBLE_R//4, BUBBLE_R*2)
        self.set_size(size, size)
        self.set_rotation(clutter.Z_AXIS,
                          random.uniform(0.0, 360.0),
                          size//2, size//2, 0)
        self.x = random.randint(0, SCREEN_W-BUBBLE_R)
        self.y = random.randint(SCREEN_H*2, SCREEN_H*3)
        self.set_position(self.x, self.y)
        self.set_opacity(random.randint(80, 255))
        
        self.linear = random.uniform(0.5, 3.0)
        self.angular = random.uniform(-0.5, 0.5)
    
    def new_frame(self, timeline, frame_num):
        delta = timeline.get_delta()
        linear = self.linear
        angular = self.angular

        angular = angular * delta
        
        self.y = self.y - linear * delta
        self.x = self.x + angular
        self.set_position(int(round(self.x)), int(round(self.y)))
        
        angular += self.get_rotation(clutter.Z_AXIS)[0]
        while (angular > 360):
            angular -= 360.0
        while (angular < 0):
            angular += 360.0
        
        radius = self.get_width() / 2
        self.set_rotation(clutter.Z_AXIS, angular, radius, radius, 0)


if __name__ == '__main__':
    bg_color = clutter.Color(0xe0, 0xf2, 0xfc, 0xff)
    
    random.seed(time.time())
    
    stage = clutter.Stage()
    stage.set_size(SCREEN_W, SCREEN_H)
    stage.set_color(bg_color)
    stage.connect('destroy', clutter.main_quit)
    
    timeline = clutter.Timeline(1000)
    timeline.set_loop(True)
    
    bubble = create_bubble()
    stage.add(bubble)
    bubble.set_opacity(0x0)
    for bubble_i in range(N_BUBBLES):
        clone = BubbleClone(bubble, bubble_i * BUBBLE_R*2, -BUBBLE_R*2)
        
        stage.add(clone)
        
        clone.connect('notify::y', BubbleClone.notify_y, stage)
        timeline.connect('new-frame', clone.new_frame)
        
        clone.notify_y(None, stage)
    
    stage.show_all()
    
    timeline.start()
    
    clutter.main()
