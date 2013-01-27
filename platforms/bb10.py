# -*- coding: utf-8 -*-
"""
Mieru hildon UI (for Maemo 5@N900)
"""
import glob
import os
from platforms.base_platform import BasePlatform


class BB10(BasePlatform):
  def __init__(self, mieru):
    BasePlatform.__init__(self)
    self.mieru = mieru
    self._cleanCoreDumps()

  def getIDString(self):
    return "bb10"

  def getName(self):
    return "BlackBerry 10"

  def getDeviceName(self):
    return "BlackBerry 10 device"

  def notify(self, message, icon=""):
    self.mieru.gui._notify(message, icon)

  def getDefaultFileSelectorPath(self):
    """we default to the MyDocs folder as this is where most
    users will store their mangas and comic books"""
    return "/accounts/1000/shared/downloads"

  def showQuitButton(self):
    """Swype handles window closing"""
    return False

  def showMinimiseButton(self):
    """Swype handles window switching"""
    return False

  def getScreenWH(self):
    return 720, 1280

  def startInFullscreen(self):
    return True

  def _cleanCoreDumps(self):
    """due to experimental OpenGL support when using QtQuick with QBB_USE_OPENGL,
    there might sometimes be creates python3.2 core dumps even though the program cleanly exits
    -> this function cleans them on startup"""

    corePath = os.path.join(self.mieru.originalCWD, 'logs', '*.core')
    for core in glob.glob(corePath):
      try:
        os.remove(core)
      except Exception as e:
        print("removing core-dump failed")
        print(e)