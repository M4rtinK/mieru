""" a clutter based GUI for Mieru """

"""
NOTE: PyClutter 1.0 import order:
import cluttergtk
import clutter
import gtk
"""

import cluttergtk
import clutter
import pygtk
pygtk.require('2.0')
import gtk

import gtk_gui
import buttons
import clutter_page

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
    self.stage.connect('allocation-changed', self._handleResize)
    self.stage.realize()
    self.stage.set_color("White")

    # activate clutter based buttons
    self.buttons = buttons.ClutterButtons(self.mieru, self)

    # create the manga layer
    self.mangaLayer = clutter.Group()
    # stick it under the button layer
    self.stage.add(self.mangaLayer)
    self.stage.lower_child(self.mangaLayer, self.buttons.getLayer())

    # This packs the button into the window (a GTK container).
    self.embed.show()

    # setup page turning
    self._setupPageTurning()
    self.activePage = None

    # page preview
    self.previewBox = None
    self.previewBoxStartingPoint = (0,0)

    # and show the window
    self.window.show_all()


  def _setupPageTurning(self):
    self.pageTurnTl = clutter.Timeline(200)
    self.pageTurnAlpha = clutter.Alpha(self.pageTurnTl, clutter.EASE_IN_CIRC)
    self.fadeIn = self._fadeInOpac
    self.fadeOut = self._fadeOutOpac
    # page turn complete notifications
    self.pageShownCB = None
    self.pageTurnTl.connect('completed', self._pageTurnDoneCB)
    self.oldPage = None

  def _fadeInOpac(self, page):
    self.a1 = clutter.BehaviourOpacity(0,255,self.pageTurnAlpha)
    self.a2 = clutter.BehaviourDepth(-255,0,self.pageTurnAlpha)
    self.a1.apply(page)
    self.a2.apply(page)
    
  def _fadeOutOpac(self, page):
    self.b1 = clutter.BehaviourOpacity(255,0,self.pageTurnAlpha)
    self.b2 = clutter.BehaviourDepth(0,255,self.pageTurnAlpha)
    self.b1.apply(page)
    self.b2.apply(page)

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

  def getPage(self, flo, name="", fitOnStart=True):
    pb = self._flo2pixbuf(flo)
    flo.close()
    return clutter_page.ClutterPage(pb, self.mieru, name, fitOnStart)

  def getCurrentPage(self):
    return self.activePage

  def showPage(self, page):
    """show a page on the stage"""

    self._addToMangaLayer(page)

    # fade out & destroy the old page (if it exists)
    if self.activePage:
      self.oldPage = self.activePage
      self.fadeOut(self.oldPage)
    # fade in the new page
    self.fadeIn(page)
    self.activePage = page
    self.pageTurnTl.start()

  def pageShownNotify(self, cb):
    self.pageShownCB = cb

  def clearStage(self):
    if self.activePage:
      self._removeAndDestroy("timeline", self.activePage)
      self.activePage = None

  def _addToMangaLayer(self, page):
    if self.mangaLayer:
      self.mangaLayer.add(page)
    else:
      "manga: error, no manga layer"

  def _pageTurnDoneCB(self, timeline):
    self._removeAndDestroyOldPage()
    self._pageShownNotify()

  def _removeAndDestroyOldPage(self):
    """remove a page from the stage and destroy it"""

    # does it exist ?
    if self.oldPage:
      # hide it
      self.oldPage.hide()

      # remove the page from the manga layer
      if self.mangaLayer and self.oldPage:
        self.mangaLayer.remove(self.oldPage)

      # deactivate it
      self.oldPage.deactivate()

      # no need to remove page manually
      # -> it will be cleared by page cache management

  def _pageShownNotify(self):
    if self.pageShownCB:
      self.pageShownCB()

  # page preview
  def _getPBoxCoords(self, type):
    """compute coordinates for the preview box"""
    (x,y,w,h) = self.getViewport()
    pBoxSide = h/2.0
    border = pBoxSide/20.0
    pBoxInSide = pBoxSide-2*border

    pBoxY = x/2.0+pBoxSide/2.0
    pBoxX = w
    pBoxShownX = w - pBoxSide
    """ previous - box on the left, next - box on the right
    (corresponding to the volume buttons)"""
    if type == "previous":
      pBoxX = 0 - pBoxSide
      pBoxShownX = 0
    return (pBoxY,pBoxX,pBoxShownX,pBoxSide,pBoxInSide,border)


  def showPreview(self, thumbnail, type, pressedAction=None):
    if self.previewBox: # replace previous preview
      self.hidePreview()

    (pBoxY,pBoxX,pBoxShownX,pBoxSide,pBoxInSide,border) = self._getPBoxCoords(type)
    # 50% transparent yellow TODO: take this from current OS theme ?
    backgroundColor = clutter.color_from_string("yellow")
    backgroundColor.alpha=128
    background = clutter.Rectangle(color=backgroundColor)
    background.set_size(pBoxSide,pBoxSide)
    background.set_reactive(True)
    background.connect('button-release-event',self._previewPressedCB, pressedAction)

    # resize and fit in the thumbnail
    thumbnail.set_keep_aspect_ratio(True)
    (tw,th) = thumbnail.get_size()
    wf = float(pBoxInSide)/tw
    hf = float(pBoxInSide)/th
    if tw >= th:
      thumbnail.set_size(tw*wf, th*wf)
    else:
      thumbnail.set_size(tw*hf, th*hf)
    (tw,th) = thumbnail.get_size()
    print (tw,th)
    thumbnail.move_by(border+(pBoxInSide-tw)/2.0,border+(pBoxInSide-th)/2.0)

    # create a container for the thumbnail and background
    box = clutter.Group()
    box.add(background)
    box.add(thumbnail)
    # TODO: preview layer above the buttons layer ?
    self.buttons.getLayer().add(box)
    box.show()
    box.set_position(pBoxX,pBoxY)
    self.previewBoxStartingPoint = (pBoxX,pBoxY)
    box.animate(clutter.LINEAR,300,"x", pBoxShownX)
    self.previewBox = box


  def _previewPressedCB(self, actor, event, action):
    """the preview box has been pressed,
    load next/previous manga - the action is a binding to the
    next/previous method

    we use the gobject idle_add method so that it does not block
    right after clicking the preview
    """
    if action:
      self.idleAdd(action)

  def hidePreview(self):
    """hide a displayed preview"""
    if self.previewBox:
      (x,y) = self.previewBoxStartingPoint
      print "manga: hiding preview"
      animation = self.previewBox.animate(clutter.LINEAR,300,"x", x)
      animation.get_timeline().connect('completed', self._killPreviewCB, self.previewBox)


  def _killPreviewCB(self, timeline, actor):
    """hide and unrealize a given actor"""
    actor.hide()
    actor.unrealize()
    self.buttons.getLayer().remove(actor)
    self.previewBox = None

  def _handleResize(self,widget,event,foo):
    """handle resizing of the stage"""
    if self.previewBox:
      (x,y,w,h) = self.getViewport()
      pBoxSide = h/2.0
      newY = x/2.0+pBoxSide/2.0
      self.previewBox.animate(clutter.LINEAR,100,"y", newY, "width",pBoxSide, "height", pBoxSide)

  def statusReport(self):
    print("main stage:", self.stage.get_children())
    print("manga layer:", self.mangaLayer.get_children())
    print("buttons:", self.buttons.getLayer().get_children())

