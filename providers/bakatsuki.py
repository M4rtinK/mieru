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
IMAGE_URL_BASE = 'http://www.baka-tsuki.org'
VOLUME_NAME = "Volume"
PRINT_SUFFIX = "&printable=yes"
NOVEL_LIST_VALID = 24 # in hours
TEMPORARY_FILE = "temp.opf"

## EPUB constants ##
EPUB_MIME = "application/epub+zip"

# folders - toplevel
EPUB_METADATA_FOLDER = "META-INF"
EPUB_DATA_FOLDER = "OEBPS"

# folders - nested
EPUB_TOPLEVEL_FOLDER = "epub_content"
EPUB_IMAGE_FOLDER = os.path.join(EPUB_DATA_FOLDER, "Images")
EPUB_STYLE_FOLDER = os.path.join(EPUB_DATA_FOLDER, "Styles")
EPUB_TEXT_FOLDER = os.path.join(EPUB_DATA_FOLDER, "Text")

# files - toplevel
EPUB_MIME_FILE = "mimetype"
# files - metadata
EPUB_CONTAINER_FILE = os.path.join(EPUB_METADATA_FOLDER, "container.xml")
# files - data
EPUB_CONTENT_FILE = os.path.join(EPUB_DATA_FOLDER, "content.opf")
EPUB_TOC_FILE = os.path.join(EPUB_DATA_FOLDER, "toc.ncx")
# files - data - styles
EPUB_STYLE_TEMPLATE_FILE = os.path.join(EPUB_STYLE_FOLDER, "page-template.xpgt")
EPUB_STYLESHEET_FILE = os.path.join(EPUB_STYLE_FOLDER, "stylesheet.css")
# files - data - text
# TODO more chapters ?
EPUB_CHAPTER_FILE = os.path.join(EPUB_TEXT_FOLDER, "chap01.xhtml")
EPUB_CHAPTER_FILE_TEMP = os.path.join(EPUB_TEXT_FOLDER, "chap01temp.xhtml")
EPUB_TITLE_PAGE_FILE = os.path.join(EPUB_TEXT_FOLDER, "title_page.xhtml")


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
  """Download URL if it is not already available"""
  if os.path.exists(path):
    print("not downloading, already exists:\n%s" % path)
  else:
    progressive_download.download(url, path)

def isLocallyAvailable(fullName):
  """check if a novel with this full name is locally available"""
  return os.path.exists(fullName)

def assurePath(path):
  """Make sure all directories in given path exist"""
  if not os.path.exists(path):
    print("creating dirs in path:\n%s" % path)
    os.makedirs(path)

