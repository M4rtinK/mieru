"""page.py - a manga/comix book page"""

import clutter
import gtk

class Page(clutter.Texture):
  def __init__(self, pb, mieru, name=""):
#    clutter.Texture.__init__(self,imagePath,load_data_async=True)
    clutter.Texture.__init__(self)
    if pb.props.has_alpha:
      bpp = 4
    else:
      bpp = 3
    self.set_from_rgb_data(
            pb.get_pixels(),
            pb.props.has_alpha,
            pb.props.width,
            pb.props.height,
            pb.props.rowstride,
            bpp, 0)
    self.originalSize = self.get_size()

    self.mieru = mieru
    self.name = name
    self.initialPosition = (0,0)
    self.motionCallbackId = None

    self.fitModeChanged() # implement current fit mode
    self._color = clutter.color_from_string('White')
    self.isPressed = False
    self.pressStart = None
    self.lastMotion = None
    self.movementEnabled = True # the page is fit to screen so it should not be moved

    self.connect('button-press-event', self.do_button_press_event)
    self.connect('button-release-event', self.do_button_release_event)

    self.set_keep_aspect_ratio(True) # we want to preserve the aspect ratio

  def do_button_press_event (self, actor, event):
    self.isPressed = True
    (x,y) = event.x,event.y
    self.pressStart = (x,y)
    self.lastMotion = (x,y)

    return False

  def do_button_release_event (self, actor, event):
    self.isPressed = False
    self.pressStart = None
    self.lastMotion = None
    
    return False

  def on_page_motion(self, page, event):
    (x,y) = event.x,event.y
    if page.lastMotion:
      (lasX,lastY) = page.lastMotion
      (dx,dy) = (x-lasX,y-lastY)
    else:
      (dx,dy) = (0,0)
    page.lastMotion = (x,y)
    if page.movementEnabled:
      self.movePage(page,dx,dy)

    return False

  def movePage(self,page,dx,dy):
    (x,y,w,h) = self.mieru.viewport
    (pageX,pageY,pageW,pageH) = page.get_geometry()
    (newX,newY) = (pageX+dx,pageY+dy)
    if pageW > w:
      if newX < w-pageW:
        newX = w-pageW
      elif newX > 0:
        newX = 0
    else:
      if newX < 0:
        newX = 0
      if newX > w-pageW:
        newX = w-pageW

    if pageH > h:
      if newY < h-pageH:
        newY = h-pageH
      elif newY > 0:
        newY = 0
    else:
      if newH < 0:
        newH = 0
      if newH > h-pageH:
        newH = h-pageH

    page.move_by(newX - pageX,newY - pageY)

  def activate(self):
    self.fitModeChanged() # implement current fit mode
    self.set_reactive(True) # this enables receiving of motion events
    self.motionCallbackId = self.connect('motion-event', self.on_page_motion)

  def deactivate(self):
    if self.motionCallbackId != None:
      self.disconnect(self.motionCallbackId)
      self.motionCallbackId = None


  def fitModeChanged(self):
    # update the variable
    mode = self.mieru.fitMode
    # implement the fit mode
    if mode == "original":
      self.setOriginalSize()
    elif mode == "width":
      self.fitToWidth()
    elif mode == "height":
      self.fitToHeight()
    elif mode == "screen":
      self.fitToScreen()


  def setOriginalSize(self):
    """resize back to original size"""
    self.set_size(*self.originalSize)

  def fitToWidth(self):
    (x,y,width,h) = self.mieru.viewport
    self.resetPosition()
    (w,h) = self.get_size()
    factor = float(width) / w
    (newW,newH) = (w*factor,h*factor)
    self.set_size(newW,newH)
    return(newW,newH)

  def fitToHeight(self):
    (x,y,w,height) = self.mieru.viewport
    self.resetPosition()
    (w,h) = self.get_size()
    factor = float(height) / h
    (newW,newH) = (w*factor,h*factor)
    self.set_size(newW,newH)
    return(newW,newH)

  def fitToScreen(self):
    (x,y,screenW,screenH) = self.mieru.viewport
    (w,h) = self.get_size()
    # resize to fit to screen
    if w > h:
      (newW,newH) = self.fitToWidth(screenW)
    else:
      (newW,newH) = self.fitToHeight(screenH)
    # move to the center
    shiftX = (screenW-newW)/2.0
    shiftY = (screenH-newH)/2.0
    self.movementEnabled = False
    print "asasas"
    print self.movementEnabled
    self.set_position(shiftX,shiftY)

  def resetPosition(self):
    self.set_position(*self.initialPosition)
    self.movementEnabled = True

  def getPath(self):
    return self.imagePath

#  def fitToWidth(self):
#    (x,y,w,h) = self.mieru.viewport
#    self.set_width(w)


#
#
##
#
#    self.connect('leave-event', self.do_leave_event)
#    self.connect('enter-event', self.do_enter_event)
#
#  def do_enter_event(self,actor,event):
#    print "enter"
#
#  def do_leave_event (self, actor, event):
#    if self._is_pressed == True:
#      self._is_pressed = False
#      clutter.ungrab_pointer()
#      return True
#    else:
#      return False
##
#  def do_clicked (self):
#    print "clicked"

#  def loadImage(self,path):
#    try:
#      self.set_from_file(path)
#    except Exception, e:
#      print "loading page from file failed"
#      print e





