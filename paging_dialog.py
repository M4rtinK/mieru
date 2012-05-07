# -*- coding: utf-8 -*-
"""provides paging dialog for Mieru"""
import gtk
import re

class PagingDialog:
  def __init__(self, manga, viewport=None, info=None):
    self.active = True
    self.dialog = self._showPagingDialog(manga, viewport, info)
    self.scalePressed = False

  def _showPagingDialog(self, manga, viewport, info):
    # get data
    if manga:
      currentPage = manga.getActivePageNumber()
      lastPage = manga.getMaxPageNumber()
    else:
      currentPage = 1
      lastPage = currentPage + 1

    label = "Paging 1-%d" % lastPage
    dialog = gtk.Dialog(
        label,
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_NO_SEPARATOR,
        ()
        )
      #create the number input field
#    entry = gtk.Entry()
#    entry.set_text("%d" % currentPage)
#    entry.select_region(0,-1)
#    # make sure the text is visible (TODO: respect current theme, but make sure the text will be visible ?)
#    entry.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
#    entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))





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

    """for performance reasons we want that paging does not occur
    while user is dragging the slider - new page should be loaded only after the user
    releases the slider"""

    scale.connect('value-changed', self._scaleValueChangedCB, manga)
    scale.connect('button-press-event', self._scalePressedCB, manga)
    scale.connect('button-release-event', self._scaleReleasedCB, manga)
    hBox1.pack_start(scale)

    # create the numeric entry widget
    nrEntry = gtk.SpinButton(pagingAdj)


    # add the paging buttons
    firstButton = gtk.Button("first page")
    firstButton.connect('clicked',self._gotoPageAndDestroyCB, manga, 0, True)
    lastButton = gtk.Button("last page")
    lastButton.connect('clicked',self._gotoPageAndDestroyCB, manga, -1, True)
    backButton = gtk.Button("back to %d" % currentPage)
    backButton.connect('clicked',self._gotoPageAndDestroyCB, manga, currentPage-1, True)
    doneButton = gtk.Button("done")
    doneButton.connect('clicked',self._destroyCB)
    hBox2.pack_start(firstButton)
    hBox2.pack_start(lastButton)
    hBox2.pack_start(backButton)
    hBox2.pack_start(nrEntry)
    hBox2.pack_start(doneButton)


    #some secondary text
#      dialog.format_secondary_markup("This will be used for <i>identification</i> purposes")
    #add it and show it
    if info:
      infoLabel = gtk.Label()
      infoLabel.set_markup(description)
      infoLabel.set_line_wrap(True)
      infoLabel.set_max_width_chars(-1)
#      vbox.pack_start(descLabel, True, True, 5)
      dialog.vbox.pack_start(infoLabel)

    dialog.vbox.pack_start(hBox1)
    dialog.vbox.pack_start(hBox2)
#    dialog.vbox.pack_end(vbox, True, True, 0)
    if viewport:
      (width, height) = dialog.get_size() # get the current size
      (x,y,w,h) = self.mieru.getViewport()
      dialog.resize(w,height) # resize the dialog to the width of the window and leave height the same
    dialog.set_keep_above(True)
    dialog.show_all()
    return dialog

  def _destroyDialog(self):
    if self.dialog:
      self.dialog.destroy()

  def _destroyCB(self, button):
    """just destroy the dialog"""
    self._destroyDialog()

  def _gotoPageAndDestroyCB(self, button, manga, pageId, destroy=True):
    """select turn a page in the manga to a desired id and optionally destroy the dialog"""
    manga.gotoPageId(pageId)
    if destroy:
      self._destroyDialog()

  def _scaleValueChangedCB(self, range, manga):
    if not self.scalePressed:
      self._turnPage(manga, int(range.get_value()-1))

  def _scalePressedCB(self,scale, event, manga):
    self.scalePressed = True

  def _scaleReleasedCB(self,scale, event, manga):
    self._turnPage(manga,int(scale.get_value()-1))
    self.scalePressed = False

  def _turnPage(self, manga, pageId):
    """turn to a new page, if the current page is id is same as the new id do nothing"""
    currentId = manga.getActivePageId()
    if currentId != pageId: # no need to repage the current page
      manga.gotoPageId(pageId)
    