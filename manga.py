"""a Mieru class representing a single manga / comix file/folder
   - this is driven by the storage format - it can really be a single chapter,
   or a whole volume if all page images are in  a single file or folder
"""
import os
import gtk
import clutter

import declutter
import page as pageModule
import container as containerModule


class Manga:
  def __init__(self, mieru, path=None, startOnPage=0, load=True):
    self.mieru = mieru
    self.group = clutter.Group()
    mieru.stage.add(self.group)
    mieru.stage.lower_child(self.group,self.mieru.buttons.getLayer())
    self.fitMode = self.mieru.get('fitMode', 'original')
    self.mieru.watch('fitMode', self.onFitModeChanged)
    self.path = path
    self.name = ""
    self.pages = []
    self.container = None
    self.pageCache = {}
    self.cacheSize = 5
    self.activePageId = None
    self.activePage = None
    self.nextArmed = False
    self.previousArmed = False

    # animation
    self.pageTurnTl = clutter.Timeline(200)
#    self.pageTurnAlpha = clutter.Alpha(self.pageTurnTl, clutter.LINEAR)
#    self.pageTurnAlpha = clutter.Alpha(self.pageTurnTl, clutter.EASE_OUT_CUBIC)
#    self.pageTurnAlpha = clutter.Alpha(self.pageTurnTl, clutter.EASE_IN_CUBIC)
    self.pageTurnAlpha = clutter.Alpha(self.pageTurnTl, clutter.EASE_IN_CIRC)
#    self.fadeIn = clutter.BehaviourOpacity(0,255,self.pageTurnAlpha)
#    self.fadeOut = clutter.BehaviourOpacity(255,0,self.pageTurnAlpha)
#    self.fadeIn = clutter.BehaviourDepth(255,0,self.pageTurnAlpha)
#    self.fadeOut = clutter.BehaviourDepth(0,-255,self.pageTurnAlpha)
    self.fadeIn = self.fadeInOpac
    self.fadeOut = self.fadeOutOpac

    if path and load:
      self.name = self._nameFromPath(path)
      if self.load(path,startOnPage):
        self.mieru.notify('<b>%s</b> loaded' % self.name)
      else:
        self.mieru.notify('<b>%s</b> loading failed' % self.name)

  def fadeInOpac(self, page):
    self.a1 = clutter.BehaviourOpacity(0,255,self.pageTurnAlpha)
    self.a2 = clutter.BehaviourDepth(-255,0,self.pageTurnAlpha)
    self.a1.apply(page)
    self.a2.apply(page)
  def fadeOutOpac(self, page):
    self.b1 = clutter.BehaviourOpacity(255,0,self.pageTurnAlpha)
    self.b2 = clutter.BehaviourDepth(0,255,self.pageTurnAlpha)
    self.b1.apply(page)
    self.b2.apply(page)

  def getName(self):
    return self.name

  def setName(self, name):
    self.name = name
    
  def getState(self):
    """save current satte to a dictionary"""

    state = {}
    state['path'] = self.path
    state['pageNumber'] = self.activePageId
    return state

  def setState(self, state):
    """restore from the state dictionary"""
    pageNumber = state.get('pageNumber',0)
    if pageNumber == None:
      pageNumber = 0
    path = state.get('path',None)
    if path:
      self.name = self._nameFromPath(path)
      if self.load(path, pageNumber):
        self.mieru.notify('<b>%s</b> restored to page %d' % (self.name, pageNumber+1))
      else:
        self.mieru.notify('<b>%s</b> restore failed' % self.name)

  def load(self, path, pageNumber=0):
    """try to load manga from the given path"""
    print "manga: loading from path: %s" % path
    self.path = path
    container = containerModule.from_path(path)
    if container: # was a container created successfully ?
      self.container = container
      self.pages = self.container.getFileList()
      return self.gotoPageId(pageNumber) # return if the first-selected page loaded successfully

  def close(self):
    if self.activePage:
      page = self.activePage
      self.activePage = None
      self._quicklyDestroyPage(page)
    if self.container:
      pass

  def _removeAndDestroy(self, timeline, page):
    self.removeFromStage(page)
    self._quicklyDestroyPage(page)


  def _quicklyDestroyPage(self,page):
    """quickly free resources held by a page"""
    if page:
      # kill it with fire
      page.unrealize()
      page.destroy()
      del page


