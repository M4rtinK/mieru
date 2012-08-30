# -*- coding: utf-8 -*-
"""a Mieru class representing a single manga / comic book file/folder
   - this is driven by the storage format - it can really be a single chapter,
   or a whole volume if all page images are in  a single file or folder
"""
import os
import time
import re

#import manga as mangaModule
import container as containerModule
import page_cache


def name2PrettyName(name, path=None):
  """convert a manga name, eq. taken from its filename
  to a nicer looking string
  * replace _ with whitespace
  * remove file extensions"""
  # TODO: if path is provided check it the target is file or folder
  # and use this information accordingly
  name, extension = os.path.splitext(name)
  # remove text in square braces
  p = re.compile('(\s)*\[(\w)*\]', re.DOTALL)
  name = p.sub('', name)
  # replace _ with whitespace
  name = re.sub('_', ' ', name)
  # assure there is a space before numbers
  name = re.sub(r"([a-zA-Z])([0-9])", r"\1 \2", name)

  return name

def path2prettyName(path):
  (path,name) = os.path.split(path)
  return name2PrettyName(name)

class Manga:
  def __init__(self, mieru, path=None, startOnPage=0, load=True, loadNotify=True, pageShownNotify=False):
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
    self.loadNotify = loadNotify
    self.scale = 1.0
    self.shiftX = 0.0
    self.shiftY = 0.0

    """in case we get a manga instance just to grag some pages,
    we don't want it to connect the page shown notify callback"""
    if pageShownNotify:
      # connect the page turn complete callback
      self.mieru.gui.pageShownNotify(self._pageShownCB)

    # get page cache object
    self.cache = page_cache.PageCache(3)
    self.cacheUpdate = None

    if path and load:
      self.name = self._nameFromPath(path)
      """
      NOTE: for some reason, when not using this variable but just
      if self.load(path,startOnPage):
      the following code gets executed 2-4 times
      """
      if self.load(path,startOnPage):
        if loadNotify:
          self.mieru.notify('<b>%s</b> loaded on page <b>%d</b>' % (self.getPrettyName(), self.ID2PageNumber(startOnPage)))
        #print('<b>%s</b> loaded on page <b>%d</b>' % (self.name, self.ID2PageNumber(startOnPage)))
      else:
        if loadNotify:
          self.mieru.notify('<b>%s</b> loading failed' % self.getPrettyName())

  def getName(self):
    return self.name

  def setName(self, name):
    self.name = name

  def getPath(self):
    return self.path

  def getScale(self):
    return self.scale

  def getShiftX(self):
    return self.shiftX
  
  def getShiftY(self):
    return self.shiftY

  def getState(self):
    """save current state to a dictionary"""

    state = {'path': self.path, 'pageNumber': self.activePageId, 'pageCount': len(self.pages)}
    scale = self.mieru.gui.getScale()
    if scale is not None:
      state['scale'] = scale
    upperLeftShift = self.mieru.gui.getUpperLeftShift()
    if upperLeftShift is not None:
      state['upperLeftShift'] = upperLeftShift
    return state

  def setState(self, state):
    """restore from the state dictionary"""
    pageNumber = state.get('pageNumber',0)
    if pageNumber is None:
      pageNumber = 0
    self.scale = state.get('scale',1.0)

    (self.shiftX, self.shiftY) = state.get('upperLeftShift',(0.0,0.0))

    path = state.get('path',None)
    if path:
      self.name = self._nameFromPath(path)
      if self.load(path, pageNumber):
        self.mieru.notify('<b>%s</b> restored to page <b>%d</b>' % (self.getPrettyName(), self.ID2PageNumber(self.activePageId)))
      else:
        self.mieru.notify('<b>%s</b> restore failed' % self.getPrettyName())

  def load(self, path, pageNumber=0):
    """try to load manga from the given path"""
    print("manga: loading from path: %s" % path)
    self.path = path

    start = time.clock()
    container = containerModule.from_path(path)
    duration = (1000 * (time.clock() - start))
    if container: # was a container created successfully ?
      print("container created in %1.2f ms" % duration)
      self.container = container
      self.pages = self.container.getImageFileList()
      if pageNumber is None: # None means we don't show a page yet
        return True # nothing to go wrong here :)
      else:
        status = self.gotoPageId(pageNumber) # return if the first-selected page loaded successfully
        return status
    else:
      print("manga: container initialization failed")
      return False

  def close(self):
    # flush cache
    self.cache.flush()

    # remove any possible pending previews
    self.mieru.gui.hidePreview()

  def getContainer(self):
    return self.container

  def ID2PageNumber(self, id):
    """guess page number from id"""
    if id is None:
      return -1
    if id >= 0:
      return id + 1
    else: # negative addressing
      return len(self.pages) + id + 1

  def PageNumber2ID(self, pageNumber):
    """convert page number to id"""
    if pageNumber <= 0 or pageNumber > self.getMaxPageNumber():
      return None
    else:
      return pageNumber-1

  def idExists(self, id):
    if self.pages:
      if id < 0 or id > (len(self.pages)-1) or id is None: # None indicates initial active id state
        print("page id out of range:", id)
        return False
      else:
        return True

  def getPageById(self, id, fitOnStart=True):
    """return a Page instance together with its id in a tuple"""
    t1 = time.clock()
    result = self.container.getImageFileById(id)
    t2 = time.clock()
    if result:
      # correct id is returned for negative addressing (id=-1, etc.)
      (file,id) = result 
      page = self.mieru.gui.getPage(file, self.mieru, fitOnStart=fitOnStart)
      t3 = time.clock()
      # TODO: reimplement this
      if self.mieru.get('debugPageLoading', False):
        (w,h) = page.getSize()
        now = time.clock()
        print("Page completely loaded in %1.2f ms" % (1000 * (now - t1)))
        print("* loading from container: %1.2f ms" % (1000 * (t2 - t1)))
        print("* loading to pixbuf & to page & cleanup: %1.2f ms" % (1000 * (t3 - t2)))
