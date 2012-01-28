"""Mieru image files container abstraction"""

import zipfile26 as zipfile # use backported zipfile from PYthon 2.6
import os
import rarfile
# make sure the built-in python-magic is used
import white_magic as magic
import re
import time
import traceback
import sys

def getFilePathMime(path):
  mime = magic.Magic(mime=True)
  return mime.from_file(path.encode('utf-8'))

def getFileMime(file):
  mime = magic.from_buffer(file.read(1024), mime=True)
  file.close() # properly close the file
  return mime

def getBufferMime(path, buffer):
  return magic.from_buffer(buffer, mime=True)

def getFileDescription(path):
  return magic.from_file(path.encode('utf-8'))

def humanSort(l):
  """ Sort the given list in the way that humans expect.
  source:
  http://www.codinghorror.com/blog/2007/12/sorting-for-humans-natural-sort-order.html
  """
  convert = lambda text: int(text) if text.isdigit() else text
  alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
  l.sort( key=alphanum_key )
  return l

def from_path(path):
  # does the path exist ?
  if os.path.exists(path):
    testResult = testPath(path)
    if testResult:
      (type, path, mime, desc) = testResult
      if type == "folder":
        return FolderContainer(path)
      elif type == "zip":
        return ZipContainer(path)
      elif type == "rar":
        return RarContainer(path)
      else:
        print "manga: loading failed, unsupported storage formate"
        return False
  else:
    print "manga: loading failed, path does not exist or is inaccessible"
    return False

def testPath(path):
  print "testing path: %s" % path
  #is it file or folder ?
  if os.path.isfile(path):
    print "manga: path is a file"
    desc = getFileDescription(path)
    print "file type: %s" % desc
    mime = getFilePathMime(path)
    print "file mime: %s" % mime
    mimeSplit = mime.split('/')
    m1 = mimeSplit[0]
    m2 = mimeSplit[1]
    if m1 == 'image':
      print "image file selected,\ncontaining folder could be loaded as a manga"
      (folderPath, tail) = os.path.split(path)
      return ("folder", folderPath, desc, mime)
    elif mime == 'application/zip' or mime == 'application/x-zip' or zipfile.is_zipfile(path):
      print "file is probably a zip file"
      return ("zip", path, desc, mime)
    elif mime == 'application/rar' or mime == 'application/x-rar' or rarfile.is_rarfile(path):
      print "file is probably a rar file"
      return ('rar', path, desc, mime)
    else:
      print "the path: %s is an unsupported file"
      print "it has this mime: %s" % mime
      print "and this description: %s" % desc
      return False
      
  elif os.path.isdir(path):
    print "manga: path is a directory"
    return ("folder", path, None, "a folder")
  else:
    print "manga: loading failed, path is neither file nor directory"
    return False

class Container:
  def __init__(self, path):
    self.path = path
    self.files = []
    self.imageFiles = []
    self.simpleImageDetection = True # use only extension matching, not mime to detect image files
    self.imageFileExtensions = ["png", "jpeg", "jpg", "bmp", "gif", "tiff", "xpm"]
    # TODO: find what image formats are actually supported by clutter ?

  def getFile(self, filename):
    """ return file object for a filename
    this is an abstract method, which must be implemented by each specialized subclass"""
    pass

  def getFileList(self):
    return self.files

  def getMaxId(self):
    return len(self.files)-1

  def getFileById(self, id):
    try:
      filename = self.files[id]
      return (self.getFile(filename),self.files.index(filename))
    except IndexError:
      print "no file with index:", id
      return None
    except TypeError:
      print "wrong index type:", id
      return None


  def getImageFile(self, filename):
    if filename in self.imageFiles:
      return self.getFile(filename)

  def getImageFileList(self):
    """only list files that are images according to mime"""
    return self.imageFiles


  def getMaxImageId(self):
    return len(self.imageFiles)-1

  def getImageFileById(self, id):
    try:
      filename = self.imageFiles[id]
      return (self.getFile(filename),self.imageFiles.index(filename))
    except IndexError, ValueError:
      print "no image file with index:", id
      return None

  def getImageFilenameById(self, id):
    try:
      filename = self.imageFiles[id]
      return filename
    except IndexError, ValueError:
      print "no image file with index:", id
      return "does not exist"

  def _setFileList(self, filenames, sort=True, useHumanSort=True):
    """NOTE: there can be not only files but also directories in the filelist"""
    start = time.clock()
    if sort:
      if useHumanSort:
        # human sort
        filenames = humanSort(filenames)
      else:
        # normal sort
        filenames.sort()
    duration = (1000 * (time.clock() - start))