#  def loadFolder(self, path):
#    if of.path.isdir:
#      sortedDirContent = sorted(os.listdir(path))
#      pages = self.loadPages(path, sortedDirContent)
#      if pages:
#        self.pages = pages
#
#        self.gotoPageId(pageNumber)
#      else:
#        print "manga: no usable pages found"
#    else:
#      print "error, path is not a directory"

#  def loadPages(self, folderPath, files):
#    loadedPages = []
#    if files:
#      for file in files:
#        path = os.path.join(folderPath,file)
#        if os.path.exists(path) and os.path.isfile(path):
#          mime = self.getFileMime(path)
#          mimeSplit = mime.split('/')
#          type = mimeSplit[0]
#          if type == 'image':
#            newPage = pageModule.Page(path,self.mieru)
#            if newPage:
#              loadedPages.append(newPage)
#              print "%s loaded" % file
#          else:
#            print "not an image - not loading"
#            print "mime: %s" % mime
#            print "path: %s" % file
#    print "manga: loaded %d pages" % len(loadedPages)
#    return(loadedPages)

  def addToStage(self, page):
    if self.group:
      self.group.add(page)
    else:
      "manga: error, no stage"

  def removeFromStage(self, page):
    if self.group and page:
      self.group.remove(page)

  def idExistst(self, id):
    if self.pages:
      if id < 0 or id > (len(self.pages)-1) or id == None: # None idicates initial active id state
        print "page id out of range:", id
        return False
      else:
        return True

  def getPageById(self, id):
    """return a Page instance together with its id in  a tuple"""
    result = self.container.getImageFileById(id)
    if result:
      (file,id) = self.container.getImageFileById(id) # return correct id of negative addressing (id=-1, etc.)
      # load the image from a pixbuf, created from the file object
      # we can like this easily unpack selected files from archives entirely in memmory
      pl = gtk.gdk.PixbufLoader()
      pl.write(file.read())
      file.close()
      pl.close() # this  blocks until the image is completely loaded
      # TODO: do this with callbacks
      page = pageModule.Page(pl.get_pixbuf(),self.mieru)
      del pl
      return (page, id)
    else:
      print "manga: page not found, id:" % id
      return None

  def getMaxId(self):
    if self.pages:
      return (len(self.pages)-1)
    else:
      return None
      
  def gotoPageId(self, id):
    # get page for the given id
    oldPage = self.activePage
    newPageQuery = self.getPageById(id)
    if newPageQuery:
      (newPage,newPageId) = newPageQuery
      print "switching to page: ", id
      self.addToStage(newPage)
      # hide the old page
      if oldPage:
        oldPage.deactivate()
#        self.fadeOut.apply(oldPage)
        self.fadeOut(oldPage)
        self.pageTurnTl.connect('completed', self._removeAndDestroy, oldPage)
#        declutter.animate(oldPage, clutter.LINEAR, 300, [('opacity', 0)])
#        oldPage.hide()
      # show the new page
      newPage.activate()
#      newPage.set_opacity(0)
      newPage.show()
#      self.fadeIn.apply(newPage)
      self.fadeIn(newPage)
      # remove the old page from stage
#      self.removeFromStage(oldPage)

