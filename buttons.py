"""Mieru clutter button"""

import clutter
import gobject

import declutter

class Buttons:
  def __init__(self, mieru):
    self.mieru = mieru
    self.layer = clutter.Group()
    self.mieru.stage.add(self.layer)
    self.fsButton = None
    self.fsButtonActive = False
    self.fsButtonActive = False
    self._addButtons()

  def getLayer(self):
    """return the current container, for abowe/below purposes"""
    return self.layer


  def _addButtons(self):
    """initialize and add ons creen buttons"""
    fsToggleButton = clutter.Texture('icons/view-fullscreen.png')
    (w,h) = fsToggleButton.get_size()
    fsToggleButton.set_size(2*w,2*h)
    fsToggleButton.set_anchor_point(2*w,2*h)
    fsToggleButton.set_reactive(True)
    fsToggleButton.set_opacity(0)

    self.layer.add(fsToggleButton)
    fsToggleButton.show()
    fsToggleButton.raise_top()

    (x,y,w1,h1) = self.mieru.viewport

    fsToggleButton.set_position(w1,h1)

    fsToggleButton.connect('button-release-event',self.do_button_press_event)

    self.fsButton = fsToggleButton

    declutter.animate(self.fsButton,clutter.LINEAR,300,[('opacity',255)])
    gobject.timeout_add(3000,self._hideFSButton, self.fsButton)

#    self.showButton = declutter.Opacity(self.fsButton,clutter.LINEAR, 1000, 255, 0)
#    print self.showButton
#    self.showButton.start()

#    self.fsButton.set_opacity(0)
#    self.animation = self.fsButton.animate(clutter.LINEAR, 1000, 'x', 200)


  def do_button_press_event (self, button, event):
    print "pressed"
    if self.fsButtonActive:
      print "starting hiding"
      self.mieru.toggleFullscreen()
      self.fsButtonR = self.fsButton.animate(clutter.LINEAR, 1000, 'rotation-angle-z', 360)
      self.fsButtonActive = False
    else:
      self.fsButtonActive = True
      declutter.animate(self.fsButton,clutter.LINEAR,300,[('opacity',255)])
      print "showing"
      timer = gobject.timeout_add(2000,self._hideFSButton, button)

  def _hideFSButton(self, button):
    print "hiding"
    self.fsButtonActive = False
    declutter.animate(button,clutter.LINEAR,300,[('opacity',0)])

#class Button(clutter.Texture):
#  pass