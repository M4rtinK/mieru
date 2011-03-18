"""a Mieru class representing a single manga / comix file/folder
   - this is driven by the storage format - it can really be a single chapter,
   or a whole volume if all page images are in  a single file or folder
"""
import os
import gtk

import page as pageModule
import container


class Manga:
  def __init__(self, mieru, path=None, load=True, startOnPage=0):
    self.mieru = mieru
    self.stage = mieru.stage
    self.fitMode = mieru.fitMode
    self.path = path
    self.name = ""
    self.pages = []
    self.container = None
    self.pageCache = {}
    self.cacheSize = 5
    self.activePageId = None
    self.activePage = None
    if path and load:
      self.name = self._nameFromPath(path)
      if self.load(path,startOnPage):
        self.mieru.notify('<b>%s<b/> loaded' % self.name)
      else:
        self.mieru.notify('<b>%s<b/> loading failed' % self.name)





  def getName(self):
    return self.name

  def setName(self, name):
    self.name = name
    
  def getState(self):
    """save current satte to a dictionary"""

    state = {}
    state['path'] = self.path
    state['pageNumber'] = self.activePageId
    print state
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
    self.container = container.from_path(path)
    self.pages = self.container.getFileList()
    return self.gotoPageId(pageNumber) # return if the first-selected page loaded successfully


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
    if self.stage:
      self.stage.add(page)
    else:
      "manga: error, no stage"

  def removeFromStage(self, page):
    if self.stage and page:
      self.stage.remove(page)

  def idExistst(self, id):
    if self.pages:
      if id < 0 or id > (len(self.pages)-1) or id == None: # None idicates initial active id state
        print "page id out of range:", id
        return False
      else:
        return True

  def getPageById(self, id):
    file = self.container.getFileById(id)
    if file:
      # load the image from a pixbuf, created from the file object
      # we can like this easily unpack selected files from archives entirely in memmory
      pl = gtk.gdk.PixbufLoader()
      pl.write(file.read())
      pl.close() # this  blocks until the image is completely loaded
      # TODO: do this with callbacks
      return pageModule.Page(pl.get_pixbuf(),self.mieru)
    else:
      return None

  def getMaxId(self):
    if self.pages:
      return (len(self.pages)-1)
    else:
      return None
      
  def gotoPageId(self, id):
    # get page for the given id
    oldPage = self.activePage
    newPage = self.getPageById(id)
    if newPage:
      print "switching to page: ", id
      self.addToStage(newPage)
      # hide the old page
      if oldPage:
        oldPage.hide()
        oldPage.deactivate()
      # show the new page
      newPage.activate()
      newPage.show()
      # remove the old page from stage
      self.removeFromStage(oldPage)
      # update the id
      self.activePageId = id
      self.activePage = newPage
      return True
    else:
      print "switching to page failed, id: ", id
      return False

  def next(self):
    """go one page forward"""
    currentId = self.activePageId
    nextId = currentId + 1
    # sanity check the id
    if nextId < len(self.pages):
      self.gotoPageId(nextId)
    else:
      print "manga: end reached, no more pages"
      self.mieru.notify('this is the <b>last</b> page')

  def previous(self):
    """go one page back"""
    currentId = self.activePageId
    prevId = currentId - 1
    # sanity check the id
    if prevId >= 0:
      self.gotoPageId(prevId)
    else:
      print "manga: start reached, no more pages" # TODO: display a notification & go to next archive/folder (?)
      self.mieru.notify('this is the <b>first</b> page')


  def updateFitMode(self):
    # notifiy all pages that the fit mode has changed
    if self.activePage:
      self.activePage.fitModeChanged()

  def getNeighborPaths(self):
    (folderPath, tail) = os.path.split(path)
    folderContent = os.path.listdir(folderPath)
    folderContent.sort()
    maxId = len(folderContent)-1
    prevPath = None
    nextPath = None
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
    return prevPath
        
  def getNextMangaPath(self):
    (prevPath,nextPath) = self.getNeighborPaths()
    return nextPath

  def _nameFromPath(self,path):
    (tail,name) = os.path.split(path)
    return name





  




#
#  def showPageID(self, id):
#    if self.pages:
#      if id in self.pages:
#        page =
#      else:
#        print "page id out of range: %d" % id








