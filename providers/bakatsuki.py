#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import zipfile

try:  # Python 2
  from urllib2 import urlopen, HTTPError, URLError
except ImportError:  # Python 3
  from urllib.request import urlopen
  from urllib.error import HTTPError, URLError
  from urllib.parse import quote

from http.client import HTTPConnection

#noinspection PyCompatibility
import argparse
import progressive_download


URL_PREFIX = "http://www.baka-tsuki.org/project/index.php?title="
MAIN_PAGE = "http://www.baka-tsuki.org/project/index.php?title=Main_Page"
IMAGE_URL_BASE = 'http://www.baka-tsuki.org'
VOLUME_NAME = "Volume"
PRINT_SUFFIX = "&printable=yes"
FULL_TEXT_SUFFIX = "_Full_Text"
URL_VOLUME_SEPARATOR = ":"
FOLDER_VOLUME_SEPARATOR = "_" 
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

#display and URL names are often different on Bakatsuki
NAMING_TABLE = {
  "Infinite_Stratos" : "IS",
  "To_Aru_Majutsu_no_Index": "Toaru_Majutsu_no_Index"
}

#def getName(name, number, separator, volumeName):
def getName(name, number, volumeName=VOLUME_NAME):
  Hit = 0
  exactHit = 0
  tempName = name
  tempName = tempName.replace(" ","").lower()
  novelList = []
  listAllAvailableNovels(novelList)
  for novel in novelList:
    tempNovel = novel.replace("_","").lower()
    if tempName == tempNovel: 
      Hit = 1
      exactHit = 1
      name = re.sub(" ", "_", name)
  if (exactHit == 0):
    for novel in novelList:
      tempNovel = novel.replace("_","").lower()
      if re.search(tempName, tempNovel) is not None:
        foundMatch = (input('Did you mean \"%s\" ? (Y/n): ' % novel.replace("_"," ")))
        if foundMatch.lower() == 'y':
          Hit = 1
          name = novel
          print(name)		  
          if name in NAMING_TABLE:
            urlName = NAMING_TABLE[name]
            print("Replacing display name %s with URL name %s" % (name, urlName))
            name = urlName
          print(name) 
          break
  if Hit == 0:
    print ("Novel not Found\n")
  return name

def getFullName(name, number, volumeName=VOLUME_NAME):
  fullName = re.sub(" ", "_", name)
  fullName += URL_VOLUME_SEPARATOR + volumeName + str(number)
#  print (fullName)
  return fullName
 
def getFolderName(name, number, volumeName=VOLUME_NAME):
  folderName = re.sub(" ", "_", name)
  folderName += FOLDER_VOLUME_SEPARATOR + volumeName + str(number)
#  print(folderName)
  return folderName

def checkUrlExists(url):
  print("checking URL:\n%s" % url)
  try:
    urlopen(url)
    print("URL exists")
    return True
  except:
    print("URL does not work")
    return False

def getUrl(fullName):
  """get Url for a given novel"""
  volumeAlter = fullName.replace("Volume","Volume_")
  urls = [
    URL_PREFIX + fullName + PRINT_SUFFIX,
    URL_PREFIX + fullName + FULL_TEXT_SUFFIX + PRINT_SUFFIX,
    URL_PREFIX + volumeAlter + PRINT_SUFFIX,
    URL_PREFIX + volumeAlter + FULL_TEXT_SUFFIX + PRINT_SUFFIX
  ]
  workingUrl = None
  for url in urls:
    if checkUrlExists(url):
      workingUrl = url
      break
  return workingUrl

def downloadNovel(fullName, folderName):
  """download a novel with the given fullname"""
  url = getUrl(fullName)
  # assure storage folder exists
  if not os.path.exists(folderName):
    os.mkdir(folderName)
  filePath = os.path.join(folderName, "%s.html" % folderName)
  downloadUrl(url, filePath)

def downloadUrl(url, path):
  """Download URL if it is not already available"""
  if os.path.exists(path):
    print("not downloading, already exists:\n%s" % path)
  else:
    progressive_download.download(url, path)

def isLocallyAvailable(folderName):
  """check if a novel with this full name is locally available"""
  filename = "%s.html" % folderName
  return os.path.exists(os.path.join(folderName, filename))

def assurePath(path):
  """Make sure all directories in given path exist"""
  if not os.path.exists(path):
    print("creating dirs in path:\n%s" % path)
    os.makedirs(path)

