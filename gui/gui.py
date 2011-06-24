"""a GUI chooser"""

class GUI:
  def __init__(self, mieru):
    self.mieru = mieru

  def resize(self, w, h):
    pass

  def getWindow(self):
    pass

  def getViewport(self):
    pass

  def setWindowTitle(self, title):
    pass

  def setManga(self, manga):
    pass

  def getToolkit(self):
    return

  def getAccel(self):
    pass

  def toggleFullscreen(self):
    pass

  def startMainLoop(self):
    """start the main loop or its equivalent"""
    pass

  def stopMainLoop(self):
    """stop the main loop or its equivalent"""
    pass

  def _destroyed(self):
    self.mieru.destroy()

  def _keyPressed(self, keyName):
    self.mieru.keyPressed(keyName)




def getGui(mieru, type="gtk",accel=True, size=(800,480)):
  if accel:
    import cluttergtk
    import clutter_gui
    return clutter_gui.ClutterGTKGUI(mieru, type, size)







