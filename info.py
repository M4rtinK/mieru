# -*- coding: utf-8 -*-
"""a Mieru module for displaying info menu content"""

import os

VERSION_FILE_PATH = "version.txt"
RELEASE_NOTES_FILE_PATH = "release_notes.txt"

def getShortcutsContent():
  import gtk
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
  text+= "\n<b>double-tap</b> - temporary fit to screen"

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
  import gtk
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

def getAboutText(forum="meego"):
  #text= "<b>Mieru project</b> contact info:"
  text= "<p><b>main developer:</b> Martin Kolman</p>"
  text+= '<p><b>email</b>: <a href="mailto:mieru.info@gmail.com">mieru.info@gmail.com</a></p>'
  text+= '<p><b>www</b>:  <a href="http://m4rtink.github.com/mieru/">http://m4rtink.github.com/mieru/</a></p>'
  if forum == "meego":
    text+= '<p><b>discussion</b>: <a href="http://forum.meego.com/showthread.php?t=5405">forum.meego.com thread</a></p>'
  else:
    text+= '<p><b>discussion</b>: check <a href="http://talk.maemo.org/showthread.php?t=73907">talk.maemo.org thread</a></p>'
  return text

def getAboutContent(versionString="unknown"):
  import gtk
  vbox = gtk.VBox(False,0)
  textVersion = "<b>Mieru</b>, version: <b>%s</b>" % versionString
  about0 = gtk.Label()
  about0.set_markup(textVersion)

  mieruIcon = gtk.image_new_from_file('icons/mieru_150x150.png')
#  mieruIcon.set_pixel_size(200)
  about1 = gtk.Label()
  about1.set_markup(getAboutText())
  vbox.pack_start(about0)
  vbox.pack_start(mieruIcon)
  vbox.pack_start(about1)
  vbox.show_all()
  return vbox

def getVersionString():
  """Return current version string
  EXAMPLE:
  V2.3.1 git:c10f25d
  if current version is unknown, return None
  """
  versionString = None
  # try read the version file
  if os.path.exists(VERSION_FILE_PATH):
    try:
      f = open(VERSION_FILE_PATH, 'r')
      versionString = f.read()
      f.close()
      # is it really string ?
      versionString = str(versionString)
    except Exception, e:
      print("loading version info failed")
      print(e)
  return versionString

def getVersionNumber():
  """return version as a (primary, secondary, build) tuple
  EXAMPLE:
  V2.3.1 git:c10f25d -> (2,3,1)
  if current version is unknown, return None
  """
  versionString = getVersionString()
  if versionString is None:
    return None
  else:
    try: # version string example: V2.3.1 git:c10f25d
      versionString = versionString[1:] # drop leading V
      versionString = versionString.split(' ')[0] # drop git tag
      c1, c2, c3 = versionString.split('.')
      return int(c1), int(c2), int(c3)
    except Exception, e:
      print('info: parsing version number failed')
      print(e)
      return None

def getNumericVersionString():
  m, n, b = getVersionNumber()
  return "%d.%d.%d" % (m, n, b)


def nvs2tuple(nvString):
  """numeric version string to version tuple"""
  a, b, c = nvString.split('.')
  return int(a), int(b), int(c)

def tuple2nvs(versionTuple):
  """numeric version tuple to numeric version string"""
  return "%d.%d.%d" % versionTuple

def getReleaseNotes():
  """return release notes fir the given version string
  (major.minor.build, EXAMPLE: "2.3.1")
  if no release notes are found, return None
  """
  # release notes aren't displayed on each start
  # (eq if the user marked the current notes as
  # read or disabled release notes altogether)
  # so import configobj only when needed
  versionNumbers = None
  try:
    from modules.configobj import ConfigObj
    releaseNotes = ConfigObj(RELEASE_NOTES_FILE_PATH)
    versionNumbers = releaseNotes['release_notes_section'].keys()
  except Exception, e:
    print('info: loading release notes failed')
    print(e)
  if versionNumbers:
    maxVersion = max(map(lambda x: nvs2tuple(x), versionNumbers))
    # TODO: localized release notes ? (would be nice in Chinese)
    notesMarkdown = releaseNotes['release_notes_section'][tuple2nvs(maxVersion)]['notes']
    import modules.markdown as markdown
    notesHTML = markdown.markdown(notesMarkdown)
    print notesHTML
    return maxVersion, notesHTML
  else:
    return None, None

def getGitHash():
  """return Git hash for the current version
  EXAMPLE:
  V2.3.1 git:c10f25d -> c10f25d
  if current version is unknown, return None
  """

  versionString = getVersionString()
  if versionString is None:
    return None
  else:
    try: # version string example: V2.3.1 git:c10f25d
      versionString = versionString.split(' ')[1] # drop the version
      gitHash = versionString.split(':')[1] # drop the git: prefix
      return gitHash
    except Exception, e:
      print('info: parsing version number failed')
      print(e)
      return None

def _getLabel(name, spacing=0):
  import gtk
  vbox = gtk.VBox(False, spacing)
  vbox.pack_start(gtk.Label(name),padding=spacing)
  vbox.show_all()
  return vbox

def getInfNotebook(mieru):
  import gtk
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
  return InfoNotebook(mieru)