def processHTML(fullName, folderName):
  """Process the raw HTML from Bakatsuki to a form usable for making EPUBs"""

  EXP = 0 #end of site
  H2 = 0 #start of novel text
  WIKI_TABLE = 0 #end of novel text

  print("opening novel: %s" % fullName)
  print("directory: %s" % folderName)
  filename = folderName + ".html"
  print("filename: %s" % filename)
  # folder name is fullName
  # filename is fullName + .html
  chapterFile = open(os.path.join(folderName,filename), "rt", encoding='utf-8')
  novel = chapterFile.read()
  chapterFile.close()
  # get title of the novel
  TITLE = getTitle(novel)

  # switch to the EPUB content folder
  toplevelFolder = os.path.join(folderName, EPUB_TOPLEVEL_FOLDER)
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
        #print (re.search('src="/project/images/thumb/', line))
        getImages(line, contentFile, chapterFile)
        ### if the line contains an image, the procedure adds the appropriate tags into the chapter.xhtml and content.opf files ###
      else:
        chapterFile.write(line)
        chapterFile.write("\n")
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
  </div>\n\
</body>\n\
</html>\n\
")
  titleFile.close()





  mimeFile = open(EPUB_MIME_FILE, 'w')
  mimeFile.write(EPUB_MIME)
  mimeFile.close()


  containerFile = open(EPUB_CONTAINER_FILE, 'w')
  containerFile.write("<?xml version=\"1.0\"?>\n \
<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">\n \
   <rootfiles>\n \
        <rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\"/>\n \
   </rootfiles>\n \
</container>")
  containerFile.close()

  stylesheetFile = open(EPUB_STYLESHEET_FILE, 'w')
  stylesheetFile.write("\
/* Style Sheet */\n\
/* This defines styles and classes used in the book */\n\
body { margin-left: 5%; margin-right: 5%; margin-top: 5%; margin-bottom: 5%; text-align: justify; }\n\
pre { font-size: x-small; }\n\
h1 { text-align: center; }\n\
h2 { text-align: center; }\n\
h3 { text-align: center; }\n\
h4 { text-align: center; }\n\
h5 { text-align: center; }\n\
h6 { text-align: center; }\n\
.CI {\n\
    text-align:center;\n\
    margin-top:0px;\n\
    margin-bottom:0px;\n\
    padding:0px;\n\
    }\n\
.center   {text-align: center;}\n\
.smcap    {font-variant: small-caps;}\n\
.u        {text-decoration: underline;}\n\
.bold     {font-weight: bold;}\n\
")
  stylesheetFile.close()

  templateFile = open(EPUB_STYLE_TEMPLATE_FILE, 'w')
  templateFile.write("\
<ade:template xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:ade=\"http://ns.adobe.com/2006/ade\"\n\
		 xmlns:fo=\"http://www.w3.org/1999/XSL/Format\">\n\
\n\
  <fo:layout-master-set>\n\
   <fo:simple-page-master master-name=\"single_column\">\n\
		<fo:region-body margin-bottom=\"3pt\" margin-top=\"0.5em\" margin-left=\"3pt\" margin-right=\"3pt\"/>\n\
    </fo:simple-page-master>\n\
  \n\
    <fo:simple-page-master master-name=\"single_column_head\">\n\
		<fo:region-before extent=\"8.3em\"/>\n\
		<fo:region-body margin-bottom=\"3pt\" margin-top=\"6em\" margin-left=\"3pt\" margin-right=\"3pt\"/>\n\
    </fo:simple-page-master>\n\
\n\
    <fo:simple-page-master master-name=\"two_column\"	margin-bottom=\"0.5em\" margin-top=\"0.5em\" margin-left=\"0.5em\" margin-right=\"0.5em\">\n\
		<fo:region-body column-count=\"2\" column-gap=\"10pt\"/>\n\
    </fo:simple-page-master>\n\
\n\
    <fo:simple-page-master master-name=\"two_column_head\" margin-bottom=\"0.5em\" margin-left=\"0.5em\" margin-right=\"0.5em\">\n\
		<fo:region-before extent=\"8.3em\"/>\n\
		<fo:region-body column-count=\"2\" margin-top=\"6em\" column-gap=\"10pt\"/>\n\
    </fo:simple-page-master>\n\
\n\
    <fo:simple-page-master master-name=\"three_column\" margin-bottom=\"0.5em\" margin-top=\"0.5em\" margin-left=\"0.5em\" margin-right=\"0.5em\">\n\
		<fo:region-body column-count=\"3\" column-gap=\"10pt\"/>\n\
    </fo:simple-page-master>\n\
\n\
    <fo:simple-page-master master-name=\"three_column_head\" margin-bottom=\"0.5em\" margin-top=\"0.5em\" margin-left=\"0.5em\" margin-right=\"0.5em\">\n\
		<fo:region-before extent=\"8.3em\"/>\n\
		<fo:region-body column-count=\"3\" margin-top=\"6em\" column-gap=\"10pt\"/>\n\
    </fo:simple-page-master>\n\
\n\
    <fo:page-sequence-master>\n\
        <fo:repeatable-page-master-alternatives>\n\
            <fo:conditional-page-master-reference master-reference=\"three_column_head\" page-position=\"first\" ade:min-page-width=\"80em\"/>\n\
            <fo:conditional-page-master-reference master-reference=\"three_column\" ade:min-page-width=\"80em\"/>\n\
            <fo:conditional-page-master-reference master-reference=\"two_column_head\" page-position=\"first\" ade:min-page-width=\"50em\"/>\n\
            <fo:conditional-page-master-reference master-reference=\"two_column\" ade:min-page-width=\"50em\"/>\n\
            <fo:conditional-page-master-reference master-reference=\"single_column_head\" page-position=\"first\" />\n\
            <fo:conditional-page-master-reference master-reference=\"single_column\"/>\n\
        </fo:repeatable-page-master-alternatives>\n\
    </fo:page-sequence-master>\n\
\n\
  </fo:layout-master-set>\n\
\n\
  <ade:style>\n\
    <ade:styling-rule selector=\".title_box\" display=\"adobe-other-region\" adobe-region=\"xsl-region-before\"/>\n\
  </ade:style>\n\
\n\
</ade:template>\n\
")
  templateFile.close()


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
    chapterFile.write('<div class="svg_outer svg_inner"><svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 824 1200" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink"><image height="1200" width="824" xlink:href="../Images/' + imageFilename + '"></image></svg></div>')
    #chapterFile.write('<p class="CI"><img alt="sample image" src="../Images/' + imageFilename + '\" /></p>\n')
    # #CONTENT = '        <item id=\"'  + IMG_URL[46:] + '\" href=\"Images/' + IMG_URL[46:] + '\" media-type=\"image/' + IMG_URL[-3:] + '\"/>\n'
    CONTENT = '        <item id=\"' + IMG_URL[46:] + '\" href=\"Images/' + imageFilename
    if IMG_URL[-3:] == 'jpg':
      CONTENT = CONTENT + '\" media-type=\"image/jpeg\"/>\n'
    else:
      CONTENT = CONTENT + '\" media-type=\"image/' + IMG_URL[-3:] + '\"/>\n'
    #   #CONTENT.replace(r"ge\/jp",r"ge\/jpe")
    #print (CONTENT)
    contentFile.write(CONTENT)


