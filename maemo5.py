"""
Mieru hildon UI (for Maemo 5@N900)
"""
import os
import gtk
import gobject
import hildon

from base_platform import BasePlatform

class Maemo5(BasePlatform):
  def __init__(self, mieru):
    BasePlatform.__init__(self)

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
    selector.append_text_column(self.historyStore, False)
    selector.connect('changed', self._historyRowSelected)
    historyPickerButton = hildon.PickerButton(gtk.HILDON_SIZE_AUTO,hildon.BUTTON_ARRANGEMENT_VERTICAL)
    historyPickerButton.set_title("History")
    historyPickerButton.set_selector(selector)
    self.mieru.watch('openMangasHistory', self._updateHistoryCB)

    clearHistoryButton = gtk.Button("Clear history") # TODO: move this somewhere into settings
    clearHistoryButton.connect('clicked',self._clearHistoryCB)

    pagingButton = gtk.Button("Paging")
    pagingButton.connect('clicked',self.showPagingDialogCB)

    menu.append(openFileButton)
    menu.append(openFolderButton)
    menu.append(fullscreenButton)
    menu.append(historyPickerButton)
    menu.append(clearHistoryButton)
    menu.append(pagingButton)

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
      if not self.historyLocked:
        try:
          id = selector.get_active(0)
          if id >= 0:
            state = self.currentHistory[id]['state']
            path = state['path']
            print "path selected: %s" % path
            activeMangaPath = self.mieru.getActiveMangaPath()
            if path != activeMangaPath: # infinite loop defence
              self.mieru.openMangaFromState(state)
        except Exception, e:
          print "error while restoring manga from history"
          print e
#      else:
#        print "history locked"


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
        pageNumber = state['pageNumber']+1
        pageCount = state['pageCount']+1
        (folderPath,tail) = os.path.split(path)
        rowText = "%s %d/%d" % (tail, pageNumber, pageCount)

        self.historyStore.append((rowText,))
      self.currentHistory = sortedHistory
    self.historyLocked = False

  def _clearHistoryCB(self, button):
    self.mieru.clearHistory()
    self.historyLocked = True
    self.historyStore.clear()
    self.historyLocked = False


  def startChooser(self, type):
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
      self.mieru.openManga(selectedPath)

  def notify(self, message, icon=None):
    print message
#    hildon.hildon_banner_show_information_with_markup(self.mieru.window, "", message)
    hildon.hildon_banner_show_information_with_markup(self.mieru.window, "icon_text", message)

  def pagingDialogBeforeOpen(self):
    """notify the user that the window in tha bakcground does not live-update"""
    self.notify("<b>Note:</b> the page in background does not refresh automatically", None)

  def minimize(self):
    """minimizing is not supported on Maemo :)"""
    self.notify('hiding to panel is not supported ona Maemo (no panel :)', None)
