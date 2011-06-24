"""an ui/device/platform module targeted on desktop PCs"""

import gtk

from base_platform import BasePlatform

class PC(BasePlatform):
  def __init__(self, mieru):
    BasePlatform.__init__(self)
    self.mieru = mieru
    self.mb = self._addMenu()

  def hasPagingKeys(self):
    """keyboard support"""
    return True

  def startChooser(self, type):
    if type == "folder":
      t = gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER
    else: # type == "file"
      t = gtk.FILE_CHOOSER_ACTION_OPEN

    buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK)
    dialog = gtk.FileChooserDialog("Open file",self.mieru.window, t, buttons=buttons)
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

  def startChooserCB(self, button, type):
    self.startChooser(type)

  def _addMenu(self):
    """add main menu"""

    if self.mieru.gui.getToolkit() == "GTK":
      print "ADASDADASDASDASD"
      mvbox = self.mieru.gui.getVbox()
      window = self.mieru.gui.getWindow()
      mb = gtk.MenuBar()
      filemenu = gtk.Menu()
      filem = gtk.MenuItem("_File")
      filem.set_submenu(filemenu)

      agr = gtk.AccelGroup()
      window.add_accel_group(agr)

      openm = gtk.ImageMenuItem(gtk.STOCK_OPEN, agr)
      key, mod = gtk.accelerator_parse("<Control>O")
      openm.add_accelerator("activate", agr, key,
          mod, gtk.ACCEL_VISIBLE)
      filemenu.append(openm)
      openm.connect("activate", self.startChooserCB, "file")

      sep = gtk.SeparatorMenuItem()
      filemenu.append(sep)

      exit = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)
      key, mod = gtk.accelerator_parse("<Control>Q")
      exit.add_accelerator("activate", agr, key,
          mod, gtk.ACCEL_VISIBLE)

      exit.connect("activate", gtk.main_quit)

      filemenu.append(exit)

      mb.append(filem)

      mvbox.pack_start(mb, False, False, 0)

      # hide the menu bar when in fullscreen

      # connect window state CB
      window.connect('window-state-event', self._fullscreenCB)

      mvbox.show_all()

      return mb


  def _fullscreenCB(self, window, event):
    """hide the menu bar when in fullscreen"""
    if event.changed_mask & gtk.gdk.WINDOW_STATE_FULLSCREEN:
      fullscreen = bool(event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN)
      if fullscreen:
        if self.mb:
          self.mb.hide()
      else:
        if self.mb:
          self.mb.show()

  def minimize(self):
    """minimize the main window"""
    self.mieru.getWindow().iconify()







