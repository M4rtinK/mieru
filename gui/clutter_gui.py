""" a clutter based stage for mangas and buttons """

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

    # and show the window
    self.window.show_all()


  def _setupPageTurning(self):
    self.pageTurnTl = clutter.Timeline(200)
    self.pageTurnAlpha = clutter.Alpha(self.pageTurnTl, clutter.EASE_IN_CIRC)
    self.fadeIn = self._fadeInOpac
    self.fadeOut = self._fadeOutOpac
    # page turn complete notifications
    self.pageShownCB = None
    self.pageTurnTl.connect('completed', self._pageShownNotifyCB)
    self.pageTurnTl.connect('completed', self._removeAndDestroyOldPageCB)
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

  def showPreview(self, type, page):
    """show a preview for a page"""
    pass

  def hidePreview(self):
    """hide any visible previews"""
    pass

  def showPage(self, page):
    """show a page on the stage"""

    # check if there is already a page loaded
    self._addToMangaLayer(page)

    # fade out & destroy the old page (if it exists)
    if self.activePage:
      self.oldPage = self.activePage
      self.fadeOut(self.oldPage)
    # fade in the new page
    self.fadeIn(page)
    self.pageTurnTl.start()

    self.activePage = page

  def pageShownNotify(self, cb):
    self.pageShownCB = cb

  def _pageShownNotifyCB(self, timeline):
    if self.pageShownCB:
      self.pageShownCB()

  def clearStage(self):
    if self.activePage:
      self._removeAndDestroy("timeline", self.activePage)
      self.activePage = None

  def _addToMangaLayer(self, page):
    if self.mangaLayer:
      self.mangaLayer.add(page)
    else:
      "manga: error, no manga layer"

  def _removeAndDestroyOldPageCB(self, timeline):
    """remove a page from the stage and destroy it"""

    # remove the page from the manga layer
    if self.mangaLayer and self.oldPage:
      print "removing from stage"
      self.mangaLayer.remove(self.oldPage)

    # quickly free resources held by the old page
    if self.oldPage:
      # kill it with fire
      self.oldPage.unrealize()
      self.oldPage.destroy()
      self.oldPage = None
