"""an ui/device/platform module targeted on desktop PCs"""

import gtk

from base_platform import BasePlatform

class PC(BasePlatform):
  def __init__(self, mieru):
    BasePlatform.__init__(self)
    self.mieru = mieru

  def hasPagingKeys(self):
    """keyboard support"""
    return True

  def startChooser(self, type):
    buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK)
    dialog = gtk.FileChooserDialog("Open file",self.mieru.window, type, buttons=buttons)
    lastFolder = self.mieru.get('lastChooserFolder', None)
    currentFolder = None
    selectedPath = None
    if lastFolder:
      dialog.set_current_folder(lastFolder)
    status = dialog.run()
    dialog.hide()
    if status == gtk.RESPONSE_OK:
      currentFolder = dialog.get_current_folder()
      selectedPath = dialog.get_filename()
    dialog.destroy()
    if currentFolder != None:
      self.mieru.set('lastChooserFolder', currentFolder)
    if selectedPath:
      print "open"
      self.mieru.openManga(selectedPath)





