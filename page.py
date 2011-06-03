"""page.py - a manga/comix book page"""

import math
import clutter

import buttons

import utils

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
    self.lastMotionTimestamp = 0
    self.lastDTDXDY = (0,0,0)
    self.clickCount = 0
    self.msButtonLastReleaseTimestamp = 0

    self.ppms = (1,1)
    self.decelTl = clutter.Timeline(10000)
    self.decelTl.connect('new_frame', self._decelerateCB)
    self.lastdecelElapsed = 0
    self.stopDecel = True

    """first number id for the horizontal and seccond for the vertical axis,
    0 means movement in this axis is disabled, 1 means movement is enabled"""
    self.movementEnabled = (1,1) # the page is fit to screen so it should not be move


    self.zoomIn=True
    self.msButtonLastPressTimestamp = None
    self.pressLength = 100

    self.connect('button-press-event', self.do_button_press_event)
    self.connect('button-release-event', self.do_button_release_event)
    self.mieru.stage.connect('allocation-changed', self._handleResize)

    self.set_keep_aspect_ratio(True) # we want to preserve the aspect ratio

  def do_button_press_event (self, page, event):
    self.isPressed = True
    (x,y) = event.x,event.y
    self.msButtonLastPressTimestamp = event.time
    self.lastDTDXDY = (0,0,0)
    page.lastMotionTimestamp = event.time
    
    # stop any decelaration in progress
    self.decelTl.stop()

    self.stopDecel = True
      
    self.pressStart = (x,y)
    self.lastMotion = (x,y)

    return False

  def do_button_release_event (self, page, event):
    (x1,y1) = self.pressStart
    (dx,dy) = (x1-event.x,y1-event.y)
    # time from last button release
    dt = event.time - self.msButtonLastReleaseTimestamp

    # check if event was a click or drag
    if buttons.wasClick(dx, dy):
      if dt < 500:
        self.clickCount+=1 # dlouble click +
      else:
        self.clickCount=1 # single click
    else:
      self.clickCount=0 # drag

    if self.clickCount >=2: # is this a doubleclick ?
      self._toggleZoom() # toggle zoom in/out
    else: # continue drag as kinetic scrolling (if enabled)
      if self.mieru.get('kineticScrolling', False):
        """if the user clicked - dont start any kinetic scrolling
           if the user crossed the drag treshold, start kinetic scrolling"""
        if not self.clickCount: # last event was a drag
          (dt, dx, dy) = self.lastDTDXDY
          self.ppms = (dx/dt,dy/dt)
          self.lastdecelElapsed = 0
          self.stopDecel = False
          self.decelTl.start()
      """any previous kinetic scrolling is stopped once the screen is pressed,
      no need to stop it here"""

    self.isPressed = False
    self.pressStart = None
    self.lastMotion = None
    self.msButtonLastReleaseTimestamp = event.time

    return False

  
# in case this this is needed someday :
#    pxDistance = math.hypot(dx,dy)
#    buttons.wasDoubleclick(event.get_click_count(), pxDistance , event.time - self.fsButtonLastPressTimestamp)

#      print event.time - self.lastMovementTimestamp
#      (x,y) = event.x,event.y
#      if page.lastMotion:
#        (lasX,lastY) = page.lastMotion
#        (dx,dy) = (x-lasX,y-lastY)
#        print (dx,dy)
#        print page.lastMotion
#        print event.x,event.y


  def on_page_motion(self, page, event):
