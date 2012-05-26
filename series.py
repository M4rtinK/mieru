# -*- coding: utf-8 -*-
#Mieru manga series handling
#
#a series is a contains one or more chapter containers and
#some added metadata, such as the series author/'s
#

class Series:
  def __init__(self, chapters = []):
    self.chapters = chapters
    self.authors = []

  def getAuthors(self):
    return self.authors

  def getChapterCount(self):
    return len(self)