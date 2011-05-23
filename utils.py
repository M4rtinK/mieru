"""various miscantelous utility functions for Mieru"""


def wasClick(dt, dx,dy):
  """decide if provided event was a click or not"""
  print "was"
  print(dt, dx,dy)
#  distSq = fullDx * fullDx + fullDy * fullDy
  distSq = dx * dx + dy * dy
  print(distSq)

