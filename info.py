"""a Mieru module for displaying info menu content"""

import gtk
import os

def getShortcutsContent():
  vbox = gtk.VBox()
  shortcuts = gtk.Label("shortcuts")
  vbox.pack_start(shortcuts)
  vbox.show_all()
  return vbox

def getStatsContent(mieru):
  vbox = gtk.VBox()
  statsText = mieru.stats.getStatsText()
  stats = gtk.Label(statsText)
  vbox.pack_start(stats)
  vbox.show_all()
  return vbox

def getAboutContent(versionString="unknown"):
  vbox = gtk.VBox()
  about = gtk.Label("Mieru version: %s" % versionString)
  vbox.pack_start(about)
  vbox.show_all()
  return vbox

def _getLabel(name, spacing=0):
  vbox = gtk.VBox(False, spacing)
  vbox.pack_start(gtk.Label(name),padding=spacing)
  vbox.show_all()
  return vbox

class InfoNotebook(gtk.Notebook):
  def __init__(self, mieru):
    gtk.Notebook.__init__(self)
    self.mieru = mieru
    enlargeTabs = 15
    versionString = self.getVersionString()
    self.append_page(getShortcutsContent(),_getLabel("Shortcuts",enlargeTabs))
    self.append_page(getStatsContent(self.mieru),_getLabel("Stats", enlargeTabs))
    self.append_page(getAboutContent(versionString),_getLabel("About", enlargeTabs))
    self.show_all()


  def getVersionString(self):
    versionString = "unknown version"
    versionFilePath = 'version.txt'

    # try read the version file
    if os.path.exists(versionFilePath):
      try:
        f = open(versionFilePath, 'r')
        versionString = f.read()
        f.close()
        # is it really string ?
        versionString = str(versionString)
        self.versionString = versionString
      except Exception, e:
        print "loading version info failed"
        print e

    return versionString






