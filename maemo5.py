"""
Mieru hildon UI (for Maemo 5@N900)
"""
import os
import gtk
import gobject
import hildon

class Maemo5:
  def __init__(self, mieru):
    self.mieru = mieru

    # enbale zoom/volume keys for usage by mieru
    self.enableZoomKeys(self.mieru.window)

    # add application menu
    menu = hildon.AppMenu()
    openFolderButton = gtk.Button("Open folder")
    openFolderButton.connect('clicked',self.startChooser, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
    openFileButton = gtk.Button("Open file")
    openFileButton.connect('clicked',self.startChooser, gtk.FILE_CHOOSER_ACTION_OPEN)
    fullscreenButton = gtk.Button("Fullscreen")
    fullscreenButton.connect('clicked',self.mieru.toggleFullscreen)

    # last open mangas list
    selector = hildon.TouchSelector()
    selector.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE)
    self.historyStore = gtk.ListStore(gobject.TYPE_STRING)
    self.historyLocked = False
    self._updateHistory()
    selector.append_text_column(self.historyStore, True)
    selector.connect('changed', self._historyRowSelected)
    historyPickerButton = hildon.PickerButton(gtk.HILDON_SIZE_AUTO,hildon.BUTTON_ARRANGEMENT_VERTICAL)
    historyPickerButton.set_title("History")
    historyPickerButton.set_selector(selector)
    self.mieru.watch('openMangasHistory', self._updateHistoryCB)

    menu.append(openFileButton)
    menu.append(openFolderButton)
    menu.append(fullscreenButton)
    menu.append(historyPickerButton)

    # Show all menu items
    menu.show_all()

    # Add the menu to the window
    self.mieru.window.set_app_menu(menu)


  def enable_zoom_cb(self, window):
    window.window.property_change(gtk.gdk.atom_intern("_HILDON_ZOOM_KEY_ATOM"), gtk.gdk.atom_intern("INTEGER"), 32, gtk.gdk.PROP_MODE_REPLACE, [1]);

  def disableZoomKeys(self):
    self.window.property_change(gtk.gdk.atom_intern("_HILDON_ZOOM_KEY_ATOM"), gtk.gdk.atom_intern("INTEGER"), 32, gtk.gdk.PROP_MODE_REPLACE, [0]);

  def enableZoomKeys(self,window):
          if window.flags() & gtk.REALIZED:
                  enable_zoom_cb(window)
          else:
                  window.connect("realize", self.enable_zoom_cb)

  def _updateHistoryCB(self, key=None, value=None, oldValue=None):
    print "update history"
    self._updateHistory()

  def _historyRowSelected(self, selector, column):
    id = selector.get_active(0)
    if not self.historyLocked:
      print "ROW SELECTED", column, id
  #    print selector.get_selected_rows(0)
      if id >= 0:
        state = self.currentHistory[id]['state']
        path = state['path']
        activeMangaPath = self.mieru.getActiveMangaPath()
        if path != activeMangaPath: # infinite loop defence
          self.mieru.openMangaFromState(state)
    else:
      print "history lcoked"

  def _updateHistory(self):
    """
    due to the fact that the touch selector emits the same signal when an
    item is selected like when an item is clicked on, we need to do this
    primitive locking
    """
    self.historyLocked = True
    sortedHistory = self.mieru.getSortedHistory()
    if sortedHistory:
      self.historyStore.clear()
      for item in sortedHistory:
        state = item['state']
        path = state['path']

        (folderPath,tail) = os.path.split(path)
        self.historyStore.append((tail,))
      self.currentHistory = sortedHistory
    self.historyLocked = False
      

  def startChooser(self, button, type):
    dialog = hildon.FileChooserDialog(self.mieru.window, type)
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

  def notify(self, message, icon):
    print message
#    hildon.hildon_banner_show_information_with_markup(self.mieru.window, "", message)
    hildon.hildon_banner_show_information_with_markup(self.mieru.window, "icon_text", message)



