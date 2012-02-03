#!/usr/bin/env python
from __future__ import with_statement # for python 2.5
from gui import gui

import timer
import time
from threading import RLock

# Mieru modules import
startTs = timer.start()
import manga
import options
import startup
import stats
timer.elapsed(startTs, "All modules combined")

# set current directory to the directory
# of this file
# like this, Mieru can be run from absolute path
# eq.: ./opt/mieru/mieru.py -p harmattan -u harmattan
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


# append the platform modules folder to path
import sys
sys.path.append('platforms')

class Mieru:

  def destroy(self):
    # log elapsed time
    sessionTime = time.time() - self.startupTimeStamp
    self.stats.updateUsageTime(sessionTime)

    self.saveActiveMangaState()
    self.options.save()
    print "mieru quiting"
    self.gui.stopMainLoop()

  def __init__(self):
    # log start
    initTs = time.clock()
    self.startupTimeStamp = time.time()

    # parse startup arguments
    start = startup.Startup()
    args = start.args

    # restore the persistent options dictionary
    self.d = {}
    self.options = options.Options(self)
    # options value watching
    self.maxWatchId = 0
    self.watches = {}
    # history lock
    self.historyLock = RLock()

    # enable stats
    self.stats = stats.Stats(self)

    self.continuousReading = True

    initialSize = (800,480)


    # get the platform module
    self.platform = None

    if args.p:
      if args.p == "maemo5":
        import maemo5
        self.platform = maemo5.Maemo5(self, GTK=False)
      elif args.p == "harmattan":
        import harmattan
        self.platform = harmattan.Harmattan(self)
      else:
        import pc
        self.platform = pc.PC(self)

    else:
      # no platform provided, decide based on selected GUI
      if args.u == "hildon":
        import maemo5
        self.platform = maemo5.Maemo5(self)
      elif args.u == "harmattan":
        import harmattan
        self.platform = harmattan.Harmattan(self)
      else:
        import pc
        self.platform = pc.PC(self)


    # create the GUI
    startTs1 = timer.start()

    if args.u == "hildon":
      self.gui = gui.getGui(self, 'hildon', accel=True, size=initialSize)
    if args.u == "harmattan" or args.u=='QML':
      self.gui = gui.getGui(self, 'QML', accel=True, size=initialSize)
    else:
      self.gui = gui.getGui(self, 'GTK', accel=True, size=initialSize)

    timer.elapsed(startTs1, "GUI module import")

#    # resize the viewport when window size changes
#    self.gui.resizeNotify(self._resizeViewport)




    self.activeManga = None

    # check if a path was specified in the startup arguments
    if args.o != None:
      try:
        print("loading manga from: %s" % args.o)
        self.setActiveManga(self.openManga(args.o))
        print('manga loaded')
      except Exception, e:
        print("loading manga from path: %s failed" % args.o)
        print(e)

    """ restore previously saved state (if available and no manga was 
    sucessfully loaded from a path provided by startup arguments"""
    if self.activeManga == None:
      self._restoreState()

