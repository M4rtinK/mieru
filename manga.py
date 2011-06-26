"""a Mieru class representing a single manga / comix file/folder
   - this is driven by the storage format - it can really be a single chapter,
   or a whole volume if all page images are in  a single file or folder
"""
import os
import time

import manga as mangaModule
import container as containerModule


class Manga:
  def __init__(self, mieru, path=None, startOnPage=0, load=True, loadNotify=True):
    self.mieru = mieru
    self.fitMode = self.mieru.get('fitMode', 'original')
    self.mieru.watch('fitMode', self.onFitModeChanged)
    self.path = path
    self.name = ""
    self.pages = []
    self.container = None
    self.activePageId = None
    self.nextArmed = False
    self.previousArmed = False
    self.previewBox = None
    self.previewBoxStartingPoint = (0,0)

    # connect the page turn complete callback
    self.mieru.gui.pageShownNotify(self._updateTitleTextCB)

    if path and load:
      self.name = self._nameFromPath(path)
      if self.load(path,startOnPage):
        if loadNotify:
          self.mieru.notify('<b>%s</b> loaded on page <b>%d</b>' % (self.name, self.ID2PageNumber(startOnPage)))
        print '<b>%s</b> loaded on page <b>%d</b>' % (self.name, self.ID2PageNumber(startOnPage))
      else:
        if loadNotify:
          self.mieru.notify('<b>%s</b> loading failed' % self.name)
        print '<b>%s</b> loaded on page <b>%d</b>' % (self.name, self.ID2PageNumber(startOnPage))

  def getName(self):
    return self.name

  def setName(self, name):
    self.name = name

  def getPath(self):
    return self.path
  
  def getState(self):
    """save current satte to a dictionary"""

    state = {}
    state['path'] = self.path
    state['pageNumber'] = self.activePageId
    state['pageCount'] = len(self.pages) # for displaying in the history list
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
        self.mieru.notify('<b>%s</b> restored to page <b>%d</b>' % (self.name, self.ID2PageNumber(self.activePageId)))
      else:
        self.mieru.notify('<b>%s</b> restore failed' % self.name)

  def load(self, path, pageNumber=0):
    """try to load manga from the given path"""
    print "manga: loading from path: %s" % path
    self.path = path
    container = containerModule.from_path(path)
    if container: # was a container created successfully ?
      self.container = container
      self.pages = self.container.getImageFileList()
      if pageNumber == None: # None means we dont show a page yet
        return True # nothing to go wrong here :)
      else:
        return self.gotoPageId(pageNumber) # return if the first-selected page loaded successfully
    else:
      print "manga: container initialization failed"
      return False


  def close(self):
    # save current state to history
    self.mieru.addMangaToHistory(self)

  def ID2PageNumber(self, id):
    """guess page number from id"""
    if id == None:
      return -1
    if id >= 0:
      return id + 1
    else: # negative addressing
      return (len(self.pages) + id + 1)

  def idExistst(self, id):
    if self.pages:
      if id < 0 or id > (len(self.pages)-1) or id == None: # None idicates initial active id state
        print "page id out of range:", id
        return False
      else:
        return True

  def getPageById(self, id, fitOnStart=True):
    """return a Page instance together with its id in a tuple"""
    t1 = time.clock()
    result = self.container.getImageFileById(id)
    t2 = time.clock()
    if result:
      # correct id is reuturned for negative addressing (id=-1, etc.)
      (file,id) = result 
      page = self.mieru.gui.getPage(file,self.mieru, fitOnStart=fitOnStart)
      (w,h) = page.getSize()
      t3 = time.clock()
      # TODO: reimplement this
      if self.mieru.get('debugPageLoading', False):
        now = time.clock()
        print("Page completely loaded in %1.2f ms" % (1000 * (now - t1)))
        print("* loading from container: %1.2f ms" % (1000 * (t2 - t1)))
        print("* loading to pixbuf & to page & cleanup: %1.2f ms" % (1000 * (t3 - t2)))
