"""page.py - a manga/comix book page"""

class Page:
  def __init__(self):
    pass

  def activate(self):
    """start reacting on dragging and stage resize
    - page is not activated by default"""
    pass

  def deactivate(self):
    """stop reacting on dragging and stage resize"""
    pass

  def getSize(self):
    """return image resolution"""
    return(0,0)
