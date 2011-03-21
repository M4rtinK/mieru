"""
Mieru hildon UI (for Maemo 5@N900)
"""
import gtk
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

    menu.append(openFileButton)
    menu.append(openFolderButton)
    menu.append(fullscreenButton)
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



