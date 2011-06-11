#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import time
import cluttergtk

# Mieru modules import
import buttons
import manga
import options
import startup
import stats

class Mieru:

  def destroy(self, widget, data=None):
    # log elapsed time
    sessionTime = time.time() - self.startupTimeStamp
    self.stats.updateUsageTime(sessionTime)

    self.saveState()
    print "mieru quiting"
    gtk.main_quit()

  def __init__(self):
    # log start
    self.startupTimeStamp = time.time()

    # parse startup arguments
    start = startup.Startup()
    args = start.args


    # restore persistent options
    self.d = {}
    self.options = options.Options(self)
    # options value watching
    self.maxWatchId = 0
    self.watches = {}

    # enable stats
    self.stats = stats.Stats(self)

    # class varibales
    self.fullscreen = False
    self.viewport = (0,0,800,480)
    (x,y,w,h) = self.viewport
#    self.continuousReading = self.get('continuousReading',True)
    self.continuousReading = True

    # create a new window
    if args.u == "hildon":
      # hildon should be imported by now by the Maemo5 platform module
      import hildon
      self.window = hildon.StackableWindow()
    else:
      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

    self.window.resize(w,h)
    # resize the viewport when window size changes
    self.window.connect('size-allocate', self._resizeViewport)

    # suhtdown when the main window is destroyed
    self.window.connect("destroy", self.destroy)

    # get the Clutter embed and add it to the window
    self.embed = cluttergtk.Embed()
    self.vbox = gtk.VBox(False, 2)
    self.window.add(self.vbox)
    
    # get the platform module
    if args.u == "hildon":
      import maemo5
      self.platform = maemo5.Maemo5(self)
    else:
      import pc
      self.platform = pc.PC(self)

    self.vbox.pack_start(self.embed)
    self.vbox.show_all()


    # we need to realize the widget before we get the stage
    self.embed.realize()
    self.embed.show()
    self.embed.connect('key-press-event', self.on_key_press_event)

    # get the stage
    self.stage = self.embed.get_stage()
    self.stage.realize()
    self.stage.set_color("White")

    # activate clutter based buttons
    self.buttons = buttons.Buttons(self)

    
    self.activeManga = None

    # restore previously saved state (if available)
    self._restoreState()
    
    self.lastPageMotionXY = (0,0)



    # This packs the button into the window (a GTK container).

    self.embed.show()

    # and the window
    self.window.show()

    gtk.main()

  def getViewport(self):
    return self.viewport

  def getWindow(self):
    return self.window

  def getVbox(self):
    return self.vbox

  def getActiveManga(self):
    return self.activeManga

  def on_key_press_event(self, embed, event):
    keyName = gtk.gdk.keyval_name(event.keyval)
    if keyName == 'f':
      self.toggleFullscreen()
    elif keyName == 'o':
      self.notify('fit to <b>original size</b>')
      self.set('fitMode',"original")
    elif keyName == 'i':
      self.notify('fit to <b>width</b>')
      self.set('fitMode',"width")
    elif keyName == 'u':
      self.notify('fit to <b>height</b>')
      self.set('fitMode',"height")
    elif keyName == 'z':
      self.notify('fit to <b>screen</b>')
      self.set('fitMode', "screen")
    elif keyName == 'n':
      """launch file chooser"""
      self.platform.startChooser(gtk.FILE_CHOOSER_ACTION_OPEN)
    elif keyName == 'b':
      """launch folder chooser"""
      self.platform.startChooser(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
    elif keyName == 'k':
      """toggle kinetic scrolling"""
      kinetic = self.get('kineticScrolling', True)
      if kinetic:
        self.set('kineticScrolling', False)
        self.notify('kinetic scrolling <b>disabled</b>')
      else:
        self.set('kineticScrolling', True)
        self.notify('kinetic scrolling <b>enabled</b>')
    elif keyName == 'p':
      """show paging dialog"""
      self.platform.showPagingDialog()
    elif keyName == 'c':
      """show options window"""
      self.platform.showOptions()
    elif keyName == 'a':
      """show info window"""
      self.platform.showInfo()
    elif keyName == 'm':
      """minimize the main window"""
      self.platform.minimize()
    elif keyName == 'q':
      self.destroy(self.window)
    elif keyName == 'F8' or keyName == 'Page_Up':
      if self.activeManga:
        self.activeManga.previous()
    elif keyName == 'F7' or keyName == 'Page_Down':
      if self.activeManga:
        self.activeManga.next()
    elif not self.platform.handleKeyPress(embed, event):
      print "key: %s" % keyName

  def on_button_press_event(actor, event):
    print "button press event"

  def toggleFullscreen(self, widget=None):
    if self.fullscreen:
      self.window.unfullscreen()
      self.fullscreen = False
    else:
      self.window.fullscreen()
      self.fullscreen = True

  def notify(self, message, icon=""):
    print "notification: %s" % message
    self.platform.notify(message,icon)

  def openManga(self, path, startOnPage=0):
    if self.activeManga:
      print "closing previously open manga"
      self.activeManga.close()

    print "opening %s on page %d" % (path,startOnPage)
    self.activeManga = manga.Manga(self, path, startOnPage)
    mangaState = self.activeManga.getState()
    # increment count
    self.stats.incrementUnitCount()

    self.addToHistory(mangaState)
    self.saveState()

  def openMangaFromState(self, state):
    if self.activeManga:
      print "closing previously open manga"
      self.activeManga.close()

    print "opening manga from state"
    self.activeManga = manga.fromState(self, state)
    mangaState = self.activeManga.getState()
    self.addToHistory(mangaState)
    self.saveState()

  def getActiveMangaPath(self):
    if self.activeManga:
      return self.activeManga.getPath()

  def addToHistory(self,mangaState):
    """add a saved manga state to the history"""
    openMangasHistory = self.get('openMangasHistory',None)
    if openMangasHistory == None: # history has not yet taken place
      openMangasHistory = {}

    if mangaState['path'] != None:
      path = mangaState['path']
      print "adding to history: %s" % path
      openMangasHistory[path] = {"state":mangaState,"timestamp":time.time()}
      """the states are saved under their path to store only unique mangas,
         when the same manga is opened again, its state is replaced by the new one
         the timestamp is used for chrnological sorting of the list
      """
    # save the history back to the persistant store
    # TODO: limit the size of the history + clearing of history
    self.set('openMangasHistory', openMangasHistory)

  def addMangaToHistory(self, manga):
    """add a manga instance to history"""
    state = manga.getState()
    if state:
      self.addToHistory(state)

  def removeMangaFromHistory(self,path):
    """delete manga described by path from history"""
    openMangasHistory = self.get('openMangasHistory',None)
    if openMangasHistory:
      if path in openMangasHistory:
        del openMangasHistory[path]
    self.set('openMangasHistory', openMangasHistory)

  def getSortedHistory(self):
    openMangasHistory = self.get('openMangasHistory',None)
    if openMangasHistory:
      sortedList = []
      for path in sorted(openMangasHistory, key=lambda path: openMangasHistory[path]['timestamp'], reverse=True):
        sortedList.append(openMangasHistory[path])
      return sortedList
    else:
      return None

  def clearHistory(self):
    """clear the history of opened mangas"""
    self.set('openMangasHistory', {})


  def watch(self, key, callback, *args):
    """add a callback on an options key"""
    id = self.maxWatchId + 1 # TODO remove watch based on id
    self.maxWatchId = id # TODO: recycle ids ? (alla PID)
    if key not in self.watches:
      self.watches[key] = [] # create the initial list
    self.watches[key].append((id,callback,args))
    return id

  def _notifyWatcher(self, key, value):
    """run callbacks registered on an options key"""
    callbacks = self.watches.get(key, None)
    if callbacks:
      for item in callbacks:
        (id,callback,args) = item
        oldValue = self.get(key, None)
        if callback:
          callback(key,value,oldValue, *args)
        else:
          print "invalid watcher callback :", callback

  def get(self, key, default):
    return self.d.get(key, default)

  def set(self, key, value):
    self.d[key] = value
    self.options.save()
    if key in self.watches.keys():
      self._notifyWatcher(key, value)

  def saveState(self):
    print "saving state"
    if self.activeManga: # is some manga actually loaded ?
      state = self.activeManga.getState()
      self.addToHistory(state)

  def setWindowTitle(self, title):
    self.window.set_title(title)

  def _restoreState(self):
    openMangasHistory = self.getSortedHistory()
    if openMangasHistory:
      print "restoring last open manga"
      lastOpenMangaState = openMangasHistory[0]['state']
      self.openMangaFromState(lastOpenMangaState)
#      self.activeManga = manga.fromState(self, lastOpenMangaState)
    else:
      print "no history found"

  def _resizeViewport(self,widget,allocation):
    self.viewport = allocation

  def getFittingModes(self):
    """return list of fitting mode with key and description"""
    modes = [
            ("original", "fit to original size"),
            ("width", "fit to width"),
            ("height", "fit to height"),
            ("screen", "fit to screen")
            ]
    return modes


#  def do_button_press_event(actor, event):
#    print "button press event"
#
#  def on_button_press(actor,event):
#    print actor,event
#
#  def do_button_press_event(self,widget,event):
#    print widget, event

if __name__ == "__main__":
  mieru = Mieru()
