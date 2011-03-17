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
        print "creating profile folder failed: %s" % e
        return False

  def save(self):
    print "options: saving options"
    try:
      f = open(self.optionsPath, "w")
      marshal.dump(self.mieru.d, f)
      f.close()
      print "options: successfully saved"
    except IOError:
      print "Can't save options"

  def load(self):
    try:
      f = open(self.optionsPath, "r")
      loadedData = marshal.load(f)
      f.close()
      self.mieru.d = loadedData
    except Exception, e:
      print "options: exception while loading saved options:\n%s" % e


