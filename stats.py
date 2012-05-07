# -*- coding: utf-8 -*-
"""a funny statistics module for Mieru"""

class Stats:
  def __init__(self, mieru):
    self.mieru = mieru

  def isOn(self):
    """inform if keeping statistics is enabled"""
    if self.mieru.get('statsOn', True):
      return True
    else:
      return False

  def setOn(self, value):
    if value is True or value is False:
      self.mieru.set('statsOn', value)
      if value is True:
        print("stats: ON")
      else:
        print("stats: OFF")
    else:
      print("stats: value must be True or False, not: ", value)

  def getStats(self):
    return self._getStats()

  def resetStats(self):
    """wipe stats"""
    self._saveStats({})
    self.mieru.set('statsPageCount', 0)

  def _getStats(self):
    """get the statistics dictionary and create a new one if none exists"""
    stats = self.mieru.get('stats', None)
    if stats:
      return stats
    else:
      return {}

  def _saveStats(self, stats):
    """save the provided statistics dictionary to the main persistent dict"""
    self.mieru.set('stats', stats)

  def _updateStats(self, key, increment, initialValue):
    """update an item in the statistics dictionary"""
    stats = self._getStats()
    if key in stats:
      stats[key] = stats[key] + increment
    else:
      stats[key] = initialValue + increment
    self._saveStats(stats)

  def incrementPageCount(self):
    """for perceived performance reasons, page counter uses its own variable"""
    if self.isOn():
      count = self.mieru.get('statsPageCount', 0)
      self.mieru.set('statsPageCount', count + 1)

  def incrementUnitCount(self):
    """increment unit (manga/comic book/chapter/directory) count"""
    if self.isOn():
      self._updateStats("unitCount", 1, 0)

  def updateUsageTime(self, increment):
    """usage time is in seconds, integer only"""
    if self.isOn():
      increment = int(increment)
      self._updateStats("usageTime", increment, 0)

  def getStatsText(self, headline=True):
    """get a pretty formatted stats info"""
    # TODO: more efficient string concatenation ? (if it makes sense here)
    stats = self._getStats()
    if headline:
      text = "<b>Usage statistics</b>"
    else:
      text = ""
    if self.isOn():
      statsFound = False
      if "\nunitCount" in stats:
        statsFound = True
        text+= "\n<b>units total:</b> %d" % stats["unitCount"]
      pageCount = self.mieru.get("statsPageCount", None)
      if pageCount:
        statsFound = True
        text+= "\n<b>pages total:</b> %d" % pageCount
      if "usageTime" in stats:
        statsFound = True
        text+= "\n<b>time open:</b> %.1f hours" % (stats["usageTime"]/3600.0) #TODO: nicer conversion
      if statsFound is False:
        text+=" <b>\nempty</b>"
    else:
      text+=" <b>\ndisabled</b>"

    return text






