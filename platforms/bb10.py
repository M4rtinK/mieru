# -*- coding: utf-8 -*-
"""
Mieru hildon UI (for Maemo 5@N900)
"""

from base_platform import BasePlatform


class BB10(BasePlatform):
  def __init__(self, mieru):
    BasePlatform.__init__(self)
    self.mieru = mieru

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
    return "."

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