#        print("* initializing page object with pixbuf: %1.2f ms" % (1000 * (t4 - t3)))
#        print("* closing file and deleting pixbuf: %1.2f ms" % (1000 * (t5 - t4)))
        print("- image resoution: %d x %d" % (w, h))
        print("- image filename: %s" % self.container.getImageFilenameById(id))

      return (page, id)
    else:
      print "manga: page not found, id: ", id
      return None

  def getActivePageId(self):
    return self.activePageId

  def getActivePageNumber(self):
    return self.ID2PageNumber(self.activePageId)

  def getMaxId(self):
    if self.pages:
      return (len(self.pages)-1)
    else:
      return None

  def getMaxPageNumber(self):
    maxId = self.getMaxId()
    if maxId == None:
      return 0
    else:
      return self.ID2PageNumber(maxId)

  def gotoPageId(self, id):
    # get page for the given id
    newPageQuery = self.getPageById(id)
    if newPageQuery:
      (newPage,newPageId) = newPageQuery
      print "switching to page: ", id
      newPage.activate()
      newPage.show()
      self.mieru.gui.showPage(newPage)

      # update the id
      self.activePageId = newPageId
      
      # increment page count
      self.mieru.stats.incrementPageCount()

      # success
      return True
    else:
      print "switching to page failed, id: ", id
      # enable to skip invalid pages that have valid id
      if id <= self.getMaxId() and id >= 0:
        self.activePageId = id
      return False

  def next(self):
    """go one page forward"""
    self._disarm("previous")
    if self.nextArmed: # should we load next manga in folder after this press ?
      (isTrue, path) = self.nextArmed # get the path
      self._hidePreview()
      self.mieru.openManga(path, 0) # open it on first page
      return # done

    currentId = self.activePageId
    if currentId == None:
      return
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
          self._showPreview(nextMangaPath, "next")
        else:
          self.mieru.notify('this is the <b>last</b> page,\n there is no <i>previous</i> to load')
      else:
        self.mieru.notify('this is the <b>last</b> page')

  def previous(self):
    """go one page back"""
    self._disarm("next")
    if self.previousArmed: # should we load next manga in folder after this press ?
      (isTrue, path) = self.previousArmed # get the path
      self._hidePreview()
      self.mieru.openManga(path, -1) # open it on last page
      return # done
    currentId = self.activePageId
    if currentId == None:
      return
    prevId = currentId - 1
    # sanity check the id
    if prevId >= 0:
      self.gotoPageId(prevId)
    else:
      print "manga: start reached" # TODO: display a notification & go to next archive/folder (?)
      if self.mieru.continuousReading:
        previousMangaPath = self.getPrevMangaPath()
        if previousMangaPath:
          # get a preview
          (folder, tail) = os.path.split(previousMangaPath)
          self.mieru.notify('this is the <b>first</b> page,\n <u>press again</u> to load:\n<b>%s</b>' % tail)
          self.previousArmed = (True, previousMangaPath)

          self._showPreview(previousMangaPath, "previous")
        else:
          self.mieru.notify('this is the <b>first</b> page,\n there is no <i>next</i> to load')
      else:
        self.mieru.notify('this is the <b>first</b> page')


  def onFitModeChanged(self, key, value, oldValue):
    # notifiy all pages that the fit mode has changed
    page = self.mieru.gui.getCurrentPage()
    if page:
      page.setFitMode(value)

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

  def getPrevisousMangaStartID(self):
    return -1

  def getNextMangaStartID(self):
    return 0

  def _nameFromPath(self,path):
    (tail,name) = os.path.split(path)
    return name

  def _getTitleText(self):
    """return a string suitable for window header"""
    name = self.getName()
    pageNumber = self.getActivePageId()+1
    maxPages = self.getMaxId()+1
    return "%d/%d %s" % (pageNumber, maxPages, name)

  def _updateTitleTextCB(self):
    """update the title text on the mieru window (and possibly elswhere)"""
    title = self._getTitleText()
    self.mieru.gui.setWindowTitle(title)

  def _showPreview(self, path, type):
    # decide page number and direction
    if type == "previous":
      pageId = -1
      direction = type
      onPressAction = self.previous
    else: # type == "next"
      pageId = 0
      direction = type
      onPressAction = self.next

    # get the page
    manga = mangaModule.Manga(self.mieru, path, load=True, loadNotify=False, startOnPage=None)
    if manga: # only continue if the next manga was successfully loaded
      query = manga.getPageById(pageId, fitOnStart=False)
      if query:
        (page, id) = query
        self.mieru.gui.showPreview(page, direction, onPressAction)

  def _hidePreview(self):
    self.mieru.gui.hidePreview()

    # show it in a preview

  def _disarm(self,type):
    """a next/previous button is armed when it loads next/previous manga after pressing
       calling this method disarms the button"""
       
    # hide any previews
    self._hidePreview()

    if type == "previous":
      self.previousArmed = False
    elif type == "next":
      self.nextArmed = False

#  def _transition(self, direction):
#    """replace the currently open manga with the previewed one"""
#
#    alpha = clutter.LINEAR
#    transition = clutter.Score()
#    minimizeTl = clutter.Timeline(duration=300)
#    maximizeTl = clutter.Timeline(duration=300)
#    bgInTl = clutter.Timeline(duration=300)
#    bgOutTl = clutter.Timeline(duration=300)
#
#    # transform currently visible page to a preview
#    self.activePage.deactivate()
#
#    (pBoxY,pBoxX,pBoxShownX,pBoxSide,pBoxInSide,border) = self._getPBoxCoords(type)
#
#    (tw,th) = self.activePage.get_size()
#    wf = float(pBoxInSide)/tw
#    hf = float(pBoxInSide)/th
#    if tw >= th:
#      self.activePage.animate_with_timeline(minimizeTl, alpha, "width", tw*wf, "height", th*wf)
#    else:
#      self.activePage.animate_with_timeline(minimizeTl, alpha, "width", tw*hf, "height", th*hf)

#    self.activePage.animate_with_timeline(minimizeTl, alpha, "x", ,"y", )


#    (tw,th) = thumbnail.get_size()
#    print (tw,th)
#    thumbnail.move_by(border+(pBoxInSide-tw)/2.0,border+(pBoxInSide-th)/2.0)





    # show a yellow background behind it

    # hide both the preview and background

    # hide the background of the new page preview

    # maximize the new page

    # replace this manga instance by the new one


def fromState(mieru, state):
  """create a Manga from the given state"""
  if mieru.gui.getAccel():
    m = Manga(mieru, load=False)
    m.setState(state)
    return m
