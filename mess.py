"a clutter in GTK module"

import gtk

LINEAR = 0
EASE_IN_BACK = 0
EASE_IN_BOUNCE = 0
EASE_IN_CIRC = 0
EASE_IN_CUBIC = 0
EASE_IN_ELASTIC = 0
EASE_IN_EXPO = 0
EASE_IN_OUT_BACK = 0
EASE_IN_OUT_BOUNCE = 0
EASE_IN_OUT_CIRC = 0
EASE_IN_OUT_CUBIC = 0
EASE_IN_OUT_ELASTIC = 0
EASE_IN_OUT_EXPO = 0
EASE_IN_OUT_QUAD = 0
EASE_IN_OUT_QUART = 0
EASE_IN_OUT_QUINT = 0
EASE_IN_OUT_SINE = 0
EASE_IN_QUAD = 0
EASE_IN_QUART = 0
EASE_IN_QUINT = 0
EASE_IN_SINE = 0
EASE_OUT_BACK = 0
EASE_OUT_BOUNCE = 0
EASE_OUT_CIRC = 0
EASE_OUT_CUBIC = 0
EASE_OUT_ELASTIC = 0
EASE_OUT_EXPO = 0
EASE_OUT_QUAD = 0
EASE_OUT_QUART = 0
EASE_OUT_QUINT = 0
EASE_OUT_SINE = 0

def color_from_string(string):
  return None

class Group(gtk.Widget):
  def __init__(self):
    pass
#    gtk.Widget.__init__(self)

  def add(self, actor):
    return



class Alpha:
  def __init__(self, tl, easing):
    pass

  def start(self):
    pass

  def stop(self):
    pass

  def connect(self, signal, callback, *args):
    pass


class Timeline:
  def __init__(self, duration):
    pass
  
  def start(self):
    pass
  
  def stop(self):
    pass

  def connect(self, signal, callback, *args):
    pass


class ReActor:
  def __init__(self, mieru):

    self.mieru = mieru
    self.group = None
    self.w = 0
    self.h = 0
    self.x = 0
    self.y = 0

  def set_group(self, group):
    self.group = group

  def connect(self, signal, callback, *args):
    pass

  def set_reactive(self, bool):
    return

  def show(self):
    return


class StopMotion():
  # clutter animation
  def __init__(self):
    pass

  def connect(self, signal, callback, *args):
    pass



class Texture(ReActor):
  def __init__(self, mieru):
    ReActor.__init__(self, mieru)
    self.px = None

  def set_from_rgb_data(self, pixels, alpha, w, h, row, bpp, flags):
    self.px = gtk.gdk.Pixmap(self.mieru.stage.window, w, h)
    gc = self.px.new_gc()
    self.w = w
    self.h = h
    if bpp == 3:
      self.px.draw_rgb_image(gc, 0,0,w,h,gtk.gdk.RGB_DITHER_NONE, pixels, row)
    else:
      self.px.draw_rgb_32_image(gc, 0,0,w,h,gtk.gdk.RGB_DITHER_NONE, pixels, row)

  def get_size(self):
    return (self.w, self.h)

  def get_position(self):
    return (self.x, self.y)

  def animate(self, alpha, duration, *args):
    print args
    return StopMotion()

  def set_keep_aspect_ratio(self, bool):
    return









class MuStache(gtk.DrawingArea):
  def __init_(self):
    gtk.DrawingArea.__init__(self)

  def set_color(self, color):
    pass

  def add(self, reactor):
    pass

  def connect(self, signal, callback, *args):
    pass

  def lower_child(self, one, two):
    pass

class Embed(gtk.VBox):
  def __init__(self):
    gtk.Box.__init__(self)
    widget = MuStache()
    self.pack_start(widget)
    self.stage = widget

  def get_stage(self):
    return self.stage

  def realize(self):
    pass

  def show(self):
    pass

  def connect(self, *args):
    pass