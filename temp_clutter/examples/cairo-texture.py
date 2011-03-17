import sys
from math import pi

import cairo
import clutter

def on_button_press_event (stage, event):
    clutter.main_quit()

def main ():
    stage = clutter.Stage()
    stage.set_color(clutter.Color(red=0xff, green=0xcc, blue=0xcc, alpha=0xff))
    stage.set_size(width=400, height=300)
    stage.connect('button-press-event', on_button_press_event)
    stage.connect('destroy', clutter.main_quit)

    cairo_tex = clutter.CairoTexture(width=200, height=200)
    cairo_tex.set_position(x=(stage.get_width() - 200) / 2,
                           y=(stage.get_height() - 200) / 2)

    # we obtain a cairo context from the clutter.CairoTexture
    # and then we can use it with the cairo primitives to draw
    # on it.
    context = cairo_tex.cairo_create()

    # we scale the context to the size of the surface
    context.scale(200, 200)
    context.set_line_width(0.1)
    context.set_source_color(clutter.Color(255, 0, 0, 0x88))
    context.translate(0.5, 0.5)
    context.arc(0, 0, 0.4, 0, pi * 2)
    context.stroke()

    del(context) # we need to destroy the context so that the
                 # texture gets properly updated with the result
                 # of our operations; you can either move all the
                 # drawing operations into their own function and
                 # let the context go out of scope or you can
                 # explicitly destroy it

    # clutter.CairoTexture is a clutter.Actor, so we can
    # manipulate it as any other actor
    center_x = cairo_tex.get_width() / 2
    center_z = cairo_tex.get_height() / 2
    cairo_tex.set_rotation(clutter.Y_AXIS, 45.0, center_x, 0, center_z)
    stage.add(cairo_tex)
    cairo_tex.show()
    
    # clutter.CairoTexture is also a clutter.Texture, so we can save
    # memory when dealing with multiple copies by simply cloning it
    # and manipulating the clones
    clone_tex = clutter.Clone(cairo_tex)
    clone_tex.set_position((stage.get_width() - 200) / 2,
                           (stage.get_height() - 200) / 2)
    clone_tex.set_rotation(clutter.Y_AXIS, -45.0, center_x, 0, center_z)
    stage.add(clone_tex)
    clone_tex.show()

    stage.show()

    clutter.main()

    return 0

if __name__ == '__main__':
    sys.exit(main())
