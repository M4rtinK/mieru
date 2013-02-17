#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement # for python 2.5
from pprint import pprint
import shutil
import traceback
import os
import sys
import gs

import bbpy

import timer
import time
from threading import RLock

# Mieru modules import
startTs = timer.start()
import manga
import options
import startup
import stats

LOG_FOLDER = '/accounts/1000/shared/downloads'
fSock = open(os.path.join(LOG_FOLDER, 'mieru_log.txt'), 'w', 1)
rfSock = open(os.path.join(LOG_FOLDER, 'mieru_error_log.txt'), 'w', 1)

sys.stdout = fSock
sys.stderr = rfSock

try:
  userHomePath = os.path.join(os.getenv("HOME", ""),".mieru/mieru_options.bin")
  shutil.copy(userHomePath, LOG_FOLDER)
except Exception as e:
  print("COPY EXCEPTION")
  print(e)

timer.elapsed(startTs, "All modules combined")

# set current directory to the directory
# of this file
# like this, Mieru can be run from absolute path
# eq.: ./opt/mieru/mieru.py -p harmattan -u harmattan
import os

originalCWD = os.getcwd()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


# append the platform modules folder to path
import sys

sys.path.append('platforms')
sys.path.append('gui')


class Mieru:
  def destroy(self):
    # log elapsed time
    sessionTime = time.time() - self.startupTimeStamp
    self.stats.updateUsageTime(sessionTime)

    self.saveActiveMangaState()
    self.options.save()
    print("Mieru quiting")
    self.gui.stopMainLoop()

  def __init__(self):
    # log start
    initTs = time.clock()
    self.startupTimeStamp = time.time()

    # parse startup arguments
    start = startup.Startup()
    args = start.args
    self.args = args
    self.originalCWD = originalCWD

    # restore the persistent options dictionary
    self.d = {}
    self.options = options.Options(self)
    # options value watching
    self.maxWatchId = 0
    self.watches = {}
    # history lock
    self.historyLock = RLock() # NOTE: not yet used

    # enable stats
    self.stats = stats.Stats(self)

    self.continuousReading = True

    # get the platform module
    self.platform = None

    # get the platform ID string
    platformId = "pc" # safe fallback

    # TODO: do this properly
    args.p = 'bb10'
    args.u = "harmattan"

    if args.p is None:
      import platform_detection
      # platform detection
      result = platform_detection.getBestPlatformModuleId()
      if result:
        platformId = result
    else: # use the CLI provided value
      platformId = args.p

    if platformId:
      if platformId == "maemo5":
        import maemo5

        if args.u == "hildon": # enable app menu with Hildon gui
          self.platform = maemo5.Maemo5(self, GTK=True)
        else:
          self.platform = maemo5.Maemo5(self, GTK=False)
      elif platformId == "harmattan":
        import harmattan

        self.platform = harmattan.Harmattan(self)
      elif platformId == "bb10":
        import bb10

        self.platform = bb10.BB10(self)
      else:
        import pc

        self.platform = pc.PC(self)

    else:
      # no platform provided, decide based on selected GUI
      if args.u == "hildon":
        import maemo5

        self.platform = maemo5.Maemo5(self, GTK=True)
      elif args.u == "harmattan":
        import harmattan

        self.platform = harmattan.Harmattan(self)
      else:
        import pc

        self.platform = pc.PC(self)


    # create the GUI
    startTs1 = timer.start()

    # use CLI provided GUI module ID
    if args.u:
      self._loadGUIModule(args.u)
    else: # get GUI module id from the platform module
      ids = self.platform.getSupportedGUIModuleIds()
      if ids:
        guiModuleId = ids[0]
        print('preferred GUI ID from platform module: %s' % guiModuleId)
        self._loadGUIModule(guiModuleId)
      else:
        print("platform module error: list of supported GUI IDs is empty")

    timer.elapsed(startTs1, "GUI module import")

    #    # resize the viewport when window size changes
    #    self.gui.resizeNotify(self._resizeViewport)

    self.activeManga = None

    # check if a path was specified in the startup arguments
    if args.o is not None:
      try:
        print("loading manga from: %s" % args.o)
        self.setActiveManga(self.openManga(args.o, checkHistory=True))
        print('manga loaded')
      except Exception as e:
        print("loading manga from path: %s failed" % args.o)
        print(e)

    """ restore previously saved state (if available and no manga was
    sucessfully loaded from a path provided by startup arguments"""
    if self.activeManga is None:
      self._restoreState()

    timer.elapsed(initTs, "Init")
    timer.elapsed(startTs, "Complete startup")

    # start the main loop
    self.gui.startMainLoop()

  #    print("loaded modules")
  #    print(list(sys.modules.keys()))

  def _loadGUIModule(self, id):
    # report GUI string
    import gui

    initialSize = self.platform.getScreenWH()
    if id in ("QML", "harmattan"):
      import qml_gui

      self.gui = qml_gui.QMLGUI(self, type='QML', size=initialSize)
    #      self.gui = gui.getGui(self, 'QML', accel=True, size=initialSize)
    elif id == "hildon":
      self.gui = gui.getGui(self, 'hildon', accel=True, size=initialSize)
    elif id == "GTK":
      self.gui = gui.getGui(self, 'GTK', accel=True, size=initialSize)

    # notify the platform module
    self.platform.guiModuleLoaded()

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
      self.set('fitMode', "original")
    elif keyName == 'i':
      self.notify('fit to <b>width</b>')
      self.set('fitMode', "width")
    elif keyName == 'u':
      self.notify('fit to <b>height</b>')
      self.set('fitMode', "height")
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
      print("key: %s" % keyName)

  def on_button_press_event(actor, event):
    print("button press event")

  def notify(self, message, icon=""):
    print("notification: %s" % message.encode('utf-8'))
    self.platform.notify(message, icon)

  def openManga(self, path, startOnPage=0, replaceCurrent=True, loadNotify=True, checkHistory=True):
    if replaceCurrent:
      mangaState = None
      if checkHistory: # check for saved state for the path
        mangaState = self.getMangaStateFromHistory(path)
      if mangaState:
        print('manga path found in history')
        self.openMangaFromState(mangaState)
      else:
        print("opening %s on page %d" % (path.encode('utf-8'), startOnPage))
        mangaInstance = manga.Manga(self, path, startOnPage, loadNotify=loadNotify)
        # close and replace any current active manga
        self.setActiveManga(mangaInstance)

        # increment manga count
        self.stats.incrementUnitCount()

        # return the newly created manga instance
        return mangaInstance
    else:
      try:
        return manga.Manga(self, path, startOnPage, loadNotify=loadNotify)
      except Exception as e:
        print('mieru: loading manga from path failed')
        #        print('path: ', path)
        print(e)
        traceback.print_exc(file=sys.stdout)
        return None

  def openMangaFromState(self, state):
    print("opening manga from state")
    mangaInstance = manga.Manga(self, load=False)
    mangaInstance.setState(state)
    if mangaInstance.container is None:
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

  def addToHistory(self, mangaState):
    """add a saved manga state to the history"""
    if self.get('historyEnabled', True):
      openMangasHistory = self.getHistory()
      status = None
      try:
        if mangaState['path'] is not None:
          path = mangaState['path']
          print("adding to history: %s, on page %d" % (path.encode('utf-8'), mangaState.get('pageNumber', 0)))
          openMangasHistory[path] = {"state": mangaState, "timestamp": time.time()}
          # the states are saved under their path to store only unique mangas,
          # when the same manga is opened again, its state is replaced by the new one
          # the timestamp is used for chronological sorting of the list

          # save the history back to the persistent store
          # TODO: limit the size of the history + clearing of history
          status = True
      except Exception as e:
        print("saving manga to history failed with exception:\n", e)
        print("manga state was:", mangaState.encode('utf-8'))
      self.set('openMangasHistory', openMangasHistory)
      self.options.save()
      return status
    else:
      print('history: not added -> history is disabled')
      return False

  def addMangaToHistory(self, manga):
    """add a manga instance to history"""
    state = manga.getState()
    if state:
      self.addToHistory(state)

  def getMangaStateFromHistory(self, path):
    history = self.getHistory()
    entry = history.get(path, None)
    if entry:
      return entry['state'] # manga path was stored in history
    else:
      return None # this manga path has no known history


  def removeMangasFromHistory(self, paths):
    """a function for batch removing mangas from history"""
    print("removing %d mangas from history" % len(paths))
    openMangasHistory = self.getHistory()
    if openMangasHistory:
      for path in paths:
        if path in openMangasHistory:
          print("deleting %s" % path)
          del openMangasHistory[path]
    self.set('openMangasHistory', openMangasHistory)
    print("removing done")

  def removeMangaFromHistory(self, path):
    """delete manga described by path from history"""
    openMangasHistory = self.getHistory()
    if openMangasHistory:
      if path in openMangasHistory:
        del openMangasHistory[path]
    self.set('openMangasHistory', openMangasHistory)

  def getHistory(self):
    """return history of open mangas, without sorting it"""
    history = self.get('openMangasHistory', {})
    # check if the data retrieved from history is really a list
    if isinstance(history, dict):
      return history
    else:
      return {}
      # looks like some other object type than a dict got stored in the history,
      # so we return an empty list (no dict -> no valid history -> empty history)

  def getSortedHistory(self):
    openMangasHistory = self.getHistory()
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
    self.watches[key].append((id, callback, args))
    return id

  def _notifyWatcher(self, key, value):
    """run callbacks registered on an options key"""
    callbacks = self.watches.get(key, None)
    if callbacks:
      for item in callbacks:
        (id, callback, args) = item
        oldValue = self.get(key, None)
        if callback:
          callback(key, value, oldValue, *args)
        else:
          print("invalid watcher callback :", callback)

  def get(self, key, default):
    """
    get a value from the persistent dictionary
    """
    try:
      return self.d.get(key, default)
    except Exception as e:
      print("options: exception while working with persistent dictionary:\n%s" % e)
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
    print("saving active manga state")
    if self.activeManga: # is some manga actually loaded ?
      state = self.activeManga.getState()
      if self.addToHistory(state):
        print('state saved')

  def _restoreState(self):
    openMangasHistory = self.getSortedHistory()
    if openMangasHistory:
      print("restoring last open manga")
      lastOpenMangaState = openMangasHistory[0]['state']
      if self.openMangaFromState(lastOpenMangaState):
        print("last open manga restored")
      else:
        print("restoring last open manga failed")
    else:
      print("no history found")

  def _resizeViewport(self, allocation):
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
  try:
    mieru = Mieru()
  except Exception:
    fp = open(os.path.join(LOG_FOLDER, 'mieru_exception_log.txt'), 'w', 1)
    traceback.print_exc(file=fp)
    fp.flush()
    fp.close()
    traceback.print_exc(file=fSock)
    fSock.flush()
  rfSock.flush()
  rfSock.close()
  fSock.flush()
  fSock.close()
  exit(0)
