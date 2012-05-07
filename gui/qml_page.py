# -*- coding: utf-8 -*-
"""qml_page.py - a manga/comix book page based on an QML image"""

import page


class QMLPage(page.Page):
  def __init__(self, image, gui):
    page.Page.__init__(self)
    self.image=image
    self.gui = gui
    """as the image data is actually managed by QML,
    the page object just stores an image id"""

  def activate(self):
    """start reacting on dragging and stage resize
    - page is not activated by default"""
    pass

  def deactivate(self):
    """stop reacting on dragging and stage resize"""
    pass

  def show(self):
    pass

  def getSize(self):
    """return image resolution"""
    return(0,0)

  def free(self):
    """quickly release all resources"""
    pass

  def popImage(self):
    """return the corresponding image file object and
    remove local references to it"""
    output = self.image
    self.image = None
    return output