#    for i in filenames:
#      print i
    
    print "%d filenames sorted in %1.2f ms, human sort: %r" % (len(filenames), duration, useHumanSort)

    self.files = filenames
    # update the image list
    self._setImageList(filenames)

  def _setImageList(self, filenames):
    """filter the provided filenames - filenames that are both files & images (by mime),
       will be set as the new imageList
       NOTE: this should be only call by the setFileList method to maintain consistency
       TODO: support for TXT info files
       """
    imageList = []
    for filename in filenames:
      if self._isImage(filename):
        imageList.append(filename)
    print "%d images found" % len(imageList)
    self.imageFiles = imageList

  def _isImage(self, filename):
    if self.simpleImageDetection:
      (basename, extension) = os.path.splitext(filename)
      if extension:
        extension = extension.lower()[1:] # remove the leading dot and make lowercase
        if extension.lower() in self.imageFileExtensions:
#          print "%s, extension: %s" % (filename, extension)
          return True
        else:
          return False # not a "supported" extension
      else:
        return False # no extension -> no image


    else:
      file = self.getFile(filename) # get the file object
      if file: # the file probably exists
        mime = getFileMime(file) # get its mime
        print "%s, mime: %s" % (filename, mime)
        mimeSplit = mime.split('/')
        m1 = mimeSplit[0]
        m2 = mimeSplit[1]
        if m1 == 'image':
          return True
        else:
          return False





class FolderContainer(Container):
  """This class represents a folder containing pictures."""
  def __init__(self, path):
    Container.__init__(self, path)
    if os.path.exists(path):
      folderContent = os.listdir(path)
      self._setFileList(folderContent)
    else:
      print "FolderContainer: folder does not exist: %s" % filename

    
  def getFile(self, filename):
    """just open the file and return a file object"""
    if filename not in self.files:
      print "FolderContainer: file not in file list: %s" % filename
      return None
    path = os.path.join(self.path,filename)
    if os.path.exists(path):
      if os.path.isfile(path):
        try:
          f = open(path, 'r')
          return f
        except Exception, e:
          print "FolderContainer: loading file failed: %s" % path
          return File

      else:
        print "FolderContainer: path is not a file: %s" % path
        return False

    else:
      print "FolderContainer: path does not exist: %s" % path
      return False

class ZipContainer(Container):
  """This class represents a zip archive containing pictures."""
  def __init__(self, path):
    Container.__init__(self, path)
    self.zf = None
    if zipfile.is_zipfile(path):
      try:
        self.zf = zipfile.ZipFile(path,'r')
      except Exception, e:
        "error, loading zip file failed: %s" % e
    else:
      print "error, this is not a zip file - wrong mime ?"
      print "path: %s" % path
    if self.zf:
      self._setFileList(self.zf.namelist())

  def getFile(self, filename):
    if self.zf:
      try:
        return self.zf.open(filename,'r')
      except Exception, e:
        print "ZipContainer: reading file from archive failed: %s" % e
        return None



class RarContainer(Container):
  """This class represents a rar archive containing pictures."""
  def __init__(self, path):
    Container.__init__(self, path)
    self.rf = None
    if rarfile.is_rarfile(path):
      try:
        self.rf = rarfile.RarFile(path,'r')
      except Exception, e:
        "error, loading rar file failed: %s" % e
    else:
      print "error, this is not a rar file - wrong mime ?"
      print "path: %s" % path
    if self.rf:
      self._setFileList(self.rf.namelist())

  def getFile(self, filename):
    if self.rf:
      try:
        return self.rf.open(unicode(filename),'r')
      except Exception, e:
        print "RarContainer: reading file from archive failed: %s" % e
        traceback.print_exc(file=sys.stdout)
        return None



class TarContainer(Container):
  """This class represents a tar archive containing pictures."""
  def __init__(self, path):
    Container.__init__(self, path)
    self.tf = None
    if rarfile.is_tarfile(path):
      try:
        self.tf = tarfile.TarFile(path,'r')
      except Exception, e:
        "error, loading rar file failed: %s" % e
    else:
      print "error, this is not a tar file - wrong mime ?"
      print "path: %s" % path
    if self.tf:
      self._setFileList(self.tf.namelist())

  def getFile(self, filename):
    if self.tf:
      try:
        return self.tf.open(filename,'r')
      except Exception, e:
        print "TarContainer: reading file from archive failed: %s" % e
        return None

