#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import urllib2
import sys
#noinspection PyCompatibility
import argparse
import progressive_download


URL_PREFIX = "http://www.baka-tsuki.org/project/index.php?title="
VOLUME_NAME = "Volume"
FULL_TEXT_SUFFIX="_Full_Text"
PRINT_SUFFIX = "&printable=yes"

def getFullName(name, number, volumeName=VOLUME_NAME):
  fullName = re.sub(" ", "_", name)
  fullName += ":" + volumeName + str(number)
  return fullName

def getUrl(fullName):
  """get Url for a given novel"""
  url = URL_PREFIX + fullName + FULL_TEXT_SUFFIX + PRINT_SUFFIX
  return url

def downloadNovel(fullName):
  """download a novel with the given fullname"""
  url = getUrl(fullName)
  # assure storage folder exists
  if not os.path.exists(fullName):
    os.mkdir(fullName)
  filePath = os.path.join(fullName, "%s.html" % fullName)
  downloadUrl(url, filePath)

def downloadUrl(url, path):
  progressive_download.download(url, path)


def isLocallyAvailable(fullName):
  """check if a novel with this full name is locally available"""
  return os.path.exists(fullName)

#def getStorageName(name, number, )

if __name__ == "__main__":
  # CLI argument parsing
  parser = argparse.ArgumentParser(description='Light novel processing.')
  parser.add_argument('name',
    help="light novel name",
    action="store")
  parser.add_argument('--number',
    help="volume number",
    action="store")
  parser.add_argument('--volume',
    help="override volume name",
    action="store")
  parser.add_argument('-r',
    help="re-download even if locally available",
    action="store_true")
  args = parser.parse_args()
  # get the novel name
  name = args.name
  fullName = getFullName(name, 1)
  print(fullName)
  if isLocallyAvailable(fullName):
    if args.r:
      print("re-downloading")
      downloadNovel(fullName)
    else:
      print("locally available")
  else:
    print("downloading")
    downloadNovel(fullName)




