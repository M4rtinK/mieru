# -*- coding: utf-8 -*-
"""Mieru persistent options storage"""
import marshal
import os
import sys

DEFAULT_PROFILE_FOLDER_NAME = '.mieru'
OPTIONS_FILENAME = 'mieru_options.bin'

class Options:
  def __init__(self, mieru):
    self.mieru = mieru
    self.profileFolderPath = self.getPlatformProfilePath()
    if self.profileFolderPath is None:
      userHomePath = os.getenv("HOME", "")
      self.profileFolderPath = os.path.join(userHomePath, DEFAULT_PROFILE_FOLDER_NAME)
    self.optionsPath = os.path.join(self.profileFolderPath, OPTIONS_FILENAME)
    self.checkProfilePath()
    print("options: profile path: %s" % self.profileFolderPath)
    self.load()

  # TODO: do this cleaner ?
  def getPlatformProfilePath(self):
    if sys.platform == "android":
      return "/sdcard/.mieru"
    else:
      return None

  def checkProfilePath(self):
    """check if the profile folder exists, try to create it if not"""
    if os.path.exists(self.profileFolderPath):
      return True
    else:
      try:
        os.makedirs(self.profileFolderPath)
        print("creating profile folder in: %s" % self.profileFolderPath)
        return True
      except Exception, e:
        print("options:Creating profile folder failed:\n%s" % e)
        return False

  def save(self):
#    print("options: saving options")
    try:
      f = open(self.optionsPath, "w")
      marshal.dump(self.mieru.getDict(), f)
      f.close()
#      print("options: successfully saved")
    except Exception, e:
      print("options: Exception while saving options:\n%s" % e)

  def load(self):
    try:
      f = open(self.optionsPath, "r")
      loadedData = marshal.load(f)
      f.close()
      self.mieru.setDict(loadedData)
    except Exception, e:
      self.mieru.setDict({})
      print("options: exception while loading saved options:\n%s" % e)


