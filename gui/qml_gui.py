"""a QML GUI module for Mieru"""

import sys
import re
from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *

import gui
import qml_page


class QMLGUI(gui.GUI):
  def __init__(self, mieru, type, size=(854,480)):
    self.mieru = mieru

    self.activePage = None

    # Create Qt application and the QDeclarative view
    class ModifiedQDeclarativeView(QDeclarativeView):
      def __init__(self, gui):
        QDeclarativeView.__init__(self)
        self.gui = gui
        
      def closeEvent(self, event):
        print "shutting down"
        self.gui.mieru.destroy()

    self.app = QApplication(sys.argv)
    self.view = ModifiedQDeclarativeView(self)
    self.window = QMainWindow()
    self.window.resize(*size)
    self.window.setCentralWidget(self.view)
    self.view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
#    self.view.setResizeMode(QDeclarativeView.SizeViewToRootObject)
    #print self.view.connect("close")

    #self.view.resize(300,300)

    # add image providers
    self.pageProvider = MangaPageImageProvider(self)
    self.iconProvider = IconImageProvider()
    self.view.engine().addImageProvider("page",self.pageProvider)
    self.view.engine().addImageProvider("icons",self.iconProvider)
    # make the reading state accesible from QML
    readingState = ReadingState(self)
    self.view.rootContext().setContextProperty("readingState", readingState)

    # Create an URL to the QML file
    url = QUrl('gui/qml/main.qml')
    # Set the QML file and show
    self.view.setSource(url)
    self.window.closeEvent = self._qtWindowClosed
    self.window.show()

    self.rootObject = self.view.rootObject()
#    self.nextButton = self.rootObject.findChild(QObject, "nextButton")
#    self.prevButton = self.rootObject.findChild(QObject, "prevButton")
#    self.pageFlickable = self.rootObject.findChild(QObject, "pageFlickable")

    self.lastTimeRequestedOtherManga = None
#    self.nextButton.clicked.connect(self._nextCB)
#    self.pageFlickable.clicked.connect(self._prevCB)
#    self.prevButton.clicked.connect(self._prevCB)
    self.toggleFullscreen()

#    gui.GUI.__init__(self, mieru)
#    if type == "hildon":
#      import hildon
#      self.window = hildon.StackableWindow()
#    else:
#      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
#    self.resize(*size)
#
#    self.window.connect("destroy", self._destroyCB)
#
#    self.vbox = gtk.VBox(False, 2)
#    self.window.add(self.vbox)
#    self.fullscreen = False

#  def resize(self, w, h):
#    self.window.resize(w,h)
#
#  def getWindow(self):
#    return self.window
#
#  def setWindowTitle(self, title):
#    self.window.set_title(title)
#
  def getToolkit(self):
    return "QML"

  def toggleFullscreen(self):
    if self.window.isFullScreen():
      self.window.showNormal()
    else:
      self.window.showFullScreen()

  def startMainLoop(self):
    """start the main loop or its equivalent"""
    self.app.exec_()

  def _qtWindowClosed(self, event):
    print('qt window closing down')
    self.mieru.destroy()

  def stopMainLoop(self):
    """stop the main loop or its equivalent"""
    self.app.exit()

  def getPage(self, fileObject, mieru, fitOnStart=False):
    return qml_page.QMLPage(fileObject, self)
#    return fileObject

  def showPage(self, page, mangaInstance, id):
    """show a page on the stage"""

    """first get the file object containing
    the page image to a local variable so it can be loaded to a
    QML Image using QDeclarativeImageProvider"""

    print "SHOW PAGE"
    path = mangaInstance.getPath()
    
#    self.activePage = page
    self.rootObject.showPage(path, id)

  def _nextCB(self):
    print "turning page forward"
    self.mieru.activeManga.next()

  def _prevCB(self):
    print "turning page forward"
    self.mieru.activeManga.previous()

  def _getPageByPathId(self, mangaPath, id):
    """as QML automatically caches images by URL,
    using a url consisting from a filesystem path to the container and page id,
    we basically create a hash with very unlikely colisions (eq. same hash resulting in different images
    and thus can avoid doing caching on our side

    NOTE: some images might get cached twice
    example: lets have a 10 page manga, in /tmp/manga.zip
    URLs "/tmp/manga.zip|9" and "/tmp/manga.zip|-1" are the same image
    but the URLs are the same and QML would probably cache the image twice
    """
    if self.mieru.activeManga and self.mieru.activeManga.getPath() == mangaPath:
      return self.mieru.activeManga.getPageById(id)

    elif self.lastTimeRequestedOtherManga and self.lastTimeRequestedOtherManga.getPath() == mangaPath:
      return self.lastTimeRequestedOtherManga.getPageById(id)

    else:
      manga = self.mieru.openManga(mangaPath, replaceCurrent=False)
      self.lastTimeRequestedOtherManga = manga
      return manga.getPageById(id)


  def _notify(self, text, icon=""):
    """trigger a notification using the Qt Quick Components
    InfoBanner notification"""

    # QML uses <br> instead of \n for linebreak
    text = re.sub('\n', '<br>', text)
    self.rootObject.notify(text)

    #self.lastTimeRequestedOtherManga