#      if oldPage:
#        self._quicklyDestroyPage(oldPage)

      # update the id
      self.activePageId = newPageId
      self.activePage = newPage
      self.pageTurnTl.start()
      return True
    else:
      print "switching to page failed, id: ", id
      return False

  def next(self):
    """go one page forward"""
    self.previousArmed = False
    nextArmed = self.nextArmed
    if nextArmed: # should we load next manga in folder after this press ?
      (isTrue, path) = nextArmed # get the path
      self.mieru.openManga(path, 0) # open it on first page
      return # done

    currentId = self.activePageId
    nextId = currentId + 1
    # sanity check the id
    if nextId < len(self.pages):
      self.gotoPageId(nextId)
    else:
      print "manga: end reached"
      if self.mieru.continuousReading:
        nextMangaPath = self.getNextMangaPath()
        if nextMangaPath:
          (folder, tail) = os.path.split(nextMangaPath)
          self.mieru.notify('this is the <b>last</b> page,\n<u>press again</u> to load:\n<b>%s</b>' % tail)
          self.nextArmed = (True, nextMangaPath)
        else:
          self.mieru.notify('this is the <b>last</b> page,\n there is no <i>previous</i> to load')
      else:
        self.mieru.notify('this is the <b>last</b> page')

  def previous(self):
    """go one page back"""
    self.nextArmed = False
    previousArmed = self.previousArmed
    if previousArmed: # should we load next manga in folder after this press ?
      (isTrue, path) = previousArmed # get the path
      self.mieru.openManga(path, -1) # open it on last page
      return # done
    currentId = self.activePageId
    prevId = currentId - 1
    # sanity check the id
    if prevId >= 0:
      self.gotoPageId(prevId)
    else:
      print "manga: start reached" # TODO: display a notification & go to next archive/folder (?)
      if self.mieru.continuousReading:
        previousMangaPath = self.getPrevMangaPath()
        if previousMangaPath:
          (folder, tail) = os.path.split(previousMangaPath)
          self.mieru.notify('this is the <b>first</b> page,\n <u>press again</u> to load:\n<b>%s</b>' % tail)
          self.previousArmed = (True, previousMangaPath)
        else:
          self.mieru.notify('this is the <b>first</b> page,\n there is no <i>next</i> to load')
      else:
        self.mieru.notify('this is the <b>first</b> page')


  def onFitModeChanged(self, key, value, oldValue):
    # notifiy all pages that the fit mode has changed
    if self.activePage:
      self.activePage.setFitMode(value)

  def getNeighborPaths(self):
    prevPath = None
    nextPath = None
    path = self.path
    if path:
      (folderPath, tail) = os.path.split(path)
      folderContent = os.listdir(folderPath)
      folderContent.sort()
      maxId = len(folderContent)-1
      if tail in folderContent: # just to be sure
        id = folderContent.index(tail)
        prevId = id-1
        nextId = id+1
        if prevId >= 0:
          prevPath = os.path.join(folderPath,folderContent[prevId])
        if nextId <= maxId:
          nextPath = os.path.join(folderPath,folderContent[nextId])
    return (prevPath, nextPath)

  def getPrevMangaPath(self):
    (prevPath,nextPath) = self.getNeighborPaths()
    if prevPath:
      containerModule.testPath(prevPath)
      return prevPath
    else:
      print "manga: previous path uses unsupported format:\n%s" % prevPath
      return False
    return prevPath
        
  def getNextMangaPath(self):
    (prevPath,nextPath) = self.getNeighborPaths()
    if nextPath:
      containerModule.testPath(nextPath)
      return nextPath
    else:
      print "manga: next path uses unsupported format:\n%s" % nextPath
      return False
    return nextPath

  def _nameFromPath(self,path):
    (tail,name) = os.path.split(path)
    return name


def fromState(parent, state):
  """create a Manga from the given state"""
  m = Manga(parent, load=False)
  m.setState(state)
  return m


#
#  def showPageID(self, id):
#    if self.pages:
#      if id in self.pages:
#        page =
#      else:
#        print "page id out of range: %d" % id








