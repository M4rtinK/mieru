"""page.py - a manga/comix book page"""

import clutter
import gtk

class Page(clutter.Texture):
  def __init__(self, pb, mieru, name="", fitOnStart=True):
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
    del pb
    self.originalSize = self.get_size()

    self.mieru = mieru
    self.name = name
    self.initialPosition = (0,0)
    self.motionCallbackId = None

    if fitOnStart:
      self.setFitMode(self.mieru.get('fitMode', 'original')) # implement current fit mode
    self._color = clutter.color_from_string('White')
    self.isPressed = False
    self.pressStart = None
    self.lastMotion = None
    self.movementEnabled = True # the page is fit to screen so it should not be moved
    self.zoomIn=True
    self.fsButtonLastPressTimestamp = None
    self.pressLength = 100

    self.connect('button-press-event', self.do_button_press_event)
    self.connect('button-release-event', self.do_button_release_event)
    self.mieru.stage.connect('allocation-changed', self._handleResize)

    self.set_keep_aspect_ratio(True) # we want to preserve the aspect ratio

  def do_button_press_event (self, actor, event):
#    clickCount = event.get_click_count()
#    print "press", clickCount
#    if clickCount >= 3:
#      self._toggleZoom()
    self.fsButtonLastPressTimestamp = event.time

      
    self.isPressed = True
    (x,y) = event.x,event.y
    self.pressStart = (x,y)
    self.lastMotion = (x,y)

    return False

  def do_button_release_event (self, actor, event):
    clickCount = event.get_click_count()
    if clickCount >= 3 and self.fsButtonLastPressTimestamp:
      if (event.time - self.fsButtonLastPressTimestamp)<self.pressLength:
        print (event.time - self.fsButtonLastPressTimestamp)
        (x1,y1) = self.pressStart
        (x,y) = (x1-event.x,y1-event.y)
        print (x,y)


        self._toggleZoom()

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
    """move the page so that the voewport either stays inside it
       or the page stays inside the viewport if it is smaller"""
    if self.isPressed:
      (x,y,w,h) = self.mieru.viewport
      (pageX,pageY,pageW,pageH) = page.get_geometry()
      (newX,newY) = (pageX+dx,pageY+dy)

      if pageW > w: # page is wider than screen
        if newX < w-pageW:
          newX = w-pageW
        elif newX > 0:
          newX = 0
      else: # screen is wider than page
        if newX < 0:
          newX = 0
        if newX > w-pageW:
          newX = w-pageW

      if pageH > h: # page is longer than screen
        if newY < h-pageH:
          newY = h-pageH
        elif newY > 0:
          newY = 0
      else: # screen is longer than page
        if newY < 0:
          newY = 0
        if newY > pageH-h:
          newY = pageH-h
      page.move_by(newX - pageX,newY - pageY)


  def activate(self):
    self.setFitMode(self.mieru.get('fitMode', 'original')) # implement current fit mode
    self.set_reactive(True) # this enables receiving of motion events
    self.motionCallbackId = self.connect('motion-event', self.on_page_motion)

  def deactivate(self):
    self.set_reactive(False)
    if self.motionCallbackId != None:
      self.disconnect(self.motionCallbackId)
      self.motionCallbackId = None


  def setFitMode(self, mode, resetPosition=True):
    # recentre first (if enabled)
#    self.resetPosition()

    # implement the fit mode
    if mode == "original":
      self.setOriginalSize()
    elif mode == "width":
      self.fitToWidth()
    elif mode == "height":
      self.fitToHeight()
    elif mode == "screen":
      self.fitToScreen()

  def _fitAfterResetCB(self, timeline, mode):
    # NOTE: always set resetPosition=False, it will couase an infinite lopp otherwise
    self.setFitMode(mode, resetPosition=False)

  def _enableMovementCB(self, timeline):
    """enable movement after an animation finishes"""
    self.movementEnabled = True

  def setOriginalSize(self):
    """resize back to original size"""
    (w, h) = self.originalSize
    (x,y,width,height) = self.mieru.viewport
    (cx,cy) = self.get_position()
    if w<=width and h<=height:
      # center and lock images smaller than viewport
      self.movementEnabled=False
      self.animate(clutter.LINEAR,100, 'x', 0, 'y', 0) # align with left border
    elif w+cy < y+height:
      alignAnim = self.animate(clutter.LINEAR,100, 'y', y-h+height) # align with left border
      alignAnim.connect("completed", self._enableMovementCB)
    self.animate(clutter.LINEAR,100, 'width', w, 'height', h)

  def fitToWidth(self):
    print "to width"
    (x,y,width,height) = self.mieru.viewport
    (cx,cy,cw,ch) = self.get_geometry()
    (w,h) = self.get_size()
    factor = float(width) / w
    (newW,newH) = (w*factor,h*factor)
    self.animate(clutter.LINEAR,100, 'width', newW, 'height', newH)
    self.movementEnabled=False
    alignAnim = self.animate(clutter.LINEAR,100, 'x', 0) # align with left border
    alignAnim.connect("completed", self._enableMovementCB)
    if height > newH: # is screen higher than the image ?
      self.animate(clutter.LINEAR,100, 'y', (height-newH)/2.0)
    elif newH+cy < y+height:
      alignAnim = self.animate(clutter.LINEAR,100, 'y', y-newH+height) # align with left border
      alignAnim.connect("completed", self._enableMovementCB)

    return(newW,newH)

  def fitToHeight(self):
    (x,y,width,height) = self.mieru.viewport
    (w,h) = self.get_size()
    factor = float(height) / h
    (newW,newH) = (w*factor,h*factor)
    self.animate(clutter.LINEAR,100, 'width', newW, 'height', newH)
    self.movementEnabled=False
    alignAnim = self.animate(clutter.LINEAR,100, 'y', 0) # align with left border
    alignAnim.connect("completed", self._enableMovementCB)
    if width > newW: # is screen wider than the image ?
       self.animate(clutter.LINEAR,100, 'x', (width-newW)/2.0)
    return(newW,newH)

  def fitToScreen(self):
    (x,y,screenW,screenH) = self.mieru.viewport
    # resize to fit to screen
    if screenW > screenH:
      (newW,newH) = self.fitToHeight()
    else:
      (newW,newH) = self.fitToWidth()
    # move to the center
    shiftX = (screenW-newW)/2.0
    shiftY = (screenH-newH)/2.0
    self.movementEnabled = False
    self.animate(clutter.LINEAR,100, 'x', shiftX, 'y', shiftY)

  def resetPosition(self):
    """reset the current position to the upper left corner and return animation instance
    so that other functions can connect to the "completed" signal, etc. """
    (x,y) = self.initialPosition
    self.animate(clutter.LINEAR,100, 'x', x, 'y', y)

#    self.set_position(*self.initialPosition)
    self.movementEnabled = True

  def getPath(self):
    return self.imagePath

  def _handleResize(self,widget,event,foo):
    # resize and refit the page when viewport size changes
    fitMode = self.setFitMode(self.mieru.get('fitMode', 'original')) # implement current fit mode
    self.setFitMode(fitMode)

  def _toggleZoom(self):
    if self.zoomIn:
      (x,y,screenW,screenH) = self.mieru.viewport
      # resize to fit to longest side of the screen
      if screenW > screenH:
        self.setFitMode("width")
      else:
        self.setFitMode("height")
      self.zoomIn = False
    else:
      self.setFitMode(self.mieru.get('fitMode', 'original'))
      self.zoomIn = True
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