def processHTML(fullName):
  """Process the raw HTML from Bakatsuki to a form usable for making EPUBs"""

  EXP = 0 #end of site
  H2 = 0 #start of novel text
  WIKI_TABLE = 0 #end of novel text

  print("opening novel: %s" % fullName)
  print("directory: %s" % fullName)
  filename = fullName + ".html"
  print("filename: %s" % filename)
  # folder name is fullName
  # filename is fullName + .html
  chapterFile = open(os.path.join(fullName,filename), "rt")
  novel = chapterFile.read()
  chapterFile.close()
  # get title of the novel
  TITLE = getTitle(novel)

  # switch to the EPUB content folder
  toplevelFolder = os.path.join(fullName, EPUB_TOPLEVEL_FOLDER)
  assurePath(toplevelFolder)
  print("switching to: %s" % toplevelFolder)
  os.chdir(toplevelFolder)
  # make sure all the needed folders exist
  assurePath(EPUB_METADATA_FOLDER)
  assurePath(EPUB_DATA_FOLDER)
  assurePath(EPUB_IMAGE_FOLDER)
  assurePath(EPUB_STYLE_FOLDER)
  assurePath(EPUB_TEXT_FOLDER)

  ### Start the content.opf file, add title ###
  contentFile = open(EPUB_CONTENT_FILE, 'w')
  contentFile.write("\
<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"BookID\" version=\"2.0\">\n\
    <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:opf=\"http://www.idpf.org/2007/opf\">\n\
        <dc:title>" + TITLE + "</dc:title>\n\
	<dc:language>en</dc:language>\n\
        <dc:rights>Public Domain</dc:rights>\n\
        <dc:creator opf:role=\"aut\">disciple961</dc:creator>\n\
        <dc:publisher>baka-tsuki.com</dc:publisher>\n\
        <dc:identifier id=\"BookID\" opf:scheme=\"UUID\">015ffaec-9340-42f8-b163-a0c5ab7d0611</dc:identifier>\n\
        <meta name=\"Sigil version\" content=\"0.2.4\"/>\n\
    </metadata>\n\
    <manifest>\n\
    <item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\"/>\n\
")
  ### content.opf still open. get_images procedure adds lines if pictures are present ###

  ### Start the chapter file with novel text, add title ###
  chapterFile = open(EPUB_CHAPTER_FILE, 'w', encoding='utf-8')
  chapterFile.write("\
<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\"\n\
  \"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">\n\
\n\
<html xmlns=\"http://www.w3.org/1999/xhtml\">\n\
<head>\n\
  <title>" + TITLE + "</title>\n\
  <link rel=\"stylesheet\" href=\"../Styles/stylesheet.css\" type=\"text/css\" />\n\
  <link rel=\"stylesheet\" type=\"application/vnd.adobe-page-template+xml\" href=\"../Styles/page-template.xpgt\" />\n\
</head>\n\
\n\
<body>\n\
  <div>\n\
")
  ### chapter file still open ###

  for line in novel.splitlines():
    if H2 == 0:
      if re.search(r'<h2> <span class="mw-headline"', line) is not None:
        H2 = 1
    if WIKI_TABLE == 0:
      if re.search(r'<table class="wikitable"', line) is not None:
        WIKI_TABLE = 1
    if (H2 == 1) and (WIKI_TABLE == 0):
      if re.search('src="/project/images/thumb/', line) is not None:
        print (re.search('src="/project/images/thumb/', line))
        getImages(line, contentFile, chapterFile)
        ### if the line contains an image, the procedure adds the appropriate tags into the chapter.xhtml and content.opf files ###
      else:
        chapterFile.write(line)
        ### if the line doesnt contain a picture, it contains text and will be added into the chapter.xhtml ###
    if re.search('</html>', line) is not None:
      EXP = 1

  ### end of the chapter file ###
  chapterFile.write("\n\
  </div>\n\
</body>\n\
</html>\n\
")
  chapterFile.close()
  ### end of the chapter file ###

  ### end of the content.opf file ###
  contentFile.write("\
        <item id=\"page-template.xpgt\" href=\"Styles/page-template.xpgt\" media-type=\"application/vnd.adobe-page-template+xml\"/>\n\
        <item id=\"stylesheet.css\" href=\"Styles/stylesheet.css\" media-type=\"text/css\"/>\n\
        <item id=\"chap01.xhtml\" href=\"Text/chap01.xhtml\" media-type=\"application/xhtml+xml\"/>\n\
        <item id=\"title_page.xhtml\" href=\"Text/title_page.xhtml\" media-type=\"application/xhtml+xml\"/>\n\
    </manifest>\n\
    <spine toc=\"ncx\">\n\
        <itemref idref=\"title_page.xhtml\"/>\n\
        <itemref idref=\"chap01.xhtml\"/>\n\
        <itemref idref=\"chap02.xhtml\"/>\n\
    </spine>\n\
</package>\n\
")
  contentFile.close()
  ### end of the content.opf file ###


  ### adds title to the table of contents ###
  tocFile = open(EPUB_TOC_FILE, 'w')
  tocFile.write("\
<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
<!DOCTYPE ncx PUBLIC \"-//NISO//DTD ncx 2005-1//EN\"\n\
   \"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd\">\n\
\n\
<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">\n\
    <head>\n\
        <meta name=\"dtb:uid\" content=\"015ffaec-9340-42f8-b163-a0c5ab7d0611\"/>\n\
        <meta name=\"dtb:depth\" content=\"1\"/>\n\
        <meta name=\"dtb:totalPageCount\" content=\"0\"/>\n\
        <meta name=\"dtb:maxPageNumber\" content=\"0\"/>\n\
    </head>\n\
    <docTitle>\n\
        <text>" + TITLE + "</text>\n\
    </docTitle>\n\
    <navMap>\n\
        <navPoint id=\"navPoint-1\" playOrder=\"1\">\n\
            <navLabel>\n\
                <text>" + TITLE + "</text>\n\
            </navLabel>\n\
            <content src=\"Text/title_page.xhtml\"/>\n\
        </navPoint>\n\
        <navPoint id=\"navPoint-2\" playOrder=\"2\">\n\
            <navLabel>\n\
                <text>" + TITLE + "</text>\n\
            </navLabel>\n\
            <content src=\"Text/chap01.xhtml\"/>\n\
        </navPoint>\n\
    </navMap>\n\
</ncx>\n\
")
  tocFile.close()

  # remove the Baka-Tsuki suffix from the title
  TITLE = TITLE.replace('- Baka-Tsuki', '')

  ### adds title to the title page ###
  titleFile = open(EPUB_TITLE_PAGE_FILE, 'w', encoding='utf-8')
  titleFile.write("\
  <?xml version=\"1.0\" encoding=\"utf-8\"?>\n\
  <!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\"\n\
    \"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">\n\
  \n\
  <html xmlns=\"http://www.w3.org/1999/xhtml\">\n\
  <head>\n\
    <title>" + TITLE + "</title>\n\
    <link rel=\"stylesheet\" href=\"../Styles/stylesheet.css\" type=\"text/css\" />\n\
    <link rel=\"stylesheet\" type=\"application/vnd.adobe-page-template+xml\" href=\"../Styles/page-template.xpgt\" />\n\
  </head>\n\
  \n\
  <body>\n\
    <div>\n\
      <h2 id=\"heading_id_2\">" + TITLE + "</h2>\n\
      <h2 id=\"heading_id_3\">Baka-Tsuki</h2>\n\
  ")
  titleFile.close()