#    self.gui.toggleFullscreen()

    timer.elapsed(initTs, "Init")
    timer.elapsed(startTs, "Complete startup")

    # start the main loop
    self.gui.startMainLoop()

  def getDict(self):
    return self.d

  def setDict(self, d):
    self.d = d

  def getViewport(self):
    return self.viewport

  def getWindow(self):
    return self.window

  def getVbox(self):
    return self.vbox

  def keyPressed(self, keyName):
    if keyName == 'f':
      self.gui.toggleFullscreen()
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
      self.platform.startChooser("file")
    elif keyName == 'b':
      """launch folder chooser"""
      self.platform.startChooser("folder")
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
    elif not self.platform.handleKeyPress(keyName):
      print "key: %s" % keyName

  def on_button_press_event(actor, event):
    print "button press event"

  def notify(self, message, icon=""):
    print "notification: %s" % message
    self.platform.notify(message,icon)

  def openManga(self, path, startOnPage=0, replaceCurrent=True, loadNotify=True):
    if replaceCurrent:
      print "opening %s on page %d" % (path,startOnPage)
      mangaInstance = manga.Manga(self, path, startOnPage, loadNotify=loadNotify)
      # close and replace any current active manga
      self.setActiveManga(mangaInstance)

      # increment manga count
      self.stats.incrementUnitCount()

      # return the newly created manga instance
      return mangaInstance
    else:
      return manga.Manga(self, path, startOnPage, loadNotify=loadNotify)

  def openMangaFromState(self, state):
    print "opening manga from state"
    #print state
    mangaInstance = manga.Manga(self,load=False)
    mangaInstance.setState(state)
    if mangaInstance.container == None:
      print("container creation failed")
      return False
    else:
      # close and replace any current active manga
      self.setActiveManga(mangaInstance)
      return True

  def setActiveManga(self, mangaInstance):
    """set the given instance as the active manga
    eq. it has focus, receives page turn events, etc."""

    # is there an already active manga
    if self.activeManga:
      # add it to history
      self.addMangaToHistory(self.activeManga)
      # close it
      self.activeManga.close()
    # replace it with the new one
    self.activeManga = mangaInstance
    # notify the GUI there is a new active manga instance
    self.gui.newActiveManga(self.activeManga)

  def getActiveManga(self):
    return self.activeManga

  def getActiveMangaPath(self):
    if self.activeManga:
      return self.activeManga.getPath()
    else:
      print("mieru: can't return manga path - there is no active manga")
      return None

  def addToHistory(self,mangaState):
    """add a saved manga state to the history"""
    openMangasHistory = self.get('openMangasHistory',{})
    try:
      if mangaState['path'] != None:
        path = mangaState['path']
        print("adding to history: %s, on page %d" % (path, mangaState.get('pageNumber',0)))
        openMangasHistory[path] = {"state":mangaState,"timestamp":time.time()}
        """the states are saved under their path to store only unique mangas,
           when the same manga is opened again, its state is replaced by the new one
           the timestamp is used for chronological sorting of the list
        """
      # save the history back to the persistent store
      # TODO: limit the size of the history + clearing of history
    except Exception, e:
      print("saving manga to history failed with exception:\n", e)
      print("manga state was:", mangaState)
    self.set('openMangasHistory', openMangasHistory)
    self.options.save()

  def addMangaToHistory(self, manga):
    """add a manga instance to history"""
    state = manga.getState()
    if state:
      self.addToHistory(state)

  def removeMangasFromHistory(self, paths):
    """a function for batch removing mangas from history"""
    print("removing %d mangas from history" % len(paths))
    openMangasHistory = self.get('openMangasHistory',None)
    if openMangasHistory:
      for path in paths:
        if path in openMangasHistory:
          print "deleting %s" % path
          del openMangasHistory[path]
    self.set('openMangasHistory', openMangasHistory)
    print("removing done")

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
      return []

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
    """
    get a value from the persistent dictionary
    """
    try:
      return self.d.get(key, default)
    except Exception, e:
      print "options: exception while working with persistent dictionary:\n%s" % e
      return default

  def set(self, key, value):
    """
    set a value in the persistent dictionary
    """
    self.d[key] = value
    self.options.save()
    if key in self.watches.keys():
      self._notifyWatcher(key, value)

  def saveActiveMangaState(self):
    print "saving active manga state state"
    if self.activeManga: # is some manga actually loaded ?
      state = self.activeManga.getState()
      self.addToHistory(state)

  def _restoreState(self):
    openMangasHistory = self.getSortedHistory()
    if openMangasHistory:
      print "restoring last open manga"
      lastOpenMangaState = openMangasHistory[0]['state']
      if self.openMangaFromState(lastOpenMangaState):
        print "last open manga restored"
      else:
        print "restoring last open manga failed"
    else:
      print "no history found"

  def _resizeViewport(self,allocation):
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

if __name__ == "__main__":
  mieru = Mieru()
