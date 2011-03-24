"""Mieru class aimed on overcomming various clutter shortcommings"""

import clutter
cache = []

class Opacity:
  def __init__(self, actor, function, duration, target, start=None):
    self.actor = actor
    self.function = function
    self.duration = duration
    if start is None:
      self.startValue = actor.get_opacity()
    else:
      self.startValue = start
    self.targetValue = target
    self.timeline = clutter.Timeline(self.duration)
    self.alpha = clutter.Alpha(self.timeline,self.function)
    self.BehOp = clutter.BehaviourOpacity(self.startValue, self.targetValue, self.alpha)
    self.BehOp.apply(actor)

  def getTimeline(self):
    return self.timeline

  def start(self):
    self.timeline.start()

def _add(object):
  """as reference counting in clutter is broken, we need to hold reference to animations in progress"""
  cache.append(object)

def _remove(timeline,bo):
  if bo in cache:
    cache.remove(bo)
    print "current cache status", cache

def animate(actor, function, duration, pairs):
  for pair in pairs:
    (property, targetValue) = pair
    if property == "opacity":
      start = actor.get_opacity()
      bo = Opacity(actor,function,duration,targetValue,start)
      bo.start()
      cache.append(bo)
      bo.getTimeline().connect('completed', _remove, bo)
    else:
      print "unknown property: ", property

