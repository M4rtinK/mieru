import sys
import clutter

try:
    from clutter.glx import TexturePixmap
    print "Using GLX TexturePixmap"
except:
    try:
        from clutter.x11 import TexturePixmap
        print "Using X11 TexturePixmap"
    except:
        print "Can't import clutter.glx or clutter.x11"
        sys.exit(1)


if len(sys.argv) != 2:
    print "Usage: %s <window-id>" % sys.argv[0]
    print "To obtain a window id, use 'xwininfo' and point to an existing "
    print "window. (e.g. 0x3e00009 would be a valid id)"
    sys.exit(1)


def on_allocate(tex, box, flags, stage):
    width, height = tex.get_size()
    print "Got window size %ix%i" % (width, height)
    print "Changing stage's size"
    stage.set_size(width, height)


stage = clutter.Stage()
stage.connect('destroy', clutter.main_quit)

window_id = long(sys.argv[1], 0)
print "Trying window-id %s (%i)" % (sys.argv[1], window_id)

tex = TexturePixmap(window=window_id)
tex.set_automatic(True)
tex.connect('allocation-changed', on_allocate, stage)
stage.add(tex)

stage.show()
clutter.main()
