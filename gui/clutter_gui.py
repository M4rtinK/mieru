""" a clutter based stage for mangas and buttons """

"""
NOTE: PyClutter 1.0 import order:
import cluttergtk
import clutter
import gtk
"""

import cluttergtk
import pygtk
pygtk.require('2.0')
import gtk

import gtk_gui
import buttons

class ClutterGTKGUI(gtk_gui.GTKGUI):
  def __init__(self, mieru, type, size):
    gtk_gui.GTKGUI.__init__(self, mieru, type, size)

    # get the Clutter embed and add it to the window
    self.embed = cluttergtk.Embed()
    self.vbox.pack_start(self.embed)
    self.vbox.show_all()
    
    # we need to realize the widget before we get the stage
    self.embed.realize()
    self.embed.show()
    self.embed.connect('key-press-event', self._onKeyPressEvent)
    
    # get the stage
    self.stage = self.embed.get_stage()
    self.stage.realize()
    self.stage.set_color("White")

    # activate clutter based buttons
    self.buttons = buttons.ClutterButtons(self.mieru, self)

    # This packs the button into the window (a GTK container).
    self.embed.show()

    # and show the window
    self.window.show()

  def _onKeyPressEvent(self, widget, event):
    keyName = gtk.gdk.keyval_name(event.keyval)
    self._keyPressed(keyName)

  def getStage(self):
    return self.stage

  def getAccel(self):
    return True

  def getViewport(self):
    (w,h) = self.stage.get_size()
    return (0,0,w,h)





