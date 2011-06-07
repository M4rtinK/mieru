"""a Mieru module for displaying info menu content"""

import gtk
import os

def getShortcutsContent():
  vbox = gtk.VBox()
  shortcuts = gtk.Label()
  text = "<b><u>Keyboard shortcuts</u></b>\n"
  text+= "\n<b>Main</b>"
  text+= "\n<b>f</b> - fullscreen"
  text+= "\n<b>n</b> - open file chooser"
  text+= "\n<b>p</b> - show paging dialog"
  text+= "\n<b>c</b> - show show options window"
  text+= "\n<b>a</b> - show info window"
  text+= "\n<b>m</b> - minimize the main window"
  text+= "\n<b>k</b> - toggle kinetic scrolling"
  text+= "\n<b>q</b> - quit"
  text+= "\n<b>volume keys</b> - turn page"
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

def _updateStatsText(stats, label):
  statsText = stats.getStatsText()
  label.set_markup(statsText)

def _wipeStatsCB(button, stats, label):
  stats.resetStats()
  _updateStatsText(stats, label)

def _setStatsOnCB(button, stats, label):
  stats.setOn(button.get_active())
  _updateStatsText(stats, label)

def getStatsContent(mieru):
  """get content for the statistics monitoring tab"""
  vbox = gtk.VBox(False,0)
  statsText = mieru.stats.getStatsText()
  statsLabel = gtk.Label()
  statsLabel.set_markup(statsText)
  vbox.pack_start(statsLabel)
  hbox = gtk.HBox()
  # stats toggle button
  statsOnOff = mieru.platform.CheckButton("Keep statistics")
  statsOnOff.set_active(mieru.stats.isOn())
  statsOnOff.connect('toggled', _setStatsOnCB, mieru.stats, statsLabel)
  # stats reset button
  resetStats = mieru.platform.Button("Reset statistics")
  resetStats.connect('clicked', _wipeStatsCB, mieru.stats, statsLabel)

  hbox.pack_end(resetStats)
  hbox.pack_end(statsOnOff)
  vbox.pack_start(hbox, False, False, 5)
  vbox.show_all()
  return vbox

def getAboutContent(versionString="unknown"):
  vbox = gtk.VBox(False,0)
  textVersion = "<b>Mieru</b>, version: <b>%s</b>" % versionString
  about0 = gtk.Label()
  about0.set_markup(textVersion)

  mieruIcon = gtk.image_new_from_file('icons/mieru.svg')
  mieruIcon.set_pixel_size(200)

  text= "<i><b>Mieru project</b> contact info:</i>"
  text+= "\n<u>main developer:</u> <b>Martin Kolman</b>"
  text+= "\n<u>email</u>: <b>mieru.info@gmail.com</b>"
  text+= "\n<u>www</u>: <b>http://www.gitorious.org/mieru/</b>"
  text+= "\n<u>discusion</u>: check <b>http://talk.maemo.org</b>"

  about1 = gtk.Label()
  about1.set_markup(text)
  vbox.pack_start(about0)
  vbox.pack_start(mieruIcon)
  vbox.pack_start(about1)
  vbox.show_all()
  return vbox

def getVersionString():
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

    except Exception, e:
      print "loading version info failed"
      print e

  return versionString

def _getLabel(name, spacing=0):
  vbox = gtk.VBox(False, spacing)
  vbox.pack_start(gtk.Label(name),padding=spacing)
  vbox.show_all()
  return vbox

class InfoNotebook(gtk.Notebook):
  def __init__(self, mieru):
    gtk.Notebook.__init__(self)
    self.mieru = mieru
    self.versionString = getVersionString()
    enlargeTabs = 15
    versionString = self.getVersionString()
    self.append_page(getShortcutsContent(),_getLabel("Shortcuts",enlargeTabs))
    self.append_page(getStatsContent(self.mieru),_getLabel("Stats", enlargeTabs))
    self.append_page(getAboutContent(versionString),_getLabel("About", enlargeTabs))
    self.show_all()
    self.set_current_page(0)







