#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clutter
import math
from clutter import CairoTexture
from datetime import datetime
import gobject
import cairo

def drawClock(cr):
    # clock drawing code from http://www.cairographics.org/SDLCLock
    
    # store the current time
    now = datetime.now()
    # compute the angles for the indicators of our clock
    #print now
    hours = now.hour * math.pi / 6
    minutes = now.minute * math.pi / 30
    seconds = now.second * math.pi / 30
    
    # Clear our surface
    cr.set_operator (cairo.OPERATOR_CLEAR)
    cr.paint()
    
    cr.set_operator(cairo.OPERATOR_OVER)
    
    # who doesn't want all those nice line settings :)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_width(0.1)
    
    # translate to the center of the rendering context and draw a black
    # clock outline
    cr.set_source_rgba(0, 0, 0, 1)
    cr.translate(0.5, 0.5)
    cr.arc(0, 0, 0.4, 0, math.pi * 2)
    cr.stroke()
    
    # draw a white dot on the current second.
    cr.set_source_rgba(1, 1, 1, 0.6)
    cr.arc(math.sin(seconds) * 0.4, -math.cos(seconds) * 0.4,  0.05, 0, math.pi * 2)
    cr.fill()
    
    # draw the minutes indicator
    cr.set_source_rgba(0.2, 0.2, 1, 0.6)
    cr.move_to(0, 0)
    cr.line_to(math.sin(minutes) * 0.4, -math.cos(minutes) * 0.4)
    cr.stroke()
    
    # draw the hours indicator
    cr.move_to(0, 0)
    cr.line_to(math.sin(hours) * 0.2, -math.cos(hours) * 0.2)
    cr.stroke()

def tick(texture):
    cr = texture.cairo_create()
    cr.scale(300, 300)#texture.get_width(), texture.get_height())
    drawClock(cr)
    return True

if __name__ == '__main__':
    stage_color = clutter.Color(0x99, 0xcc, 0xff, 0xff)
    
    stage = clutter.Stage()
    stage.connect('button-press-event', clutter.main_quit)
    stage.connect('destroy', clutter.main_quit)
    stage.set_color(stage_color)
    
    texture = CairoTexture(300, 300)
    texture.set_position(
        (stage.get_width() - 300) / 2,
        (stage.get_height() - 300) / 2
    )
    stage.add(texture)
    texture.show()
    
    tick(texture)
    gobject.timeout_add_seconds(1, tick, texture)
    stage.show()
    
    clutter.main()
