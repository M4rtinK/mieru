#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import urllib2
import sys
#noinspection PyCompatibility
import argparse


URL_PREFIX = "http://www.baka-tsuki.org/project/index.php?title="
VOLUME_NAME = "Volume"
PRINT_SUFFIX = "&printable=yes"

def getFullName(name, number, volumeName=VOLUME_NAME):
  fullName = re.sub(" ", "_", name)
  fullName += ":" + volumeName + str(number)
  return fullName

def getUrl(fullName):
  """
  get Url for a given novel
  """
  url = URL_PREFIX + fullName + PRINT_SUFFIX
  return url

#def getStorageName(name, number, )

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Light novel processing.')
  parser.add_argument('--name',
    help="light novel name",
    action="store")
  parser.add_argument('--number',
    help="volume number",
    action="store")
  parser.add_argument('--volume',
    help="override volume name",
    action="store")
  args = parser.parse_args()
  name = args.name
  fullName = getFullName(name, 1)
  print fullName
  url = getUrl(fullName)
  print url
  result = urllib2.urlopen(url)
  os.mkdir(fullName)
  filePath = os.path.join(fullName, "%s.html" % fullName)
  f = open(filePath, "w")
  f.write(result.read())
  f.close




