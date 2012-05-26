# -*- coding: utf-8 -*-
#Mieru manga-container providers
#
#the aim of this class is to wrap various online services that provide
# mangas and other content

class Provider:
  def __init__(self):
    """
    an abstract manga provider class
    """
    pass

  def search(self, term):
    """
    search for a given term
    """
    pass

  def getChapter(self, identifier):
    """
    get a container with a the given identifier
    """
    pass

  def getChapters(self, identifiers):
    """
    a convenience function for getting chapters as provided by a list of
    identifiers

    by default, we just iterate over the list and return an identifier:container
    dictionary but services that support batch downloading multiple chapters might
    want to override this function
    """
    results = {}
    for id in identifiers:
      result = self.getChapter(id)
      # only return valid results
      if result:
        results[id] = result
    return results

  def getSeries(self, identifier):
    """"
    return a series object corresponding to the given identifier
    """
    pass

class MangafoxProvider(Provider):
  def __init__(self):
    Provider.__init__()
