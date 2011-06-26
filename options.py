"""Mieru persistent options storage"""
import marshal
import os

class Options:
  def __init__(self, mieru):
    self.mieru = mieru
    optionsFilename = 'mieru_options.bin'
    mieruProfileFolderName = '.mieru'
    userHomePath = os.getenv("HOME")
    self.profileFolderPath = os.path.join(userHomePath, mieruProfileFolderName)
    self.optionsPath = os.path.join(self.profileFolderPath, optionsFilename)
    self.checkProfilePath()
    print "options: profile path: %s" % self.profileFolderPath
    self.load()

  def checkProfilePath(self):
    """check if the profile folder exists, try to create it if not"""
    if os.path.exists(self.profileFolderPath):
      return True
    else:
      try:
        os.makedirs(self.profileFolderPath)
        print "creating profile folder in: %s" % self.profileFolderPath
        return True
      except Exception, e:
        print "options:Creating profile folder failed:\n%s" % e
        return False

  def save(self):
#    print "options: saving options"
    try:
      f = open(self.optionsPath, "w")
      marshal.dump(self.mieru.getDict(), f)
      f.close()
#      print "options: successfully saved"
    except Exception, e:
      print "options: Exception while saving options:\n%s" % e

  def load(self):
    try:
      f = open(self.optionsPath, "r")
      loadedData = marshal.load(f)
      f.close()
      self.mieru.setDict(loadedData)
    except Exception, e:
      self.mieru.setDict({})
      print "options: exception while loading saved options:\n%s" % e


