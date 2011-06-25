"""a Mieru class representing a single manga / comix file/folder
   - this is driven by the storage format - it can really be a single chapter,
   or a whole volume if all page images are in  a single file or folder
"""
import os
import cluttergtk
import clutter
import gtk
import gobject
import time

import manga as mangaModule
#import declutter
import page as pageModule
import container as containerModule


class Manga:
  def __init__(self, mieru, path=None, startOnPage=0, load=True, loadNotify=True):
    self.mieru = mieru
    stage = self.mieru.gui.getStage()
    # buttons FIXME
    stage.connect('allocation-changed', self._handleResize)
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
    self.previewBox = None
    self.previewBoxStartingPoint = (0,0)

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
    # cleanup
    if self.activePage:
      page = self.activePage
      self.activePage = None
      self._quicklyDestroyPage(page)
    if self.container:
      pass

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

      return True
#    # get page for the given id
#    oldPage = self.activePage
#    newPageQuery = self.getPageById(id)
#    if newPageQuery:
#      (newPage,newPageId) = newPageQuery
#      print "switching to page: ", id
#      self.addToStage(newPage)
#      # hide the old page
#      if oldPage:
#        oldPage.deactivate()
##        self.fadeOut.apply(oldPage)
#        self.fadeOut(oldPage)
#        self.pageTurnTl.connect('completed', self._removeAndDestroy, oldPage)
##        declutter.animate(oldPage, clutter.LINEAR, 300, [('opacity', 0)])
##        oldPage.hide()
#      # show the new page
#      newPage.activate()
##      newPage.set_opacity(0)
#      newPage.show()
##      self.fadeIn.apply(newPage)
#      self.fadeIn(newPage)
#      # remove the old page from stage
##      self.removeFromStage(oldPage)
#
##      if oldPage:
##        self._quicklyDestroyPage(oldPage)
#
#      # update the id
#      self.activePageId = newPageId
#      self.activePage = newPage
#      self.pageTurnTl.start()
#
#      # increment page count
#      self.mieru.stats.incrementPageCount()
#
#      return True
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

  def _updateTitleTextCB(self, timeline=None):
    """update the title text on the mieru window (and possibly elswhere)"""
    title = self._getTitleText()
    self.mieru.gui.setWindowTitle(title)

  def _getPBoxCoords(self, type):
    """compute coordinates for the preview box"""
    (x,y,w,h) = self.mieru.viewport
    pBoxSide = h/2.0
    border = pBoxSide/20.0
    pBoxInSide = pBoxSide-2*border

    pBoxY = x/2.0+pBoxSide/2.0
    pBoxX = w
    pBoxShownX = w - pBoxSide
    """ previous - box on the left, next - box on the right
    (corresponding to the volume buttons)"""
    if type == "previous":
      pBoxX = 0 - pBoxSide
      pBoxShownX = 0
    return (pBoxY,pBoxX,pBoxShownX,pBoxSide,pBoxInSide,border)

  def _showPreview(self, path, type):
    if not self.previewBox: # we show only one preview
      print "manga: showing preview"
      manga = mangaModule.Manga(self.mieru, path, load=True, loadNotify=False, startOnPage=None)
      if manga: # only continue if the next manga was successfully loaded
        previewId = 0
        (x,y,w,h) = self.mieru.viewport
#        pBoxSide = h/2.0
#        border = pBoxSide/20.0
#        pBoxInSide = pBoxSide-2*border
#
#        pBoxY = x/2.0+pBoxSide/2.0
#        pBoxX = w
#        pBoxShownX = w - pBoxSide
        """ previous - box on the left, next - box on the right
        (corresponding to the volume buttons)"""
        action = self.next
        if type == "previous":
          action = self.previous
          previewId = -1
#          pBoxX = 0 - pBoxSide
#          pBoxShownX = 0

        (pBoxY,pBoxX,pBoxShownX,pBoxSide,pBoxInSide,border) = self._getPBoxCoords(type)
        # get and scale to fit the next(prev page
        thumbnail = manga.getPageById(previewId, fitOnStart=False)[0]
        if thumbnail: # no need to do a preview if there is none
          # 50% transparent yellow TODO: take this from current OS theme ?
          backgroundColor = clutter.color_from_string("yellow")
          backgroundColor.alpha=128
          background = clutter.Rectangle(color=backgroundColor)
          background.set_size(pBoxSide,pBoxSide)
          background.set_reactive(True)
          background.connect('button-release-event',self._previewPressedCB, action)

          # resize and fit in the thumbnail
          thumbnail.set_keep_aspect_ratio(True)
          (tw,th) = thumbnail.get_size()
          wf = float(pBoxInSide)/tw
          hf = float(pBoxInSide)/th
          if tw >= th:
            thumbnail.set_size(tw*wf, th*wf)
          else:
            thumbnail.set_size(tw*hf, th*hf)
          (tw,th) = thumbnail.get_size()
          print (tw,th)
          thumbnail.move_by(border+(pBoxInSide-tw)/2.0,border+(pBoxInSide-th)/2.0)

          # create a container for the thumbnail and background
          box = clutter.Group()
          box.add(background)
          box.add(thumbnail)
          self.mieru.buttons.getLayer().add(box)
          box.show()
          box.set_position(pBoxX,pBoxY)
          self.previewBoxStartingPoint = (pBoxX,pBoxY)
          box.animate(clutter.LINEAR,300,"x", pBoxShownX)
          self.previewBox = box

  def _previewPressedCB(self, actor, event, action):
    """the preview box has been pressed,
    load next/previous manga - the action is a binding to the
    next/previous method

    we use the gobject idle_add mathod so that it does not block
    right after clicking the preview
    """
    gobject.idle_add(action)
    
  def _hidePreview(self):
    """hide a displayed preview"""
    if self.previewBox:
      (x,y) = self.previewBoxStartingPoint
      print "manga: hiding preview"
      animation = self.previewBox.animate(clutter.LINEAR,300,"x", x)
      animation.get_timeline().connect('completed', self._killPreviewCB, self.previewBox)
      

  def _killPreviewCB(self, timeline, actor):
    """hide and unrealize a given actor"""
    actor.hide()
    actor.unrealize()
    self.mieru.buttons.getLayer().remove(actor)
    self.previewBox = None

  
  def _disarm(self,type):
    """a next/previous button is armed when it loads next/previous manga after pressing
       calling this method disarms the button"""
    if self.previewBox:
      self._hidePreview()
    if type == "previous":
      self.previousArmed = False
    elif type == "next":
      self.nextArmed = False



  def _handleResize(self,widget,event,foo):
    """handle resizing of the stage"""
    if self.previewBox:
      (x,y,w,h) = self.mieru.viewport
      pBoxSide = h/2.0
      newY = x/2.0+pBoxSide/2.0

      self.previewBox.animate(clutter.LINEAR,100,"y", newY, "width",pBoxSide, "height", pBoxSide)

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
