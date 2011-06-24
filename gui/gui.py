"""a GUI chooser"""

class GUI:
  def __init__(self, mieru):
    self.mieru = mieru

  def resize(self, w, h):
    """resize the GUI to given width and height"""
    pass

  def getWindow(self):
    """return the main window"""
    pass

  def getViewport(self):
    """return a (x,y,w,h) tupple"""
    pass

  def setWindowTitle(self, title):
    """set the window title to a given string"""
    pass

  def getToolkit(self):
    """report which toolkit the current GUI uses"""
    return

  def getAccel(self):
    """report if current GUI supports acceleration"""
    pass

  def toggleFullscreen(self):
    pass

  def startMainLoop(self):
    """start the main loop or its equivalent"""
    pass

  def stopMainLoop(self):
    """stop the main loop or its equivalent"""
    pass

  def showPreview(self, type, page):
    """show a preview for a page"""
    pass

  def hidePreview(self):
    """hide any visible previews"""
    pass

  def getPage(self, flObject, name="", fitOnStart=True):
    """create a page from a file like object"""
    pass

  def showPage(self, page):
    """show a page on the stage"""
    pass

  def clearStage(self):
    pass

  def _destroyed(self):
    self.mieru.destroy()

  def _keyPressed(self, keyName):
    self.mieru.keyPressed(keyName)


def getGui(mieru, type="gtk",accel=True, size=(800,480)):
  """return a GUI object"""
  if accel:
    import cluttergtk
    import clutter_gui
    return clutter_gui.ClutterGTKGUI(mieru, type, size)







