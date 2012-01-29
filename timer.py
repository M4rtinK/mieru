"""a simple timing module

just call the "elapsed" with a time.clock() timestamp and a message you want displayed and
 timeit will print time elapsed since the timestamp in milliseconds

NOTE: repeat the timing multiple times to make sure it's consistent
"""

import time

def start():
  """a timestamp returning convenience function"""
  return time.clock()

def elapsed(start, message):
  """print the message and how much ms elapsed since the start timestamp"""
  duration = (1000 * (time.clock() - start))
  print("%s %1.2f ms" % (message, duration))