def getTitle(novel):
  """Extract the title from the given light novel"""
  return re.search('<title>(.*)</title>', novel).group(1)

def getImages(line, contentFile, chapterFile):
  imgUrls = re.findall('(src="/project/images/thumb/.*\.jpg|src="/project/images/thumb/.*\.png)', line)
  if imgUrls != []:
    print("IMAGE PROCESSING")
    imgUrl = imgUrls[0]
    # remove unneeded prefix
    imgUrl = str(imgUrl).replace("src=\"/project/images/thumb/", "")
    # remove unneeded suffix (stuff after ")
    imgUrl = imgUrl.split("\"")[0]
    # remove the unneeded image suffix
    # (strip everything after the last slash)
    imgUrl = imgUrl.rsplit("/", 1)[0]

    IMG_URL = IMAGE_URL_BASE + "/project/images/" + str(imgUrl)
    print("Download URL:")
    print(IMG_URL)
    imageFilename = imgUrl.rsplit("/", 1)[1]
    downloadPath = os.path.join(EPUB_IMAGE_FOLDER, imageFilename)
    downloadUrl(IMG_URL, downloadPath)


    # IMAGE = urlopen(IMG_URL)#, IMG_URL[46:])
    # path = CUSTOM_PATH + "\sample\OEBPS\Images"
    # os.chdir(path)
    # output = open(IMG_URL[46:], 'wb')
    # output.write(IMAGE.read())
    # output.close()
    # path = CUSTOM_PATH + "\sample\OEBPS\Text"
    # os.chdir(path)
    chapterFile.write('<p class="CI"><img alt="sample image" src="../Images/' + imageFilename + '\" /></p>\n')
    # #CONTENT = '        <item id=\"'  + IMG_URL[46:] + '\" href=\"Images/' + IMG_URL[46:] + '\" media-type=\"image/' + IMG_URL[-3:] + '\"/>\n'
    CONTENT = '        <item id=\"' + IMG_URL[46:] + '\" href=\"Images/' + imageFilename
    if IMG_URL[-3:] == 'jpg':
      CONTENT = CONTENT + '\" media-type=\"image/jpeg\"/>\n'
    else:
      CONTENT = CONTENT + '\" media-type=\"image/' + IMG_URL[-3:] + '\"/>\n'
    #   #CONTENT.replace(r"ge\/jp",r"ge\/jpe")
    #print (CONTENT)
    contentFile.write(CONTENT)






def makeEPUB(path):
  """Make EPUB from HTML file on the given path"""
  pass

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
        processHTML(fullName)
    else:
      print("downloading")
      downloadNovel(fullName)