#        print("* initializing page object with pixbuf: %1.2f ms" % (1000 * (t4 - t3)))
#        print("* closing file and deleting pixbuf: %1.2f ms" % (1000 * (t5 - t4)))
        print("- image resolution: %d x %d" % (w, h))
        print("- image filename: %s" % self.container.getImageFilenameById(id))

      return page, id
    else:
      print("manga: page not found, id: ", id)
      return None

  def getActivePageId(self):
    return self.activePageId

  def setActivePageId(self, id):
    """set active page id to a given value"""
    #TODO: support negative indexing
    if 0 <= id <= self.getMaxId():
      self.activePageId = id

  def getActivePageNumber(self):
    """get the id of the currently active page"""
    return self.ID2PageNumber(self.getActivePageId())

  def getMaxId(self):
    if self.pages:
      return len(self.pages)-1
    else:
      return None

  def getMaxPageNumber(self):
    maxId = self.getMaxId()
    if maxId is None:
      return 0
    else:
      return self.ID2PageNumber(maxId)

  def gotoPageId(self, id, direction=1):
    """go to the the page with the given id"""

    if id < 0: # -1 = last page, etc.
      currentId = ( self.getMaxId() - id - 1 )
    else:
      currentId = id

    print("###################")
    print("switching to page id: %d rel id: %d" % (currentId, id))
    print("###################")

    self.activePageId = currentId

    # get page for the given id
    newPage = None
    cacheThisPage = False
    # check if the page is already cached
    page = self.cache.get(currentId, None) # try to load from cache
    if page: # page was in cache
      newPage = page
      print("# page from cache")
    else: # not in cache, load from storage
      newPageQuery = self.getPageById(currentId)
      print("# page from storage")
      if newPageQuery:
        (newPage,newPageId) = newPageQuery
        cacheThisPage = True
      
    if newPage:
      # cache next/previous pages + this page (if needed)
      if cacheThisPage:
        self.cacheUpdate = (id, newPage, direction)
      else:
        self.cacheUpdate = (id, None, direction)

      # show the page
      newPage.activate()
      newPage.show()
      self.mieru.gui.showPage(newPage, self, currentId)
      
      # increment page count
      self.mieru.stats.incrementPageCount()

      # success
      return True
    else:
      print("switching to page failed, id: ", currentId)
      # enable to skip invalid pages that have valid id
      return False

  def next(self):
    """go one page forward"""
    self._disarm("previous")
    if self.nextArmed: # should we load next manga in folder after this press ?
      (isTrue, path) = self.nextArmed # get the path
      self._hidePreview()
      self.mieru.openManga(path, 0) # open it on first page
      return False, "loadingNext" # done

    currentId = self.activePageId
    if currentId is None:
      return False,"Error"
    nextId = currentId + 1
    # sanity check the id
    if nextId < len(self.pages):
      self.gotoPageId(nextId, +1)
      return True, nextId
    else:
      print("manga: end reached")
      if self.mieru.continuousReading:
        nextMangaPath = self.getNextMangaPath()
        if nextMangaPath:
          (folder, tail) = os.path.split(nextMangaPath)
          name = name2PrettyName(tail)
          self.mieru.notify('this is the <b>last</b> page,\n<u>press again</u> to load:\n<b>%s</b>' % name)
          self.nextArmed = (True, nextMangaPath)
          #self._showPreview(nextMangaPath, "next")
          return False, "press4Next"
        else:
          self.mieru.notify('this is the <b>last</b> page,\n there is no <i>previous</i> to load')
          return False, "noNext"
      else:
        self.mieru.notify('this is the <b>last</b> page')
        return False, "thisIsLastPage"

  def previous(self):
    """go one page back"""
    self._disarm("next")
    if self.previousArmed: # should we load next manga in folder after this press ?
      (isTrue, path) = self.previousArmed # get the path
      self._hidePreview()
      self.mieru.openManga(path, -1) # open it on last page
      return False, "loadingPrev" # done
    currentId = self.activePageId
    if currentId is None:
      return False,"Error"
    prevId = currentId - 1
    # sanity check the id
    if prevId >= 0:
      self.gotoPageId(prevId, -1)
      return True,prevId
    else:
      print("manga: start reached") # TODO: display a notification & go to next archive/folder (?)
      if self.mieru.continuousReading:
        previousMangaPath = self.getPrevMangaPath()
        if previousMangaPath:
          # get a preview
          (folder, tail) = os.path.split(previousMangaPath)
          name = name2PrettyName(tail)
          self.mieru.notify('this is the <b>first</b> page,\n <u>press again</u> to load:\n<b>%s</b>' % name)
          self.previousArmed = (True, previousMangaPath)

          #self._showPreview(previousMangaPath, "previous")
          return False, "press4Prev"
        else:
          self.mieru.notify('this is the <b>first</b> page,\n there is no <i>previous</i> to load')
          return False, "noPrev"
      else:
        self.mieru.notify('this is the <b>first</b> page')
        return False, "thisIsFirstPage"

  def getPrettyName(self):
    """get a pretty name of this manga instance"""
    return name2PrettyName(self.name)

  def onFitModeChanged(self, key, value, oldValue):
    # notify all pages that the fit mode has changed
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
    return prevPath, nextPath

  def getPrevMangaPath(self):
    (prevPath,nextPath) = self.getNeighborPaths()
    if prevPath:
      containerModule.testPath(prevPath)
      return prevPath
    else:
      print("manga: previous path uses unsupported format:\n%s" % prevPath)
      return False
    return prevPath
        
  def getNextMangaPath(self):
    (prevPath,nextPath) = self.getNeighborPaths()
    if nextPath:
      containerModule.testPath(nextPath)
      return nextPath
    else:
      print("manga: next path uses unsupported format:\n%s" % nextPath)
      return False
    return nextPath

  def getPreviousMangaStartID(self):
    return -1

  def getNextMangaStartID(self):
    return 0

  def _nameFromPath(self,path):
    (tail,name) = os.path.split(path)
    return name

  def _getTitleText(self):
    """return a string suitable for window header"""
    name = self.getName()
    pageNumber = self.getActivePageNumber()
    maxPages = self.getMaxPageNumber()
    return "%d/%d %s" % (pageNumber, maxPages, name)

  def _pageShownCB(self):
    self._updateTitleText()
    if self.cacheUpdate:
      (id, page, direction) = self.cacheUpdate
      self.mieru.gui.idleAdd(self._cacheAround, id, page, direction)

      self.cacheUpdate = None

