# -*- coding: utf-8 -*-
"""page_cache.py - a cache for manga pages for Mieru"""
from __future__ import with_statement # for python 2.5
import threading

class PageCache:
  def __init__(self, size=2):
    self.lock = threading.RLock()
    self.size = size
    self.items = {}
    self.history = []

  def add(self, page, id, direction):
    """add an item to cache,
    if an item with the same id is already inside,
    move the id to most recent in history
    and overwrite the page"""
    with self.lock:
      if id in self.items: # already present
        # move in history to most recent place
        self.items[id] = page
        print "* radd %d" % id
      else: #add new item
        self.history.append(id)
        self.history.sort()
        self.items[id] = page
        print "* add %d" % id
      if len(self.items) > self.size:
        self.trimToSize(self.size, direction)
        


  def get(self, id, default):
    with self.lock:
      item = self.items.get(id, default)

    return item

  def has(self, id):
    with self.lock:
      return id in self.items

  def trimToSize(self, size, direction):
    """trim the cache to a given size"""
    while len(self.items) > size:
      self._removeOldest(direction)

  def _removeOldest(self, direction):
    """remove oldest item in cache
    should be called with the lock acquired"""

    """the direction determines which item should be preferably removed
    +1 -> paging from previous to next => going forward
       -> remove oldest page
    -1 -> paging from next to previous => going back
       -> remove most recently added page
    """
    if direction > 0:
      rmIndex = 0
    else:
      rmIndex = -1


    id = self.history.pop(rmIndex)
    item = self.items.pop(id)
    self.destroyItem(item)

    print "rm %d" % id

  def destroyItem(self, item):
    # this is for pages
    # TODO arbitrary item support ?
    item.free()
    del item

  def statusReport(self):
    with self.lock:
      print("# page cache status report:")
      print("# items cached: %d" % len(self.items))
      print(self.items)
      print(self.history)

  def flush(self):
    print "flushing cache"
    self.trimToSize(0,0)