def _zipDirContent(path, zipPath):
  """Zip content of directory on path to zip file on zipPath
  :param path: path to directory contents to be zipped
  :param zipPath: path to the zip file
  """
  z = zipfile.ZipFile(zipPath, 'w', compression=zipfile.ZIP_DEFLATED)
  for root, dirs, files in os.walk(path):
    # print(root)
    for file in files:
      # remove the toplevel directory from storage path
      # NOTE: not sure how robust is this
      storagePath = os.path.join(root.replace(path,""), file)
      storagePath = storagePath.strip(os.sep)
      # zipfile will strip the leading separator in arcname
      z.write(os.path.join(root, file),arcname=storagePath)
  z.close()

def createEPUB(absolutePath, folderName):
  """Create EPUB from files present in the given folder
  absolutePath + folderName -> path to the folder for the given light novel
  folderName + .epub -> name of the EPUB file
  """
  os.chdir(os.path.join(absolutePath))
  zipPath = "%s.epub" % folderName
  print("creating EPUB file")
  sourcePath = os.path.join(absolutePath, folderName, EPUB_TOPLEVEL_FOLDER)
  _zipDirContent(sourcePath, zipPath)
  print("EPUB created: %s" % zipPath)


def listAllAvailableNovels(novels):
  """list all novels available from Bakatsuki"""
  LN = 0
  h = urlopen(MAIN_PAGE)
  for i in range(1000):
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
 # for novel in novels:
 #   print(novel.replace("_"," "))
  return novels
  
#def getStorageName(name, number, )

if __name__ == "__main__":
  # save PWD
  absoluteStartingPath = os.path.dirname(os.path.abspath(__file__))
  # CLI argument parsing
  parser = argparse.ArgumentParser(description='Light novel processing.')
  parser.add_argument('name',
    help="light novel name",
    action="store",
    nargs='?',
    default=None)
  parser.add_argument('--number',
    help="volume number",
    action="store",
    type=int,
    default=1
    )
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
  if args.list:
    listAllAvailableNovels()
  # get name of the novel
  elif args.name is not None:
    name = args.name
    name = getName(name, args.number)
    fullName = getFullName(name, args.number)
    folderName = getFolderName(name, args.number)
    print(fullName)
    if isLocallyAvailable(folderName):
      if args.r:
        print("re-downloading")
        downloadNovel(fullName, folderName)
      else:
        print("locally available")
    else:
      print("downloading")
      downloadNovel(fullName, folderName)
    processHTML(folderName, folderName)
    createEPUB(absoluteStartingPath, folderName)




