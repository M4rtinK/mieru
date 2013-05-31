#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
try:  # Python 2
  from urllib2 import urlopen, HTTPError, URLError
except ImportError:  # Python 3
  from urllib.request import urlopen
  from urllib.error import HTTPError, URLError
#noinspection PyCompatibility
import argparse
import progressive_download


URL_PREFIX = "http://www.baka-tsuki.org/project/index.php?title="
MAIN_PAGE = "http://www.baka-tsuki.org/project/index.php?title=Main_Page"
VOLUME_NAME = "Volume"
PRINT_SUFFIX = "&printable=yes"
NOVEL_LIST_VALID = 24 # in hours

def getFullName(name, number, volumeName=VOLUME_NAME):
  fullName = re.sub(" ", "_", name)
  fullName += ":" + volumeName + str(number)
  return fullName

def getUrl(fullName):
  """get Url for a given novel"""
  url = URL_PREFIX + fullName + PRINT_SUFFIX
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

def listAllAvailableNovels():
  """list all novels available from Bakatsuki"""
  LN = 0
  h = urlopen(MAIN_PAGE)
  novels = []
  for i in range(500):
    data = h.readline()
    if re.search(r"- Light Novels -->",str(data)) is not None:
      LN = 1
    if re.search(r"- /Light Novels -->",str(data)) is not None:
      LN = 0

    #print (re.search(r"- Light Novels -->",str(data)))
    #data = data.decode('utf-8', errors='replace')
    # print (str(data))
    #found = re.findall(".*title\=.*\">.*</a></li>",str(data))
    if LN == 1:
      #found = re.findall("index.php\?title\=.*\">",str(data))
      found = re.search("index.php\?title\=(.*)\">", str(data))
      # found = re.findall("index.php\?title\=.*\">",str(data))
      # purge the prefix
      #found = re.sub("index.php\?title\=.*\">", "", found)
      if found:
        novels.append(found.group(1))

  h.close()
  for novel in novels:
    print(novel.replace("_"," "))

#def getStorageName(name, number, )

if __name__ == "__main__":
  # CLI argument parsing
  parser = argparse.ArgumentParser(description='Light novel processing.')
  parser.add_argument('name',
    help="light novel name",
    action="store",
    nargs='?',
    default=None)
  parser.add_argument('--number',
    help="volume number",
    action="store")
  parser.add_argument('--volume',
    help="override volume name",
    action="store")
  parser.add_argument('-r',
    help="re-download even if locally available",
    action="store_true")
  parser.add_argument('--list',
    help="list all available light novels",
    action="store_true")
  args = parser.parse_args()
  # get name of the novel
  if args.list:
    listAllAvailableNovels()
  else:
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




