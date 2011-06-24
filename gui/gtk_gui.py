# To change this template, choose Tools | Templates
# and open the template in the editor.

import pygtk
pygtk.require('2.0')
import gtk
import gui

class GTKGUI(gui.GUI):
  def __init__(self, mieru, type, size=(800,480)):
    gui.GUI.__init__(self, mieru)
    if type == "hildon":
      import hildon
      self.window = hildon.StackableWindow()
    else:
      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.resize(*size)

    self.window.connect("destroy", self._destroyCB)

    self.vbox = gtk.VBox(False, 2)
    self.window.add(self.vbox)
    self.fullscreen = False

  def getVbox(self):
    return self.vbox

  def resize(self, w, h):
    self.window.resize(w,h)

  def getWindow(self):
    return self.window

  def setWindowTitle(self, title):
    self.window.set_title(title)

  def getToolkit(self):
    return "GTK"

  def toggleFullscreen(self):
    if self.fullscreen:
      self.window.unfullscreen()
      self.fullscreen = False
    else:
      self.window.fullscreen()
      self.fullscreen = True

  def startMainLoop(self):
    """start the main loop or its equivalent"""
    gtk.main()

  def stopMainLoop(self):
    """stop the main loop or its equivalent"""
    gtk.main_quit()

  def _destroyCB(self, window):
    self.mieru.destroy()