#    self.mieru.gui.statusReport()

  def _updateTitleText(self):
    """update the title text on the mieru window (and possibly elsewhere)"""
    title = self._getTitleText()
    self.mieru.gui.setWindowTitle(title)

  def _showPreview(self, path, type):
    pass

#  def _showPreview(self, path, type):
#    # decide page number and direction
#    if type == "previous":
#      pageId = -1
#      direction = type
#      onPressAction = self.previous
#    else: # type == "next"
#      pageId = 0
#      direction = type
#      onPressAction = self.next
#
#    # get the page
#    manga = mangaModule.Manga(self.mieru, path, load=True, loadNotify=False, startOnPage=None, pageShownNotify=False)
#    if manga: # only continue if the next manga was successfully loaded
#      query = manga.getPageById(pageId, fitOnStart=False)
#      if query:
#        (page, id) = query
#        self.mieru.gui.showPreview(page, direction, onPressAction)

  def _hidePreview(self):
    self.mieru.gui.hidePreview()

  def _disarm(self,type):
    """a next/previous button is armed when it loads next/previous manga after pressing
       calling this method disarms the button"""
       
    # hide any previews
    self._hidePreview()

    if type == "previous":
      self.previousArmed = False
    elif type == "next":
      self.nextArmed = False

  def _cacheAround(self, id, page, direction):
    """cache pages around the current one"""
    if id < 0: # -1 = last page, etc.
      id = (self.getMaxId() - id + 1)

    # get possible previous and nex page ids
    pId = id - 1
    nId = id + 1

    # cache previous (if available)
    if pId >= 0:
      self._cachePageById(pId, direction)
      
    # cache current (if needed)
    if page:
      self._cachePage(page, id, direction)

    # cache next (if available)
    if nId <= self.getMaxId():
      self._cachePageById(nId, direction)

    self.cache.statusReport()

  def _cachePageById(self, id, direction):
    """check if the page already contains page with similar id,
    if it doesnt add the page to cache"""
    if not self.cache.has(id):
      query = self.getPageById(id, fitOnStart=False)
      if query:
        (page, id) = query
        self._cachePage(page, id, direction)

  def _cachePage(self, page, id, direction):
    """add a page to cache under an id"""
    self.cache.add(page, id, direction)


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
#    print(tw,th)
#    thumbnail.move_by(border+(pBoxInSide-tw)/2.0,border+(pBoxInSide-th)/2.0)




# possible eye candy manga to manga transition

    # show a yellow background behind it

    # hide both the preview and background

    # hide the background of the new page preview

    # maximize the new page

    # replace this manga instance by the new one
