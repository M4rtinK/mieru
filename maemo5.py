"""
Mieru hildon UI (for Maemo 5@N900)
"""
import gtk
import hildon

class Maemo5:
  def __init__(self, mieru):
    self.mieru = mieru
    self.enableZoomKeys(self.mieru.window)
    menu = hildon.AppMenu()
    openFolderButton = gtk.Button("Open folder")
    openFolderButton.connect('clicked',self.startFolderChooser)
    openFileButton = gtk.Button("Open file")
    openFileButton.connect('clicked',self.startFileChooser)
    menu.append(openFileButton)
    menu.append(openFolderButton)
    # Show all menu items
    menu.show_all()

    # Add the menu to the window
    self.mieru.window.set_app_menu(menu)


  def enable_zoom_cb(self, window):
	window.window.property_change(gtk.gdk.atom_intern("_HILDON_ZOOM_KEY_ATOM"), gtk.gdk.atom_intern("INTEGER"), 32, gtk.gdk.PROP_MODE_REPLACE, [1]);

  def disableZoom(self):
	self.window.property_change(gtk.gdk.atom_intern("_HILDON_ZOOM_KEY_ATOM"), gtk.gdk.atom_intern("INTEGER"), 32, gtk.gdk.PROP_MODE_REPLACE, [0]);

  def enableZoomKeys(self,window):
          if window.flags() & gtk.REALIZED:
                  enable_zoom_cb(window)
          else:
                  window.connect("realize", self.enable_zoom_cb)

  def startFolderChooser(self, foo=None):
    dialog = hildon.FileChooserDialog(self.mieru.window, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER) 
    lastFolder = self.mieru.get('lastChooserFolder', None)
    currentFolder = None
    if lastFolder:
      dialog.set_current_folder(lastFolder)
    if dialog.run() == gtk.RESPONSE_OK:
      currentFolder = dialog.get_current_folder()
      path = dialog.get_filename()
    dialog.destroy()
    if currentFolder != None:
      self.mieru.set('lastChooserFolder', currentFolder)
    self.mieru.openManga(path)

  def startFileChooser(self, foo=None):
    dialog = hildon.FileChooserDialog(self.mieru.window, gtk.FILE_CHOOSER_ACTION_OPEN)
    lastFolder = self.mieru.get('lastChooserFolder', None)
    currentFolder = None
    if lastFolder:
      dialog.set_current_folder(lastFolder)
    if dialog.run() == gtk.RESPONSE_OK:
      currentFolder = dialog.get_current_folder()
      path = dialog.get_filename()
    dialog.destroy()
    if currentFolder != None:
      self.mieru.set('lastChooserFolder', currentFolder)
    self.mieru.openManga(path)

  def notify(self, message, icon):
    print message
#    hildon.hildon_banner_show_information_with_markup(self.mieru.window, "", message)
    hildon.hildon_banner_show_information_with_markup(self.mieru.window, "icon_text", message)