#  def _addToCache(self, page, id):
#
#  def idleAdd(self, callback, *args):
#    gobject.idle_add(callback, *args)
#
#  def _destroyCB(self, window):
#    self.mieru.destroy()
#
#  def _flo2pixbuf(self, flo):
#    pl = gtk.gdk.PixbufLoader()
#    try:
#      pl.write(flo.read())
#      pl.close() # this  blocks until the image is completely loaded
#    except Exception,e:
#      print "gtkgui: Loading page failed with this exception:\n%s\ngtkgui: loading placeholder image" % e
#      # load a "page unredable image"  (@_@)
#      file = open("icons/page_unreadable.png", 'r')
#      # create a fresh pl
#      pl = gtk.gdk.PixbufLoader()
#      pl.write(file.read())
#      pl.close()
#      file.close()
#    pb = pl.get_pixbuf()
#    # cleanup
#    del pl
#    flo.close()
#    return pb

class MangaPageImageProvider(QDeclarativeImageProvider):
  """the MangaPageImageProvider class provides manga pages to the QML layer"""
  def __init__(self, gui):
      QDeclarativeImageProvider.__init__(self, QDeclarativeImageProvider.ImageType.Image)
      self.gui = gui

  def requestImage(self, pathId, size, requestedSize):
    (path,id) = pathId.split('|',1)
    print path, id
    id = int(id) # string -> integer
    #print(path, id)
    (page, id) = self.gui._getPageByPathId(path, id)
    imageFileObject = page.popImage()
    img=QImage()
    img.loadFromData(imageFileObject.read())
    return img

#    if self.gui.activePage:
#        print self.gui.activePage
#        imageFileObject = self.gui.activePage.popImage()
#        img=QImage()
#        img.loadFromData(imageFileObject.read())
#        return img
#    else:
#      if self.gui.activePage:
#        print("imProvider: unknown id: ", id)
#      else:
#        print("imProvider: no active page")
#      return None

class IconImageProvider(QDeclarativeImageProvider):
  """the IconImageProvider class provides icon images to the QML layer as
  QML does not seem to handle .. in the url very well"""
  def __init__(self):
      QDeclarativeImageProvider.__init__(self, QDeclarativeImageProvider.ImageType.Image)

  def requestImage(self, iconFilename, size, requestedSize):
    #print "!!!!!! icon image requested"
    try:
      f = open('icons/%s' % iconFilename,'r')
      img=QImage()
      img.loadFromData(f.read())
      f.close()
      return img
      #return img.scaled(requestedSize)
    except Exception, e:
      print("loading icon failed", e)

class ReadingState(QObject):
    def __init__(self, gui):
      QObject.__init__(self)
      self.gui = gui

    @QtCore.Slot(result=str)
    def next(self):
      activeManga = self.gui.mieru.getActiveManga()
      if activeManga:
        path = activeManga.getPath()
        idValid, id = activeManga.next()
        if idValid:
          return "image://page/%s|%d" % (path, id)
        else:
          return "ERROR do something else"
      else:
        return "ERROR no active manga"


    @QtCore.Slot(result=str)
    def previous(self):
      activeManga = self.gui.mieru.getActiveManga()
      if activeManga:
        path = activeManga.getPath()
        idValid, id = activeManga.previous()
        if idValid:
          return "image://page/%s|%d" % (path, id)
        else:
          return "ERROR do something else"
      else:
        return "ERROR no active manga"

    @QtCore.Slot(result=str)
    def getNextMangaPath(self):
        print ""

    @QtCore.Slot(result=str)
    def getPreviousMangaPath(self):
        print ""

    @QtCore.Slot(result=str)
    def toggleFullscreen(self):
      self.gui.toggleFullscreen()






#        width = 100
#        height = 50
#
#        if size:
#            size.setWidth(width)
#            size.setHeight(height)
#
#        if requestedSize.width() > 0:
#            width = requestedSize.width()
#        if requestedSize.height() > 0:
#            height = requestedSize.height()
#
#        pixmap = QPixmap(width, height)
#        pixmap.fill(QColor(id).rgba())
#
#        return pixmap
