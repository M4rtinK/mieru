# -*- coding: utf-8 -*-
"""
Mieru Android platform module
"""
from platforms.base_platform import BasePlatform


class Android(BasePlatform):
  def __init__(self, mieru):
    BasePlatform.__init__(self)
    self.mieru = mieru
    self._cleanCoreDumps()

  def getIDString(self):
    return "android"

  def getName(self):
    return "Android"

  def getDeviceName(self):
    # TODO: advanced device detection ?
    # -> CPU architecture ?
    # -> tablet VS smartphone ?
    # -> somehow getting device name ?
    # NOTE: this string is not yet shown anywhere :)
    return "An Android device"


  def notify(self, message, icon=""):
    self.mieru.gui._notify(message, icon)

  def getDefaultFileSelectorPath(self):
    """we default to the MyDocs folder as this is where most
    users will store their mangas and comic books"""
    return "/sdcard"

  def showQuitButton(self):
    """Swype handles window closing"""
    return False

  def showMinimiseButton(self):
    """Swype handles window switching"""
    return False

  def getScreenWH(self):
    return 1024, 768

  def startInFullscreen(self):
    return True