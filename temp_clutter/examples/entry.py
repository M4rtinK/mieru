#!/usr/bin/env python
# -*- coding: utf-8 -*-

# clutter.Entry usage example
# Copyright (C) 2008  Florent Thiery <florent.thiery@ubicast.eu>
# Released under the terms of the LGPL
#
# This example demonstrates basic Entry handling with pyclutter
# Usage: click on the Entry box to activate the Entry widget, type to
#        write text and hit <return> for Entry buffer console print

import clutter

class EntryWidget (clutter.Text):
    def __init__(self, stage):
        clutter.Text.__init__(self)
        self.set_color(clutter.color_from_string('Black'))
        self.set_text("Test entry (modify me)")
        self.set_position(10,10)
        self.set_reactive(True)
        self.set_editable(True)
        self.connect("button-press-event", self.on_press_cb)
        self.connect("key-press-event", self.key_cb)
        self.connect("activate", self.activated_cb)
        self.stage = stage

    def key_cb(self, stage, event):
        print "key_cb called: %s" % (str(event))
        return False

    def activated_cb(self, stage):
        print "Entered text was: "+self.get_text()
        # unset the key focus by giving it back to the stage
        self.stage.set_key_focus(None)

    def on_press_cb(self, stage, event):
        # acquire key focus
        self.stage.set_key_focus(self)
        return False

if __name__ == '__main__':
    stage = clutter.Stage()
    stage.set_color(clutter.Color(0xcc, 0xcc, 0xcc, 0xff))
    stage.set_size(320,240)
    stage.connect('destroy', clutter.main_quit)

    entry_test = EntryWidget(stage)

    stage.add(entry_test)
    stage.show_all()
    clutter.main()
