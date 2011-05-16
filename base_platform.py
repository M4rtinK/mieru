"""this is a "abstract" class defining the API for platform modules
   NOTE: this is not just API, some multiplatform implementations are there too
"""

import gtk

class BasePlatform:
  def __init__(self):
    pass

  def hasPagingKeys(self):
    """report if the device has has some buttons usable for paging"""
    return False

  def startChooser(self, type):
    """start a file/folder chooser dialog"""
    pass

  def handleKeyPress(self, widget, event):
    """handle a key press event and return True if the key was "consumed" or
    "False" if it wasn't"""
    return False

  def notify(self, message, icon):
    """show a notification, if possible"""
    pass

  def showPagingDialog(self, button):
    # get data
    activeManga = self.mieru.getActiveManga()
    if activeManga:
      currentPage = activeManga.getActivePageNumber()
      lastPage = activeManga.getMaxPageNumber()
    else:
      currentPage = 1
      lastPage = currentPage + 1

    label = "Paging 1-%d" % lastPage
    dialog = gtk.Dialog(
        label,
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_NO_SEPARATOR,
#                      gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
#        (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
        ()
        )
      #create the text input field
    entry = gtk.Entry()
    entry.set_text("%d" % currentPage)
    entry.select_region(0,-1)
    # make sure the text is visible (TODO: respect current theme, but make sure the text will be visible ?)
    entry.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
    entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
    #allow the user to press enter to do ok
#    entry.connect("activate", self.respondToTextEntry, dialog, gtk.RESPONSE_OK, instance,key)
#    dialog.connect("response", self.respondToDialog,entry, instance,key)
    """create a vbox and pack two hboxes into it"""
#    vbox = gtk.VBox(True)
    hBox1 = gtk.HBox(True)
    hBox2 = gtk.HBox(True)

    # add the scale widget
    pagingAdj = gtk.Adjustment(currentPage, 1, lastPage, 1)
    scale = gtk.HScale(pagingAdj)
    scale.set_digits(0) # integers only
    scale.set_draw_value(True) # show current value next to slider
    hBox1.pack_start(scale)
    # add the paging buttons
    firstButton = gtk.Button("first page")
    backButton = gtk.Button("back to %d" % currentPage)
    lastButton = gtk.Button("last page")
    doneButton = gtk.Button("done")
    hBox2.pack_start(firstButton)
    hBox2.pack_start(lastButton)
    hBox2.pack_start(backButton)
    hBox2.pack_start(entry)
    hBox2.pack_start(doneButton)


    #some secondary text
#      dialog.format_secondary_markup("This will be used for <i>identification</i> purposes")
    #add it and show it
    dialog.vbox.pack_start(hBox1)
    dialog.vbox.pack_start(hBox2)
#    dialog.vbox.pack_end(vbox, True, True, 0)
    (width, height) = dialog.get_size() # get the current size
    (x,y,w,h) = self.mieru.getViewport()
    dialog.resize(w,height) # resize the dialog to the width of the window and leave height the same
    dialog.set_keep_above(True)
    dialog.show_all()