#    print page, event
#    print dir(event)
    (x,y) = event.x,event.y
    if page.lastMotion:
      (lasX,lastY) = page.lastMotion
      (dx,dy) = (x-lasX,y-lastY)
    else:
      (dx,dy) = (0,0)
    page.lastMotion = (x,y)
    page.lastDTDXDY = (event.time - page.lastMotionTimestamp, dx,dy)
    page.lastMotionTimestamp = event.time

    if self.isPressed:
      self.movePage(page,dx*page.movementEnabled[0],dy*page.movementEnabled[1])
    return False

  def movePage(self,page,dx,dy):
    """move the page so that the voewport either stays inside it
       or the page stays inside the viewport if it is smaller"""
    (x,y,w,h) = self.mieru.viewport
    (pageX,pageY,pageW,pageH) = page.get_geometry()
    (newX,newY) = (pageX+dx,pageY+dy)
    wCollision = False
    hCollision = False

    if pageW > w: # page is wider than screen
      if newX < w-pageW:
        newX = w-pageW
        wCollision = True
      elif newX > 0:
        newX = 0
        wCollision = True
    else: # screen is wider than page
      if newX < 0:
        newX = 0
        wCollision = True
      if newX > w-pageW:
        newX = w-pageW
        wCollision = True

    if pageH > h: # page is longer than screen
      if newY < h-pageH:
        newY = h-pageH
        hCollision = True
      elif newY > 0:
        newY = 0
        hCollision = True
    else: # screen is longer than page
      if newY < 0:
        newY = 0
        hCollision = True
      if newY > pageH-h:
        newY = pageH-h
        hCollision = True
#    page.set_clip(newX*(-1), newY*(-1), w, h)
    page.move_by(newX - pageX,newY - pageY)

    return (wCollision, hCollision)

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

  def _enableMovementCB(self, timeline, movementTupple=None):
    """enable movement after an animation finishes"""
    (we,he) = self.movementEnabled
    if movementTupple == None:
      self.movementEnabled = (1,1)
    else:
      (we1,he1) = movementTupple
      if we1 == None:
        we1 = we
      if he1 == None:
        he1 = he
      self.movementEnabled = (we1,he1)

  def _decelerateCB(self, timeline, foo):
    (dxPMS, dyPMS) = self.ppms
    dt = timeline.get_delta()
#    print (dxPMS*dt, dyPMS*dt)
    if self.stopDecel or self.movePage(self, dxPMS*dt, dyPMS*dt) == (True, True):
      print "stopping"
      timeline.stop()

  def setOriginalSize(self):
    """resize back to original size"""
    (w, h) = self.originalSize
    (x,y,width,height) = self.mieru.viewport
    (cx,cy) = self.get_position()
    if w<=width and h<=height:
      # center and lock images smaller than viewport
      self.movementEnabled=(0,0)
      # move to the middle of the screen and lock it there
      self.animate(clutter.LINEAR,100, 'x', (width-w)/2.0, 'y', (height-h)/2.0)

    elif w >= width: #page is wider than viewport
      self.movementEnabled=(0,0)
      # align with left border
      alignAnim = self.animate(clutter.LINEAR,100, 'x', 0)
      alignAnim.connect("completed", self._enableMovementCB, (1,1))
    elif w < width: # viewport is wider than page
      # position in the middle and lock horizontal movement
      alignAnim1 = self.animate(clutter.LINEAR,100, 'x', x+((width-w)/2.0) )
      alignAnim1.connect("completed", self._enableMovementCB, (0,None))
    if h < height: # viewport is higher than page
      # position in the middle and lock vertical movement
      alignAnim2 = self.animate(clutter.LINEAR,100, 'y', y+((height-h)/2.0) )
      alignAnim2.connect("completed", self._enableMovementCB, (None,0))

    self.animate(clutter.LINEAR,100, 'width', w, 'height', h)

  def fitToWidth(self):
    print "to width"
    (x,y,width,height) = self.mieru.viewport
    (cx,cy,cw,ch) = self.get_geometry()
    (w,h) = self.get_size()
    factor = float(width) / w
    (newW,newH) = (w*factor,h*factor)
    self.animate(clutter.LINEAR,100, 'width', newW, 'height', newH)
    self.movementEnabled=(0,0)
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
    self.movementEnabled=(0,0)
    alignAnim = self.animate(clutter.LINEAR,100, 'y', 0) # align with left border
    alignAnim.connect("completed", self._enableMovementCB, (0, None))
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
    self.movementEnabled=(0,0)
    self.animate(clutter.LINEAR,100, 'x', shiftX, 'y', shiftY)

  def resetPosition(self):
    """reset the current position to the upper left corner and return animation instance
    so that other functions can connect to the "completed" signal, etc. """
    (x,y) = self.initialPosition
    self.animate(clutter.LINEAR,100, 'x', x, 'y', y)

#    self.set_position(*self.initialPosition)
    self.movementEnabled = (1,1)

  def getPath(self):
    return self.imagePath

  def _handleResize(self,widget,event,flags):
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





