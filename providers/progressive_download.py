# -*- coding: utf-8 -*-
"""
downloading with progress information
based on:
http://stackoverflow.com/questions/2028517/python-urllib2-progress-hook
"""
import sys

try:  # Python 2
  from urllib2 import urlopen, HTTPError, URLError
except ImportError:  # Python 3
  from urllib.request import urlopen
  from urllib.error import HTTPError, URLError

def _chunk_report(bytes_so_far, chunk_size, total_size):
  if total_size:
    percent = float(bytes_so_far) / total_size
    percent = round(percent*100, 2)
    sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
                     (bytes_so_far, total_size, percent))

    if bytes_so_far >= total_size:
      sys.stdout.write('\n')
  else:
    sys.stdout.write("Downloaded %d bytes\r" % bytes_so_far)


def _chunk_download(url, path, chunk_size=8192, report_hook=None):
  """
  response hook = None -> select response hook automatically
  response hook = False -> do not use response hook
  """
  response = urlopen(url)
  total_size = response.info().getheader('Content-Length')
  if total_size:
    total_size = total_size.strip()
    total_size = int(total_size)
  bytes_so_far = 0

  f = open(path, "w")

  while 1:
    chunk = response.read(chunk_size)
    bytes_so_far += len(chunk)
    f.write(chunk)

    if not chunk:
      break

    if report_hook is None:
      _chunk_report(bytes_so_far, chunk_size, total_size)
  f.close()

  return bytes_so_far

def download(url, path, report_hook=None, verbose=True):

  if verbose:
    print(url)
  _chunk_download(url, path, report_hook=None)


if __name__ == '__main__':
  download("http://www.modrana.org/om2012/mobile_os_om2012.odp", "test.odp")

