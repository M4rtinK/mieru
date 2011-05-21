"""a Mieru module for displaying info menu content"""

import gtk
import os

import hildon

def getShortcutsContent():
  vbox = gtk.VBox()
  shortcuts = gtk.Label()
  text = "<b>Keyboard shortcuts</b>\n"
  text+= "\n\n<b>Main</b>"
  text+= "\n<b>f</b> - fullscreen"
  text+= "\n<b>n</b> - open file chooser"
  text+= "\n<b>p</b> - show paging dialog"
  text+= "\n<b>m</b> - minimize the main window"
  text+= "\n<b>k</b> - toggle kinetic scrolling"
  text+= "\n<b>q</b> - quit"
  text+= "\n<b>volume keys</b> - turn pages"
  text+= "\n\n<b>Page fitting</b>"
  text+= "\n<b>o</b> - original size"
  text+= "\n<b>i</b> - fit to width"
  text+= "\n<b>u</b> - fit to height"
  text+= "\n<b>z</b> - fit to screen"
  text+= "\n<b>doubletap</b> - temporary fit to screen"

  shortcuts.set_markup(text)

  vbox.pack_start(shortcuts)
  vbox.show_all()
  return vbox

def getStatsContent(mieru):
  vbox = gtk.VBox(False,0)
  statsText = mieru.stats.getStatsText()
  stats = gtk.Label()
  stats.set_markup(statsText)
  vbox.pack_start(stats)
  hbox = gtk.HBox()
  statsOnOff = gtk.CheckButton("keep statistics")
  resetStats = gtk.Button("Reset statistics")
  hbox.pack_end(resetStats)
  hbox.pack_end(statsOnOff)
  vbox.pack_start(hbox, False, False, 5)
  vbox.show_all()
  return vbox

def getAboutContent(versionString="unknown"):
  vbox = gtk.VBox(False,0)
  about = gtk.Label()
  text = "<b>Mieru</b> version: <b>%s</b>\n" % versionString
  text+= "\nadd icon here\n"
  text+= "\nContact the <b>Mieru</b> project:"
  text+= "\nmain developer: <b>Martin Kolman</b>"
  text+= "\nemail: <b>mieru.info@gmail.com</b>"
  text+= "\nwww: add WWW :)"

  about.set_markup(text)
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






