#!/usr/bin/env python
### BEGIN LICENSE
# Copyright (C) 2009 Manuel de la Pena <mandel@themacaque.com>
#This program is free software: you can redistribute it and/or modify it
#under the terms of the GNU General Public License version 3, as published
#by the Free Software Foundation.
#
#This program is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranties of
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#PURPOSE.  See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along
#with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

#source: http://www.themacaque.com/?p=587

import gobject
import clutter
 
class FloatLayout(clutter.Actor, clutter.Container):
    """
    Container that aligns its children in a canvas in a way that the bigest
    number of widgets is shown per row given the allocation provided by the
    stage.
    """
 
    def __init__(self, padding=5):
        """
        Creates a new layout that can
        """
        clutter.Actor.__init__(self)
        self._children = []
        self._padding = padding
        # we need to listen to the parent being set in order to be able to
        # re do the layout when the parent resizes, that is the parent paints
        # and we re allocate the widget
        self.connect("parent-set", self.on_set_parent)
 
    def on_set_parent(self, widget, old_parent):
        parent = self.get_parent()
        if parent:
            parent.connect('notify::allocation', self.on_parent_allocate)
 
    def on_parent_allocate(self, *args):
        # we ignore the params, we simple re layout
        self.queue_relayout()
 
    def do_add(self, *children):
        """
        Allows to add new childrent to the layout.
        """
        for child in children:
            if child in self._children:
                raise Exception("Actor {0} is already a children of {1}".format(
                    child, self))
            self._children.append(child)
            child.set_parent(self)
            self.queue_relayout()
 
    def do_remove(self, *children):
        for child in children:
            if child in self._children:
                self._children.remove(child)
                child.unparent()
                self.queue_relayout()
            else:
                raise Exception("Actor {0} is not a child of {1}".format(
                    child, self))
 
    def do_get_preferred_width(self, for_height):
        """
        The preferred width to be used in this layout is to have all
        the actors in a single line trying to use the bigest amount of space
        given horizontaly.
        """
        min_width = 0
        natural_width = self.get_parent().get_size()[0]
        for child in self._children:
            child_min_width, child_natural_width = child.get_preferred_width(
                for_height)
            min_width = max(min_width, child_min_width)
        return (min_width + self._padding, natural_width)
 
    def do_get_preferred_height(self, for_width):
        """
        The preferred height of this layout is the bigest height of the
        collection og childre trying to draw all the actors in the same line.
        """
        min_height = 0
        natural_height = 0
        for child in self._children:
            child_min_height, child_natural_width = child.get_preferred_height(
                    for_width)
            min_height = max(min_height, child_min_height)
            natural_height = max(natural_height, child_natural_width)
        return (min_height + self._padding, natural_height + self._padding)
 
    def do_allocate(self, box, flags):
        # we get the width of the box, when drawing we draw horizontaly until
        # we run out of space, then we draw vertically
        box_width = box.x2 - box.x1
        child_x = child_y = self._padding
        for child in self._children:
            w, h = child.get_preferred_size()[2:]
            child_box = clutter.ActorBox()
            child_box.x1 = child_x
            child_box.y1 = child_y
            child_box.x2 = child_box.x1 + w
            child_box.y2 = child_box.y1 + h
            child.allocate(child_box, flags)
            # TODO: If this is ought to be used in general the diff sizes should
            # be taken into account
            if child_box.x2 + (1.5 * w) > box_width:
                child_x = self._padding
                child_y += h + 2 * self._padding
            else:
                child_x += w + 2 * self._padding
        clutter.Actor.do_allocate(self, box, flags)
 
    def do_foreach(self, func, data=None):
        for child in self._children:
            func(child, data)
 
    def do_paint(self):
        for actor in self._children:
            actor.paint()
 
    def do_pick(self, color):
        clutter.Actor.do_pick(self, color)
        for actor in self._children:
            actor.paint()
 
gobject.type_register(FloatLayout)
 
if __name__ == '__main__':
    def on_button_press(box, event):
        box.props.orientation = not box.props.orientation
        return True
 
    def on_child_button_pressed(actor, event):
        print 'Rectangle with color %s pressed' % actor.get_color()
 
    def on_key_press(stage, event, box):
        from clutter import keysyms
        if event.keyval == keysyms.h:
            for child in box:
                do_allocate = box.child_get_property(child,
                        'allocate-hidden')
                box.child_set_property(child, 'allocate-hidden',
                        not do_allocate)
            box.queue_relayout()
 
    import random
    stage = clutter.Stage()
    stage.connect('destroy', clutter.main_quit)
 
    box = FloatLayout()
    for i in range(10):
        rect = clutter.Rectangle()
        color = clutter.Color(random.randint(0, 255), random.randint(0, 255),
                random.randint(0, 255), 255)
        rect.set_color(color)
        rect.set_size(50, 50)
        box.add(rect)
 
    stage.add(box)
    box.set_reactive(True)
 
 
    box.connect('button-press-event', on_button_press)
    stage.connect('key-press-event', on_key_press, box)
 
    stage.set_user_resizable(True)
    stage.show()
    clutter.main()

