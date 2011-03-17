#import pygtk
#pygtk.require('2.0')
#import gtk
import sys
if len (sys.argv) > 1:
  firstParam = sys.argv[1]
  if firstParam == "n900":
    sys.path.append('temp_clutter')
#import cluttergtk
import clutter
import page

stage = clutter.Stage()
stage.set_size(800,480)
stage.set_color(clutter.color_from_string('Black'))
stage.connect('destroy', clutter.main_quit)

p = page.Page('manga.jpg')

stage.add(p)
stage.show()
clutter.main()

