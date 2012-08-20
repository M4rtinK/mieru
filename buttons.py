# -*- coding: utf-8 -*-
"""Mieru clutter button"""

import clutter
import gobject

import declutter

# taken from Clutter 1.6 defaults
PX_DOBLECLICK_DISTANCE = 10
MS_DOUBLECLICK_DURATION = 250
CLICK_TRESHOLD = 2048 # anything more and its a drag

def wasDoubleclick(clickCount, pxDistance, msDuration):
  """decide if an event was a click or a doubleclick"""
  # yeah, for some reason Clutter count a doubleclick as 3 clicks
  return clickCount >= 3 and pxDistance <= PX_DOBLECLICK_DISTANCE and msDuration <= MS_DOUBLECLICK_DURATION

def wasClick(dx,dy):
  """ check if a screen press event was a drag or just a click/tap"""
  distSq = dx * dx + dy * dy
  return distSq <= CLICK_TRESHOLD

class ClutterButtons:
  def __init__(self, mieru, gui):
    self.mieru = mieru
    self.gui = gui
    self.layer = clutter.Group()
    self.gui.getStage().add(self.layer)
    self.pressLength = 175 # in ms, higher than this and it will be considered to a drag
    self.fsButton = None
    self.fsButtonActive = False
    self.fsButtonLastPressTimestamp = None
    self._addButtons()
    self.gui.getStage().connect('allocation-changed', self._handleResize)

  def getLayer(self):
    """return the current container, for above/below purposes"""
    return self.layer

  def _handleResize(self, actor, actorBox, flags):
    """reposition the buttons after the window is resized
    -> on the N900 this mostly happens when switching to and from
    fullscreen"""
    (x,y,w,h) = actorBox
    self.fsButton.animate(clutter.LINEAR,200, 'x', w, 'y', h)

  def _addButtons(self):
    """initialize and add on screen buttons"""
    fsToggleButton = clutter.Texture('icons/view-fullscreen.png')
    (w,h) = fsToggleButton.get_size()
    fsToggleButton.set_size(2*w,2*h)
    fsToggleButton.set_anchor_point(2*w,2*h)
    fsToggleButton.set_reactive(True)
    fsToggleButton.set_opacity(0)

    self.layer.add(fsToggleButton)
    fsToggleButton.show()
    fsToggleButton.raise_top()

    (w1,h1) = self.gui.getStage().get_size()

    fsToggleButton.set_position(w1,h1)

    fsToggleButton.connect('button-release-event',self.do_button_release_event)
    fsToggleButton.connect('button-press-event',self.do_button_press_event)

    self.fsButton = fsToggleButton

    declutter.animate(self.fsButton,clutter.LINEAR,100,[('opacity',255)])
    gobject.timeout_add(3000,self._hideFSButton, self.fsButton)

#    self.showButton = declutter.Opacity(self.fsButton,clutter.LINEAR, 1000, 255, 0)
#    print(self.showButton)
#    self.showButton.start()

#    self.fsButton.set_opacity(0)
#    self.animation = self.fsButton.animate(clutter.LINEAR, 1000, 'x', 200)


  def do_button_press_event (self, button, event):
    self.fsButtonLastPressTimestamp = event.time

  def do_button_release_event(self, button, event):
    if self.fsButtonLastPressTimestamp:
      """we only want to react on presses that start and end on the button and last a short time,
         so that the button does not interfere with dragging the page content"""
      if (event.time - self.fsButtonLastPressTimestamp) <= self.pressLength:
        if self.fsButtonActive:
          self.gui.toggleFullscreen()
          self.fsButtonActive = False
        else:
          self.fsButtonActive = True
          declutter.animate(self.fsButton,clutter.LINEAR,100,[('opacity',255)])
          print("showing")
          timer = gobject.timeout_add(2000,self._hideFSButton, button)
      
  def _hideFSButton(self, button):
    self.fsButtonActive = False
    declutter.animate(button,clutter.LINEAR,200,[('opacity',0)])

#class Button(clutter.Texture):
#  pass